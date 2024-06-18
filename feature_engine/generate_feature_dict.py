import pickle
from utils.calculate_chat_level_features import ChatLevelFeaturesCalculator
from utils.calculate_conversation_level_features import ConversationLevelFeaturesCalculator

if __name__ == "__main__":

  features = {
      "Positivity (BERT)": {
        "columns": ["positive_bert", "negative_bert", "neutral_bert"],
        "file": "bert_features.py",
        "level": "Chat",
        "semantic_grouping": "Emotion",
        "description": "The extent to which a statement is positive, negative, or neutral, as assigned by Cardiffnlp/twitter-roberta-base-sentiment-latest. The total scores (Positive, Negative, Neutral) sum to 1.",
        "references": "(Hugging Face, 2023)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/BERT-Sentiment-Analysis-Feature"
      },
      "Message Length" : {
        "columns": ["num_words", "num_chars"],
        "file": "message_length_features.py",
        "level": "Chat",
        "semantic_grouping": "Quantity",
        "description": "The length of a message in words and characters.",
        "references": "(Ranganath et al., 2013; Cao et al., 2021)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-Number-Words,-Messages-Per-Person"
      },
      "Message Quantity": {
        "columns": ["num_messages"],
        "file": "message_quantity_features.py",
        "level": "Conversation,Speaker",
        "semantic_grouping": "Quantity",
        "description": "The total number of messages sent.",
        "references": "(Cao et al., 2021; Marlow et al., 2018, as objective communication frequency)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-Number-Words,-Messages-Per-Person"
      },
      "Information Exchange" : {
        "columns": [
          "info_exchange_zscore_chats",
          "info_exchange_zscore_conversation"
        ],
        "file": "information_exchange_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "A crude measure of task-focused communication: the total number of words spoken, with the number of first-person pronouns (which suggest self-focus) removed. This value is then z-scored to describe the extent to which a message had more/less task-focused communication relative to other messages. We implement two flavors of the z-score: the first scores the messages with respect to other messages in the same conversation; the second scores the messages with respect to all messages in the data.",
        "references": "(Tausczik & Pennebaker, 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/E.24-Information-Exchange"
      },
      "LIWC and Other Lexicons": {
        "columns": [
          "discrepancies_lexical_per_100",
          "hear_lexical_per_100",
          "home_lexical_per_100",
          "conjunction_lexical_per_100",
          "certainty_lexical_per_100",
          "inclusive_lexical_per_100",
          "bio_lexical_per_100",
          "achievement_lexical_per_100",
          "adverbs_lexical_per_100",
          "anxiety_lexical_per_100",
          "third_person_lexical_per_100",
          "negation_lexical_per_100",
          "swear_lexical_per_100",
          "death_lexical_per_100",
          "health_lexical_per_100",
          "see_lexical_per_100",
          "body_lexical_per_100",
          "family_lexical_per_100",
          "negative_affect_lexical_per_100",
          "quantifier_lexical_per_100",
          "positive_affect_lexical_per_100",
          "insight_lexical_per_100",
          "humans_lexical_per_100",
          "present_tense_lexical_per_100",
          "future_tense_lexical_per_100",
          "past_tense_lexical_per_100",
          "relative_lexical_per_100",
          "sexual_lexical_per_100",
          "inhibition_lexical_per_100",
          "sadness_lexical_per_100",
          "social_lexical_per_100",
          "indefinite_pronoun_lexical_per_100",
          "religion_lexical_per_100",
          "work_lexical_per_100",
          "money_lexical_per_100",
          "causation_lexical_per_100",
          "anger_lexical_per_100",
          "first_person_singular_lexical_per_100",
          "feel_lexical_per_100",
          "tentativeness_lexical_per_100",
          "exclusive_lexical_per_100",
          "verbs_lexical_per_100",
          "friends_lexical_per_100",
          "article_lexical_per_100",
          "argue_lexical_per_100",
          "auxiliary_verbs_lexical_per_100",
          "cognitive_mech_lexical_per_100",
          "preposition_lexical_per_100",
          "first_person_plural_lexical_per_100",
          "percept_lexical_per_100",
          "second_person_lexical_per_100",
          "positive_words_lexical_per_100",
          "first_person_lexical_per_100",
          "nltk_english_stopwords_lexical_per_100",
          "hedge_words_lexical_per_100"
        ],
        "file": "liwc_lexicon_features.py",
        "level": "Chat",
        "semantic_grouping": ["Content", "Emotion", "Engagement"],
        "description": "The extent to which messages reflect words from a variety of lexicons (predominantly LIWC). Each measure is expressed as a rate of word use per 100 words.",
        "references": "(For LIWC: Niederhoffer & Pennebaker, 2002; Pennebaker et al., 1997; Tausczik & Pennebaker, 2010; for NLTK English Stopwords: Inspired by Yeomans et al. (2023), which notes the role of stylistic and structural language (e.g., function words), which frequently appear in stopword lists.)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-LIWC-Lexical-Word-Counts"
      },
      "Questions": {
        "columns": ["num_question_naive"],
        "file": "questions_features.py",
        "level": "Chat",
        "semantic_grouping": "Engagement",
        "description": "Number of questions asked in an utterance. In the naive version, it counts the number of question marks (’?’).",
        "references": "(Ranganath et al., 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Questions-&-NTRI-(next-turn-repair-indicators)"
      },
      "Conversational Repair": {
        "columns": ["NTRI"],
        "file": "conversational_repair_features.py",
        "level": "Chat",
        "semantic_grouping": "Engagement",
        "description": "A binary indicator of whether an utterance contains a repair indicator, defined as the following: - “what?” - “sorry” - “excuse me” - “huh?” - “who?” - “pardon?” - “say … again?” - “what’s that?” - “what is that”",
        "references": "(Ranganath et al., 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Questions-&-NTRI-(next-turn-repair-indicators)"
      },
      "Word Type-Token Ratio": {
        "columns": ["word_TTR"],
        "file": "word_ttr_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "The ratio of word types (the total number of unique words in an utterance) to tokens (the total number of words in an utterance).",
        "references": "(Reichel et al., 2015)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.13-Word-Type-Token-Ratio,-Proportion-of-First-Person-Pronouns"
      },
      "Proportion of First-Person Pronouns": {
        "columns": ["first_pronouns_proportion"],
        "file": "first_person_pronouns_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "The proportion of words in an utterance that are first-person pronouns (e.g., “I,” “me,” “we,” “us”).",
        "references": "(Reichel et al., 2015)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.13-Word-Type-Token-Ratio,-Proportion-of-First-Person-Pronouns"
      },
      "Function Word Accommodation": {
        "columns": ["function_word_accommodation"],
        "file": "function_word_accommodation_features.py",
        "level": "Chat",
        "semantic_grouping": "Variance",
        "description": "The total number of function words used in a given turn that were also used in the previous turn. Function words are defined as a list of 190 words from the source paper.",
        "references": "(Ranganath et al., 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Mimicry:-Function-word,-Content-word,-BERT,-Moving"
      },
      "Content Word Accommodation": {
        "columns": ["content_word_accommodation"],
        "file": "content_word_accommodation_features.py",
        "level": "Chat",
        "semantic_grouping": "Variance",
        "description": "The total number of non-function words used in a given turn that were also used in the previous turn, normalized by the inverse document frequency of each content word.",
        "references": "(Ranganath et al., 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Mimicry:-Function-word,-Content-word,-BERT,-Moving"
      },
      "(BERT) Mimicry": {
        "columns": ["mimicry_bert"],
        "file": "bert_mimicry_features.py",
        "level": "Chat",
        "semantic_grouping": "Variance",
        "description": "The cosine similarity of the SBERT vectors between the current utterance and the utterance in the previous turn.",
        "references": "Inspired by accommodation (Matarazzo & Wiens, 1977), language style matching (Tausczik & Pennebaker, 2013) and synchrony (Niederhoffer & Pennebaker, 2002), and implemented in a manner similar to forward flow (Gray et al., 2019)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Mimicry:-Function-word,-Content-word,-BERT,-Moving"
      },
      "Moving Mimicry": {
        "columns": ["moving_mimicry"],
        "file": "moving_mimicry_features.py",
        "level": "Chat",
        "semantic_grouping": "Variance",
        "description": "The running average of all BERT Mimicry scores computed so far in a conversation. Captures the extent to which all participants in a conversation mimic each other up until a given point.",
        "references": "Inspired by accommodation (Matarazzo & Wiens, 1977), language style matching (Tausczik & Pennebaker, 2013) and synchrony (Niederhoffer & Pennebaker, 2002), and implemented in a manner similar to forward flow (Gray et al., 2019)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Mimicry:-Function-word,-Content-word,-BERT,-Moving"
      },
      "Hedge": {
        "columns": ["hedge_naive"],
        "file": "hedge_features.py",
        "level": "Chat",
        "semantic_grouping": "Engagement",
        "description": "Captures whether a speaker appears to “hedge” their statement and express lack of certainty; e.g., a score of 1 is assigned if hedge phrases (”I think,” “a little,” “maybe,” “possibly”) are present, and a score of 0 is assigned otherwise.",
        "references": "(Ranganath et al., 2013; (Danescu-Niculescu-Mizil et al., 2013; Islam et al., 2020)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Hedge"
      },
      "TextBlob Subjectivity": {
        "columns": ["textblob_subjectivity"],
        "file": "textblob_subjectivity_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "The extent to which a statement is “subjective” (containing personal information) or “objective” (containing factual information), as measured by TextBlob. Ranges from 0 (objective) to 1 (subjective).",
        "references": "(Cao et al., 2021)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-TextBlob-Sentiment-Analysis-Features"
      },
      "TextBlob Polarity": {
        "columns": ["textblob_polarity"],
        "file": "textblob_polarity_features.py",
        "level": "Chat",
        "semantic_grouping": "Emotion",
        "description": "The extent to which a statement is positive or negative; ranges from -1 (negative) to 1 (positive); neutrality is assigned a score of 0.",
        "references": "(Cao et al., 2021)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-TextBlob-Sentiment-Analysis-Features"
      },
      "Positivity Z-Score": {
        "columns": ["positivity_zscore_chats", "positivity_zscore_conversation"],
        "file": "positivity_zscore_features.py",
        "level": "Chat",
        "semantic_grouping": "Emotion",
        "description": "The relative extent to which an utterance is more (or less) positive, compared to other messages. Here, we use the BERT-assigned positivity score, and calculate two flavors of the z-score: the first scores the messages with respect to other messages in the same conversation; the second scores the messages with respect to all messages in the data.",
        "references": "(Tausczik & Pennebaker, 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/E.24-Positivity-(and-Positivity-z%E2%80%90score)"
      },
      "Dale-Chall Score": {
        "columns": ["dale_chall_score", "dale_chall_classification"],
        "file": "dale_chall_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "The reading level of the utterance, as calculated by the Dale-Chall Score.",
        "references": "(Cao et al., 2021)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.18-Readability"
      },
      "Time Difference": {
        "columns": ["time_diff"],
        "file": "time_difference_features.py",
        "level": "Chat",
        "semantic_grouping": "Pace",
        "description": "The response time between successive utterances.",
        "references": "(Reichel et al., 2015)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.13-Temporal-Features"
      },
      "Politeness Strategies": {
        "columns": [
          "please",
          "please_start",
          "hashedge",
          "indirect_btw",
          "hedges",
          "factuality",
          "deference",
          "gratitude",
          "apologizing",
          "1st_person_pl",
          "1st_person",
          "1st_person_start",
          "2nd_person",
          "2nd_person_start",
          "indirect_greeting",
          "direct_question",
          "direct_start",
          "haspositive",
          "hasnegative",
          "subjunctive",
          "indicative"
        ],
        "file": "politeness_strategies_features.py",
        "level": "Chat",
        "semantic_grouping": "Engagement",
        "description": "A collection of conversational markers that indicates the use of politeness.",
        "references": "(Danescu-Niculescu-Mizil et al., 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.23-Politeness-(ConvoKit)"
      },
      "Forward Flow": {
        "columns": ["forward_flow"],
        "file": "forward_flow_features.py",
        "level": "Chat",
        "semantic_grouping": "Variance",
        "description": "The extent to which a conversation “flows forward” — that is, evolves to new topics over time. The forward flow of a given message is the cosine similarity between the SBERT vector of the current message and the average SBERT vector of all previous messages. In other words, it captures how similar a message is to everything that has come before (so far).",
        "references": "(Gray et al., 2019)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.31-Forward-Flow"
      },
      "Certainty": {
        "columns": ["certainty_rocklage"],
        "file": "certainty_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "The extent to which a message expresses (un)certainty, as evaluated on a 1-9 scale. Very certain messages (e.g., “I am absolutely sure”) are higher on the scale; very uncertain messages (”I do not know for certain…”) are lower on the scale.",
        "references": "(Rocklage et al., 2023)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Certainty"
      },
      "Equal Participation": {
        "columns": [
          "gini_coefficient_sum_num_words",
          "gini_coefficient_sum_num_chars",
          "gini_coefficient_sum_num_messages"
        ],
        "file": "equal_participation_features.py",
        "level": "Conversation",
        "semantic_grouping": "Equality",
        "description": "The extent to which each participant in a conversation engages equally, as measured by a Gini coefficient. We calculate three flavors of Gini coefficient, using the number of words, number of characters, and the number of messages, respectively.",
        "references": "(Tausczik & Pennebaker, 2013)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/E.24-Equal-Participation"
      },
      "Discursive Diversity": {
        "columns": [
          "discursive_diversity",
          "variance_in_DD",
          "incongruent_modulation",
          "within_person_disc_range"
        ],
        "file": "discursive_diversity_features.py",
        "level": "Conversation",
        "semantic_grouping": "Variance",
        "description": "Calculates metrics related to the extent to which members in a conversation speak similarly. 1. Discursive diversity: 1 - the average pairwise cosine distances between the centroids associated with each speaker in a conversation. 2. Variance in discursive diversity: the extent to which discursive diversity varies across the beginning, middle, and end of a conversation. 3. Incongruent modulation: the total variance, per speaker, between the (beginning, middle) and (middle, end) of a conversation. As described by the pape, this is the “team-level variance in members’ within-person discursive range” from stage 1 to stage 2, and from stage 2 to stage 3. 4. Within-person discursive range: The sum, across all speakers in the conversation, of each speaker’s average distance between their centroids for the (beginning, middle) and (middle, end) of a conversation.",
        "references": "(Lix et al., 2022)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/E.-25-Discursive-Diversity-Metrics"
      },
      "Turn-Taking Index": {
        "columns": ["turn_taking_index"],
        "file": "turn_taking_features.py",
        "level": "Conversation",
        "semantic_grouping": "Equality",
        "description": "Calculates a metric describing the extent to which individuals take turns speaking in a conversation. Adapted from Almaatouq et al. (2023), in which we treat each separate chat as equivalent to an in-game “solution”: ”A group’s turn-taking index for a given round is measured by dividing the number of turns taken … by the total number of [chats] on a particular task instance.”",
        "references": "(Almaatouq et al., 2023)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Turn%E2%80%90Taking"
      },
      "Online Discussion Tags": {
        "columns": [
          "num_all_caps",
          "num_links",
          "num_reddit_users",
          "num_emphasis",
          "num_bullet_points",
          "num_numbered_points",
          "num_quotes",
          "num_block_quote_responses",
          "num_ellipses",
          "num_parentheses",
          "num_emoji"
        ],
        "file": "online_discussion_tags_features.py",
        "level": "Chat",
        "semantic_grouping": "Content",
        "description": "Calculates a number of metrics specific to communications in an online setting: 1. Num all caps: Number of words that are in all caps 2. Num links: Number of links to external resources 3. Num Reddit Users: Number of usernames referred to, in u/RedditUser format. 4. Num Emphasis: The number of times someone used **emphasis** in their message 5. Num Bullet Points: The number of bullet points used in a message. 6. Num Line Breaks: The number of line breaks in a message. 7. Num Quotes: The number of “quotes” in a message. 8. Num Block Quotes Responses: The number of times someone uses a block quote (”>”), indicating a longer quotation 9. Num Ellipses: The number of times someone uses ellipses (…) in their message 10. Num Parentheses: The number of sets of fully closed parenthetical statements in a message 11. Num Emoji: The number of emoticons in a message, e.g., “:)”",
        "references": "New",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Reddit-Tags"
      },
      "Politeness / Receptiveness Markers": {
        "columns": [
          "Impersonal_Pronoun",
          "First_Person_Single",
          "Hedges",
          "Negation",
          "Subjectivity",
          "Negative_Emotion",
          "Reasoning",
          "Agreement",
          "Second_Person",
          "Adverb_Limiter",
          "Disagreement",
          "Acknowledgement",
          "First_Person_Plural",
          "For_Me",
          "WH_Questions",
          "YesNo_Questions",
          "Bare_Command",
          "Truth_Intensifier",
          "Apology",
          "Ask_Agency",
          "By_The_Way",
          "Can_You",
          "Conjunction_Start",
          "Could_You",
          "Filler_Pause",
          "For_You",
          "Formal_Title",
          "Give_Agency",
          "Affirmation",
          "Gratitude",
          "Hello",
          "Informal_Title",
          "Let_Me_Know",
          "Swearing",
          "Reassurance",
          "Please",
          "Positive_Emotion",
          "Goodbye",
          "Token_count"
        ],
        "file": "politeness_receptiveness_markers_features.py",
        "level": "Chat",
        "semantic_grouping": "Engagement",
        "description": "A collection of conversational markers that indicates the use of politeness / receptiveness.",
        "references": "(Yeomans et al., 2020)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Politeness-V2"
      },
      "Team Burstiness": {
        "columns": ["team_burstiness"],
        "file": "burstiness_features.py",
        "level": "Conversation",
        "semantic_grouping": "Pace",
        "description": "This conversation-level feature measures the level of burstiness of chats in a conversation. The metric takes a value between -1 and 1, with a higher value indicating higher levels of team burstiness. Teams with higher burstiness would have more spiked patterns in team activity, which tends to indicate a higher sense of responsiveness and connectedness within the team members.",
        "references": "(Reidl and Wooley, 2017)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Team-Burstiness"
      },
      "Information Diversity": {
        "columns": ["info_diversity"],
        "file": "information_diversity_features.py",
        "level": "Conversation",
        "semantic_grouping": "Variance",
        "description": "This conversation-level feature uses topic modeling to measure the level of information diversity across a conversation. We first preprocess the data with lowercasing, lemmatization, removing stop words, and removing short words (less than length 3). We then use the gensim package to create an LDA Model for each conversation, generating a corresponding topic space with its number of dimensions = num_topics. To determine the number of topics used, we use a logarithmic scale relative to the number of chats in the conversation. A team's info diversity is then computed by looking at the average cosine dissimilarity between each chat's topic vector and the mean topic vector across the entire conversation. The value ranges between 0 and 1, with higher values indicating a higher level of information diversity/diversity in topics discussed throughout the conversation. As discussed in the paper above, typical info diversity values are quite small, with the paper having a mean score of 0.04 and standard deviation of 0.05.",
        "references": "(Reidl and Wooley, 2017)",
        "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/Information-Diversity"
      }
    }

  feature_methods_chat = {
      "Positivity (BERT)": ChatLevelFeaturesCalculator.concat_bert_features,
      "Message Length": ChatLevelFeaturesCalculator.text_based_features,
      "Message Quantity": ChatLevelFeaturesCalculator.text_based_features,
      "Information Exchange": ChatLevelFeaturesCalculator.info_exchange,
      "LIWC and Other Lexicons": ChatLevelFeaturesCalculator.lexical_features,
      "Questions": ChatLevelFeaturesCalculator.other_lexical_features,
      "Conversational Repair": ChatLevelFeaturesCalculator.other_lexical_features,
      "Word Type-Token Ratio": ChatLevelFeaturesCalculator.other_lexical_features,
      "Proportion of First-Person Pronouns": ChatLevelFeaturesCalculator.other_lexical_features,
      "Function Word Accommodation": ChatLevelFeaturesCalculator.calculate_word_mimicry,
      "Content Word Accommodation": ChatLevelFeaturesCalculator.calculate_word_mimicry,
      "(BERT) Mimicry": ChatLevelFeaturesCalculator.calculate_word_mimicry,
      "Moving Mimicry": ChatLevelFeaturesCalculator.calculate_word_mimicry,
      "Hedge": ChatLevelFeaturesCalculator.calculate_hedge_features,
      "TextBlob Subjectivity": ChatLevelFeaturesCalculator.calculate_textblob_sentiment,
      "TextBlob Polarity": ChatLevelFeaturesCalculator.calculate_textblob_sentiment,
      "Positivity Z-Score": ChatLevelFeaturesCalculator.positivity_zscore,
      "Dale-Chall Score": ChatLevelFeaturesCalculator.get_dale_chall_score_and_classfication,
      "Time Difference": ChatLevelFeaturesCalculator.get_temporal_features,
      "Politeness Strategies": ChatLevelFeaturesCalculator.calculate_politeness_sentiment,
      "Politeness / Receptiveness Markers": ChatLevelFeaturesCalculator.calculate_politeness_v2,
      "Forward Flow": ChatLevelFeaturesCalculator.get_forward_flow,
      "Certainty": ChatLevelFeaturesCalculator.get_certainty_score,
      "Online Discussion Tags": ChatLevelFeaturesCalculator.get_reddit_features
  }

  feature_methods_conv = {
      "Turn-Taking Index": ConversationLevelFeaturesCalculator.get_turn_taking_features,
      "Equal Participation": ConversationLevelFeaturesCalculator.get_gini_features,
      "Conversation Level Aggregates": ConversationLevelFeaturesCalculator.get_conversation_level_aggregates,
      "User Level Aggregates": ConversationLevelFeaturesCalculator.get_user_level_aggregates,
      "Discursive Diversity": ConversationLevelFeaturesCalculator.get_discursive_diversity_features,
      "Team Burstiness": ConversationLevelFeaturesCalculator.calculate_team_burstiness,
      "Information Diversity": ConversationLevelFeaturesCalculator.calculate_info_diversity
  }

  # combine feature_methods_chat and feature_methods_conv
  feature_methods_dicts = {**feature_methods_chat, **feature_methods_conv}

  # add them to a combined dictionary
  for feat in features.keys():
    features[feat]["function"] = feature_methods_dicts[feat]

  # save the features 
  with open('features.pkl', 'wb') as file:
      pickle.dump(features, file)
