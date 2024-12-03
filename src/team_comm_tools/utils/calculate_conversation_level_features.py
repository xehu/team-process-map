# Importing modules from features
from team_comm_tools.features.basic_features import *
from team_comm_tools.features.get_all_DD_features import *
from team_comm_tools.features.turn_taking_features import*
from team_comm_tools.features.burstiness import *
from team_comm_tools.features.information_diversity import *
from team_comm_tools.utils.summarize_features import *
from team_comm_tools.utils.gini_coefficient import *
from team_comm_tools.utils.preprocess import *
from fuzzywuzzy import process

class ConversationLevelFeaturesCalculator:
    """
    Initialize variables and objects used by the ConversationLevelFeaturesCalculator class.

    This class uses various feature modules to define conversation-level features. It reads input data and
    initializes variables required to compute the features.

    :param chat_data: Pandas dataframe of chat-level features read from the input dataset
    :type chat_data: pd.DataFrame
    :param user_data: Pandas dataframe of user-level features derived from the chat-level dataframe
    :type user_data: pd.DataFrame
    :param conv_data: Pandas dataframe of conversation-level features derived from the chat-level dataframe
    :type conv_data: pd.DataFrame
    :param vect_data: Pandas dataframe of processed vectors derived from the chat-level dataframe
    :type vect_data: pd.DataFrame
    :param vector_directory: Directory where vector files are stored
    :type vector_directory: str
    :param convo_aggregation: If true, will aggregate features at the conversational level
    :type convo_aggregation: bool
    :param convo_methods: Specifies which functions users want to aggregate with (e.g., mean, stdev...)
    :type convo_methods: list
    :param convo_columns: Specifies which columns (at the chat level) users want aggregated
    :type convo_columns: list
    :param user_aggregation: If true, will aggregate features at the user level
    :type convo_aggregation: bool
    :param user_methods: Specifies which functions users want to aggregate with (e.g., mean, stdev...) at the user level
    :type user_methods: list
    :param user_columns: Specifies which columns (at the chat level) users want aggregated for the user level
    :type user_columns: list
    :param chat_features: Tracks all the chat-level features generated by the toolkit
    :type chat_features: list
        """
    def __init__(self, chat_data: pd.DataFrame, 
                        user_data: pd.DataFrame, 
                        conv_data: pd.DataFrame, 
                        vect_data: pd.DataFrame, 
                        vector_directory: str, 
                        conversation_id_col: str,
                        speaker_id_col: str,
                        message_col: str,
                        timestamp_col: str,
                        convo_aggregation: bool,
                        convo_methods: list,
                        convo_columns: list,
                        user_aggregation: bool,
                        user_methods: list,
                        user_columns: list,
                        chat_features: list,
                        ) -> None:

        # Initializing variables
        self.chat_data = chat_data
        self.user_data = user_data
        self.conv_data = conv_data
        self.vect_data = vect_data
        self.vector_directory = vector_directory
        self.conversation_id_col = conversation_id_col
        self.speaker_id_col = speaker_id_col
        self.message_col = message_col
        self.timestamp_col = timestamp_col
        self.convo_aggregation = convo_aggregation
        self.convo_methods = convo_methods
        self.user_aggregation = user_aggregation
        self.user_methods = user_methods
        self.user_columns = user_columns
        self.chat_features = chat_features

        def clean_up_aggregation_method_names(aggregation_method_names:list) -> list:
            """
            Clean up different ways of specifying the aggregation names; e.g., point "average" and "max"
            to the same function

            :param aggregation_method_names: The list of method names requested by the user for aggregation
            :type aggregation_method_names: list

            :return: the list of valid methods that can be used for aggregation
            :rtype: list
            """

            aggregation_method_names = aggregation_method_names.copy()

            for i in range(len(aggregation_method_names)):
                # directly modify the list to replace synonyms
                if aggregation_method_names[i] == "average":
                    aggregation_method_names[i] = "mean"
                if aggregation_method_names[i] == "maximum":
                    aggregation_method_names[i] = "max"
                if aggregation_method_names[i] == "minimum":
                    aggregation_method_names[i] = "min"
                if aggregation_method_names[i] == "standard deviation":
                    aggregation_method_names[i] = "stdev"
                if aggregation_method_names[i] == "sd":
                    aggregation_method_names[i] = "stdev"
                if aggregation_method_names[i] == "std":
                    aggregation_method_names[i] = "stdev"
                if aggregation_method_names[i] == "total":
                    aggregation_method_names[i] = "sum"
                if aggregation_method_names[i] == "add":
                    aggregation_method_names[i] = "sum"
                if aggregation_method_names[i] == "summing":
                    aggregation_method_names[i] = "sum"
                            
                current = aggregation_method_names[i]

                if current != "mean" and current != "max" and current != "min" and current != "stdev" and current != "median" and current != "sum":
                    print("Warning: ", current, "is not a valid user method. Valid methods are: [mean, max, min, stdev, median, sum]. Ignoring...")
                    aggregation_method_names.remove(current)

                # print a warning for sum, since not all sums make sense; e.g., it makes sense to sum the total number of words, but not to sum the positivity scores
                if current == "sum":
                    print("INFO: User requested 'sum'. Ensure summing is appropriate; it is helpful for countable metrics like word counts. For non-countable metrics, such as sentiment ratings, consider using the mean instead.")

            return aggregation_method_names

        def ensure_aggregation_columns_present(user_inputted_columns:list, agg_param:str) -> list:
            
            """
            An error checking function to ensure that the columns inputted by the user are present in the data.

            :param user_inputted_columns: The list of columns requested by the user for aggregation
            :type user_inputted_columns: list

            :param user_inputted_columns: The name of the parameter the user specified for aggregation (convo_columns or user_columns)
            :type user_inputted_columns: str

            :return: the list of valid columns that can be aggregated (they are present in the chat data AND generated by us)
            :rtype: list
            """
            columns_in_data = list(set(user_inputted_columns).intersection(set(self.chat_features).intersection(set(self.chat_data.columns))))
            if(len(columns_in_data) != len(user_inputted_columns)):
                print(
                    f"Warning: One or more columns requested for aggregation using the {agg_param} parameter are not valid. Ignoring..."
                )
                # help the user fix their error
                for i in user_inputted_columns:
                    matches = process.extract(i, self.chat_data.columns, limit=3)
                    best_match, similarity = matches[0]
                    
                    if similarity == 100:
                        continue
                    elif similarity >= 80:
                        print("Did you mean", best_match, "instead of", i, "?")
                    else:
                        print(i, "not found in data and no close match.")

            return columns_in_data

        # check if user inputted convo_columns is None
        # If 'None', the default behavior is to summarize all numeric columns generated at the chat level
        if convo_columns is None:
            self.columns_to_summarize = [column for column in set(self.chat_features).intersection(set(self.chat_data.columns)) \
                                        if pd.api.types.is_numeric_dtype(self.chat_data[column])]
        else:
            if convo_aggregation == True and (len(convo_columns) == 0 or len(convo_methods) == 0):
                print(
                    "Warning: convo_aggregation is True but no convo_columns specified. Defaulting convo_aggregation to False."
                )
                self.convo_aggregation = False
            else:
                # to check if columns are in data and in the list of features we generate
                convo_columns_in_data = ensure_aggregation_columns_present(user_inputted_columns = convo_columns, agg_param = "convo_columns")   
                self.columns_to_summarize = convo_columns_in_data
                
                # ensure all lowercase
                self.convo_methods = [col.lower() for col in self.convo_methods]
                self.columns_to_summarize = [col.lower() for col in self.columns_to_summarize]
                
                # check if columns are numeric
                for col in self.columns_to_summarize:
                    if pd.api.types.is_numeric_dtype(self.chat_data[col]) is False:
                        print("WARNING: ", col, " is not numeric. Ignoring...")
                        self.columns_to_summarize.remove(col)

        # check if user inputted user_columns is None
        # as with the conversation level, we default to aggregating all generated chat-level features
        if user_columns is None:
            self.user_columns = [column for column in set(self.chat_features).intersection(set(self.chat_data.columns)) \
                                        if pd.api.types.is_numeric_dtype(self.chat_data[column])]
        else:
            if user_aggregation == True and len(user_columns) == 0:
                print("Warning: user_aggregation is True but no user_columns specified. Defaulting user_aggregation to False.")
                self.user_aggregation = False
            else:
                # to check if columns are in data
                user_columns_in_data = ensure_aggregation_columns_present(user_inputted_columns = user_columns, agg_param = "user_columns")
                self.user_columns = user_columns_in_data
                
                # ensure all lowercase
                self.user_methods = [col.lower() for col in self.user_methods]
                self.user_columns = [col.lower() for col in self.user_columns]
                
                # check if columns are numeric
                for col in self.user_columns:
                    if pd.api.types.is_numeric_dtype(self.chat_data[col]) is False:
                        print("WARNING: ", col, " is not numeric. Ignoring...")
                        self.user_columns.remove(col)
                   
        # replace interchangable words in convo_methods and remove invalid methods
        self.convo_methods = clean_up_aggregation_method_names(aggregation_method_names = self.convo_methods)
    
        # replace interchangable words in user_methods and remove invalid methods
        self.user_methods = clean_up_aggregation_method_names(aggregation_method_names = self.user_methods)
        
        # columns that need to be summed due to dependency on gini coefficient
        self.summable_columns = ["num_words", "num_chars", "num_messages"]

        
    def calculate_conversation_level_features(self, feature_methods: list) -> pd.DataFrame:
        """
        Main driver function for creating conversation-level features.

        This function computes various conversation-level features by aggregating chat-level and user-level features,
        and appends them as new columns to the input conversation-level data.

        :param feature_methods: The list of methods to use to generate features
        :type turns: list

        :return: The conversation-level dataset with new columns for each conversation-level feature
        :rtype: pd.DataFrame
        """

        for method in feature_methods:
            method(self)

        return self.conv_data

    def get_turn_taking_features(self) -> None:
        """
        Calculate the turn-taking index in the conversation.

        This function merges turn-taking features into the conversation-level data.

        :return: None
        :rtype: None
        """

        self.conv_data = pd.merge(
            left=self.conv_data,
            right=get_turn(self.chat_data.copy(), self.conversation_id_col, self.speaker_id_col),
            on=[self.conversation_id_col],
            how="inner"
        )

    def get_gini_features(self) -> None:
        """
        Calculate the Gini index for relevant features in the conversation.

        This function computes the Gini index for features involving counts, such as:
        - Word count
        - Character count
        - Message count

        The Gini index is then merged into the conversation-level data.

        :return: None
        :rtype: None
        """
        for column in self.summable_columns:
            self.conv_data = pd.merge(
                left=self.conv_data,
                right=get_gini(self.user_data.copy(), "sum_"+column, self.conversation_id_col), # this applies to the summed columns in user_data, which matches the above
                on=[self.conversation_id_col],
                how="inner"
            )

    def get_conversation_level_aggregates(self) -> None:
        """
        Aggregate summary statistics from chat-level features to conversation-level features.

        This function calculates and merges the following aggregation functions for each summarizable feature:
        - Average/Mean
        - Standard Deviation
        - Minimum
        - Maximum

        For countable features (e.g., num_words, num_chars, num_messages), it also calculates and merges the sum.

        :return: None
        :rtype: None
        """

        if self.convo_aggregation == True:
            # For each summarizable feature
            for column in self.columns_to_summarize:
                
                # Average/Mean of feature across the Conversation
                if 'mean' in self.convo_methods:
                    self.conv_data = pd.merge(
                        left=self.conv_data,
                        right=get_mean(self.chat_data.copy(), column, 'mean_'+column, self.conversation_id_col),
                        on=[self.conversation_id_col],
                        how="inner"
                    )

                # Standard Deviation of feature across the Conversation
                if 'stdev' in self.convo_methods:
                    self.conv_data = pd.merge(
                        left=self.conv_data,
                        right=get_stdev(self.chat_data.copy(), column, 'stdev_'+column, self.conversation_id_col),
                        on=[self.conversation_id_col],
                        how="inner"
                    )

                # Minima for the feature across the Conversation
                if 'min' in self.convo_methods:
                    self.conv_data = pd.merge(
                        left=self.conv_data,
                        right=get_min(self.chat_data.copy(), column, 'min_'+column, self.conversation_id_col),
                        on=[self.conversation_id_col],
                        how="inner"
                    )

                # Maxima for the feature across the Conversation
                if 'max' in self.convo_methods:
                    self.conv_data = pd.merge(
                        left=self.conv_data,
                        right=get_max(self.chat_data.copy(), column, 'max_'+column, self.conversation_id_col),
                        on=[self.conversation_id_col],
                        how="inner"
                    )
                    
                # Median for the feature across the Conversation
                if 'median' in self.convo_methods:
                    self.conv_data = pd.merge(
                        left=self.conv_data,
                        right=get_median(self.chat_data.copy(), column, 'median_'+column, self.conversation_id_col),
                        on=[self.conversation_id_col],
                        how="inner"
                    )

                # Sum for the feature across the Conversation
                if column not in self.summable_columns: # do this only for things we are not already auto-summarizing
                    if 'sum' in self.convo_methods:
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_sum(self.chat_data.copy(), column, 'sum_'+column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )

        # Compute some sums regardless of user specifications, as it's necessary for gini.
        for column in self.summable_columns:
            # Sum for the feature across the Conversation
            self.conv_data = pd.merge(
                left=self.conv_data,
                right=get_sum(self.chat_data.copy(), column, 'sum_'+column, self.conversation_id_col),
                on=[self.conversation_id_col],
                how="inner"
            )

    def get_user_level_aggregates(self) -> None:
        """
        Aggregate summary statistics from user-level features to conversation-level features.

        This function calculates and merges the following aggregation functions for each user-level feature:
        - Average/Mean of summed user-level features
        - Standard Deviation of summed user-level features
        - Minimum of summed user-level features
        - Maximum of summed user-level features
        - Average/Mean of averaged user-level features
        - Standard Deviation of averaged user-level features
        - Minimum of averaged user-level features
        - Maximum of averaged user-level features


        :return: None
        :rtype: None
        """

        if self.convo_aggregation == True and self.user_aggregation == True:
            
            # aggregates from the user level based on conversation methods
            if 'mean' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                         # Average/Mean of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_mean(self.user_data.copy(), user_method + "_" +user_column, "mean_user_" + user_method + "_" +user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )

            if 'stdev' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                        # Standard Deviation of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_stdev(self.user_data.copy(), user_method + "_" + user_column, 'stdev_user_' + user_method + "_" + user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )

            if 'min' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                        # Minima of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_min(self.user_data.copy(), user_method + "_" + user_column, 'min_user_' + user_method + "_" + user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )
                
            if 'max' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                        # Maxima of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_max(self.user_data.copy(), user_method + "_" + user_column, 'max_user_' + user_method + "_" + user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )
                        
            if 'median' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                        # Median of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_median(self.user_data.copy(), user_method + "_" + user_column, 'median_user_' + user_method + "_" + user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )

            if 'sum' in self.convo_methods:
                for user_column in self.user_columns:
                    for user_method in self.user_methods:
                        # Sum of User-Level Feature
                        self.conv_data = pd.merge(
                            left=self.conv_data,
                            right=get_sum(self.user_data.copy(), user_method + "_" + user_column, 'sum_user_' + user_method + "_" + user_column, self.conversation_id_col),
                            on=[self.conversation_id_col],
                            how="inner"
                        )

    def get_discursive_diversity_features(self) -> None:
        """
        Calculate discursive diversity features for each conversation.

        This function computes discursive diversity based on the word embeddings (SBERT) 
        and chat-level information, and merges the features into the conversation-level data.

        :return: None
        :rtype: None
        """
        self.conv_data = pd.merge(
            left=self.conv_data,
            right=get_DD_features(self.chat_data, self.vect_data, self.conversation_id_col, self.speaker_id_col, self.timestamp_col),
            on=[self.conversation_id_col],
            how="inner"
        )
            
      
    def calculate_team_burstiness(self) -> None:
        """
        Calculate the team burstiness coefficient.

        This function computes the team burstiness coefficient by looking at the differences 
        in standard deviation and mean of the time intervals between chats, and merges the 
        results into the conversation-level data.

        :return: None
        :rtype: None
        """
        if {'time_diff'}.issubset(self.chat_data.columns):
            self.conv_data = pd.merge(
            left = self.conv_data,
            right = get_team_burstiness(self.chat_data, "time_diff", self.conversation_id_col),
            on = [self.conversation_id_col],
            how = "inner"
        )
    
    def calculate_info_diversity(self) -> None:
        """
        Calculate an information diversity score for the team.

        This function computes the information diversity score by looking at the cosine 
        similarity between the mean topic vector of the team and each message's topic vectors, 
        and merges the results into the conversation-level data.

        :return: None
        :rtype: None
        """
        self.conv_data = pd.merge(
            left = self.conv_data,
            right = get_info_diversity(self.chat_data, self.conversation_id_col, self.message_col),
            on = [self.conversation_id_col],
            how = "inner"
        )