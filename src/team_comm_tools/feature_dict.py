from team_comm_tools.utils.calculate_chat_level_features import ChatLevelFeaturesCalculator
from team_comm_tools.utils.calculate_conversation_level_features import ConversationLevelFeaturesCalculator
from team_comm_tools.utils.preprocess import *

from flask import Flask, jsonify
import json

app = Flask(__name__)

from flask import Flask, jsonify
import json

app = Flask(__name__)

feature_dict = { # TODO: customize preprocess methods
    # Chat Level
    "Named Entity Recognition": {
    "columns": ["num_named_entity", "named_entities"],
    "file": "./features/named_entity_recognition_features.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "This feature detects whether a user is talking about (or to) someone else in a conversation.",
    "references": "N/A",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/named_entity_recognition.html",
    "function": ChatLevelFeaturesCalculator.get_named_entity,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Sentiment (RoBERTa)": {
    "columns": ["positive_bert", "negative_bert", "neutral_bert"],
    "file": "./utils/check_embeddings.py",
    "level": "Chat",
    "semantic_grouping": "Emotion",
    "description": "The extent to which a statement is positive, negative, or neutral, as assigned by Cardiffnlp/twitter-roberta-base-sentiment-latest. The total scores (Positive, Negative, Neutral) sum to 1.",
    "references": "(Hugging Face, 2023)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/positivity_bert.html",
    "function": ChatLevelFeaturesCalculator.concat_bert_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": True
  },
  "Message Length": {
    "columns": ["num_words", "num_chars"],
    "file": "./features/basic_features.py",
    "level": "Chat",
    "semantic_grouping": "Quantity",
    "description": "The length of a message in words and characters.",
    "references": "(Ranganath et al., 2013; Cao et al., 2021)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/message_length.html",
    "function": ChatLevelFeaturesCalculator.text_based_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Message Quantity": {
    "columns": ["num_messages"],
    "file": "./features/basic_features.py",
    "level": "Chat", # This was "Conversation, Speaker" in the database
    "semantic_grouping": "Quantity",
    "description": "The total number of messages sent.",
    "references": "(Cao et al., 2021; Marlow et al., 2018, as objective communication frequency)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/message_quantity.html",
    "function": ChatLevelFeaturesCalculator.text_based_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Information Exchange": {
    "columns": [
      "info_exchange_zscore_chats",
      "info_exchange_zscore_conversation"
    ],
    "file": "./features/info_exchange_zscore.py, ./utils/zscore_chats_and_conversation.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "A crude measure of task-focused communication: the total number of words spoken, with the number of first-person pronouns (which suggest self-focus) removed. This value is then z-scored to describe the extent to which a message had more/less task-focused communication relative to other messages. We implement two flavors of the z-score: the first scores the messages with respect to other messages in the same conversation; the second scores the messages with respect to all messages in the data.",
    "references": "(Tausczik & Pennebaker, 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/information_exchange.html#",
    "function": ChatLevelFeaturesCalculator.info_exchange,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "LIWC and Other Lexicons": {
    "columns": [
      "discrepancies_lexical_wordcount",
      "hear_lexical_wordcount",
      "home_lexical_wordcount",
      "conjunction_lexical_wordcount",
      "certainty_lexical_wordcount",
      "inclusive_lexical_wordcount",
      "bio_lexical_wordcount",
      "achievement_lexical_wordcount",
      "adverbs_lexical_wordcount",
      "anxiety_lexical_wordcount",
      "third_person_lexical_wordcount",
      "negation_lexical_wordcount",
      "swear_lexical_wordcount",
      "death_lexical_wordcount",
      "health_lexical_wordcount",
      "see_lexical_wordcount",
      "body_lexical_wordcount",
      "family_lexical_wordcount",
      "negative_affect_lexical_wordcount",
      "quantifier_lexical_wordcount",
      "positive_affect_lexical_wordcount",
      "insight_lexical_wordcount",
      "humans_lexical_wordcount",
      "present_tense_lexical_wordcount",
      "future_tense_lexical_wordcount",
      "past_tense_lexical_wordcount",
      "relative_lexical_wordcount",
      "sexual_lexical_wordcount",
      "inhibition_lexical_wordcount",
      "sadness_lexical_wordcount",
      "social_lexical_wordcount",
      "indefinite_pronoun_lexical_wordcount",
      "religion_lexical_wordcount",
      "work_lexical_wordcount",
      "money_lexical_wordcount",
      "causation_lexical_wordcount",
      "anger_lexical_wordcount",
      "first_person_singular_lexical_wordcount",
      "feel_lexical_wordcount",
      "tentativeness_lexical_wordcount",
      "exclusive_lexical_wordcount",
      "verbs_lexical_wordcount",
      "friends_lexical_wordcount",
      "article_lexical_wordcount",
      "argue_lexical_wordcount",
      "auxiliary_verbs_lexical_wordcount",
      "cognitive_mech_lexical_wordcount",
      "preposition_lexical_wordcount",
      "first_person_plural_lexical_wordcount",
      "percept_lexical_wordcount",
      "second_person_lexical_wordcount",
      "positive_words_lexical_wordcount",
      "first_person_lexical_wordcount",
      "nltk_english_stopwords_lexical_wordcount",
      "hedge_words_lexical_wordcount"
    ],
    "file": "./features/lexical_features_v2.py",
    "level": "Chat",
    "semantic_grouping": ["Content", "Emotion", "Engagement"],
    "description": "The extent to which messages reflect words from a variety of lexicons (predominantly LIWC). Each measure is expressed as a rate of word use per 100 words.",
    "references": "(For LIWC: Niederhoffer & Pennebaker, 2002; Pennebaker et al., 1997; Tausczik & Pennebaker, 2010; for positive words, Hu and Liu (2004); for NLTK English Stopwords: Inspired by Yeomans et al. (2023), which notes the role of stylistic and structural language (e.g., function words), which frequently appear in stopword lists.)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/liwc.html",
    "function": ChatLevelFeaturesCalculator.lexical_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Questions": {
    "columns": ["num_question_naive"],
    "file": "./features/question_num.py",
    "level": "Chat",
    "semantic_grouping": "Engagement",
    "description": "Number of questions asked in an utterance. In the naive version, it counts the number of question marks (’?’).",
    "references": "(Ranganath et al., 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/questions.html",
    "function": ChatLevelFeaturesCalculator.other_lexical_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features, ChatLevelFeaturesCalculator.lexical_features],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Conversational Repair": {
    "columns": ["NTRI"],
    "file": "./features/other_lexical_features.py",
    "level": "Chat",
    "semantic_grouping": "Engagement",
    "description": "A binary indicator of whether an utterance contains a repair indicator, defined as the following: - “what?” - “sorry” - “excuse me” - “huh?” - “who?” - “pardon?” - “say … again?” - “what’s that?” - “what is that”",
    "references": "(Ranganath et al., 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/conversational_repair.html",
    "function": ChatLevelFeaturesCalculator.other_lexical_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features, ChatLevelFeaturesCalculator.lexical_features],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Word Type-Token Ratio": {
    "columns": ["word_TTR"],
    "file": "./features/other_lexical_features.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "The ratio of word types (the total number of unique words in an utterance) to tokens (the total number of words in an utterance).",
    "references": "(Reichel et al., 2015)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/word_ttr.html",
    "function": ChatLevelFeaturesCalculator.other_lexical_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features, ChatLevelFeaturesCalculator.lexical_features],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Proportion of First-Person Pronouns": {
    "columns": ["first_pronouns_proportion"],
    "file": "./features/other_lexical_features.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "The proportion of words in an utterance that are first-person pronouns (e.g., “I,” “me,” “we,” “us”).",
    "references": "(Reichel et al., 2015)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/proportion_of_first_person_pronouns.html",
    "function": ChatLevelFeaturesCalculator.other_lexical_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features, ChatLevelFeaturesCalculator.lexical_features],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Function Word Accommodation": {
    "columns": ["function_word_accommodation"],
    "file": "./features/word_mimicry.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The total number of function words used in a given turn that were also used in the previous turn. Function words are defined as a list of 190 words from the source paper.",
    "references": "(Ranganath et al., 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/function_word_accommodation.html",
    "function": ChatLevelFeaturesCalculator.calculate_word_mimicry,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Content Word Accommodation": {
    "columns": ["content_word_accommodation"],
    "file": "./features/word_mimicry.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The total number of non-function words used in a given turn that were also used in the previous turn, normalized by the inverse document frequency of each content word.",
    "references": "(Ranganath et al., 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/content_word_accommodation.html",
    "function": ChatLevelFeaturesCalculator.calculate_word_mimicry,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "(BERT) Mimicry": {
    "columns": ["mimicry_bert"],
    "file": "./features/word_mimicry.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The cosine similarity of the SBERT vectors between the current utterance and the utterance in the previous turn.",
    "references": "Inspired by accommodation (Matarazzo & Wiens, 1977), language style matching (Tausczik & Pennebaker, 2013) and synchrony (Niederhoffer & Pennebaker, 2002), and implemented in a manner similar to forward flow (Gray et al., 2019)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/mimicry_bert.html",
    "function": ChatLevelFeaturesCalculator.calculate_vector_word_mimicry,
    "dependencies": [],
    "preprocess": [],
    "vect_data": True,
    "bert_sentiment_data": False
  },
  "Moving Mimicry": {
    "columns": ["moving_mimicry"],
    "file": "./features/word_mimicry.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The running average of all BERT Mimicry scores computed so far in a conversation. Captures the extent to which all participants in a conversation mimic each other up until a given point.",
    "references": "Inspired by accommodation (Matarazzo & Wiens, 1977), language style matching (Tausczik & Pennebaker, 2013) and synchrony (Niederhoffer & Pennebaker, 2002), and implemented in a manner similar to forward flow (Gray et al., 2019)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/moving_mimicry.html",
    "function": ChatLevelFeaturesCalculator.calculate_vector_word_mimicry,
    "dependencies": [],
    "preprocess": [],
    "vect_data": True,
    "bert_sentiment_data": False
  },
  "Hedge": {
    "columns": ["hedge_naive"],
    "file": "./features/hedge.py",
    "level": "Chat",
    "semantic_grouping": "Engagement",
    "description": "Captures whether a speaker appears to “hedge” their statement and express lack of certainty; e.g., a score of 1 is assigned if hedge phrases (”I think,” “a little,” “maybe,” “possibly”) are present, and a score of 0 is assigned otherwise.",
    "references": "(Ranganath et al., 2013; (Danescu-Niculescu-Mizil et al., 2013; Islam et al., 2020)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/hedge.html",
    "function": ChatLevelFeaturesCalculator.calculate_hedge_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features, ChatLevelFeaturesCalculator.lexical_features],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "TextBlob Subjectivity": {
    "columns": ["textblob_subjectivity"],
    "file": "./features/textblob_sentiment_analysis.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "The extent to which a statement is “subjective” (containing personal information) or “objective” (containing factual information), as measured by TextBlob. Ranges from 0 (objective) to 1 (subjective).",
    "references": "(Cao et al., 2021)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/textblob_subjectivity.html",
    "function": ChatLevelFeaturesCalculator.calculate_textblob_sentiment,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "TextBlob Polarity": {
    "columns": ["textblob_polarity"],
    "file": "./features/textblob_sentiment_analysis.py",
    "level": "Chat",
    "semantic_grouping": "Emotion",
    "description": "The extent to which a statement is positive or negative; ranges from -1 (negative) to 1 (positive); neutrality is assigned a score of 0.",
    "references": "(Cao et al., 2021)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/textblob_polarity.html",
    "function": ChatLevelFeaturesCalculator.calculate_textblob_sentiment,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Positivity Z-Score": {
    "columns": ["positivity_zscore_chats", "positivity_zscore_conversation"],
    "file": "./utils/zscore_chats_and_conversation.py",
    "level": "Chat",
    "semantic_grouping": "Emotion",
    "description": "The relative extent to which an utterance is more (or less) positive, compared to other messages. Here, we use the BERT-assigned positivity score, and calculate two flavors of the z-score: the first scores the messages with respect to other messages in the same conversation; the second scores the messages with respect to all messages in the data.",
    "references": "(Tausczik & Pennebaker, 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/positivity_z_score.html",
    "function": ChatLevelFeaturesCalculator.positivity_zscore,
    "dependencies": [ChatLevelFeaturesCalculator.concat_bert_features],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": True
  },
  "Dale-Chall Score": {
    "columns": ["dale_chall_score", "dale_chall_classification"],
    "file": "./features/readability.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "The reading level of the utterance, as calculated by the Dale-Chall Score.",
    "references": "(Cao et al., 2021)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/dale_chall_score.html",
    "function": ChatLevelFeaturesCalculator.get_dale_chall_score_and_classfication,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Time Difference": {
    "columns": ["time_diff"],
    "file": "./features/temporal_features.py",
    "level": "Chat",
    "semantic_grouping": "Pace",
    "description": "The response time between successive utterances.",
    "references": "(Reichel et al., 2015)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/time_difference.html",
    "function": ChatLevelFeaturesCalculator.get_temporal_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Politeness Strategies": {
    "columns": [
      "please_politeness_convokit",
      "please_start_politeness_convokit",
      "hashedge_politeness_convokit",
      "indirect_btw_politeness_convokit",
      "hedges_politeness_convokit",
      "factuality_politeness_convokit",
      "deference_politeness_convokit",
      "gratitude_politeness_convokit",
      "apologizing_politeness_convokit",
      "1st_person_pl_politeness_convokit",
      "1st_person_politeness_convokit",
      "1st_person_start_politeness_convokit",
      "2nd_person_politeness_convokit",
      "2nd_person_start_politeness_convokit",
      "indirect_greeting_politeness_convokit",
      "direct_question_politeness_convokit",
      "direct_start_politeness_convokit",
      "haspositive_politeness_convokit",
      "hasnegative_politeness_convokit",
      "subjunctive_politeness_convokit",
      "indicative_politeness_convokit"
    ],
    "file": "./features/politeness_features.py",
    "level": "Chat",
    "semantic_grouping": "Engagement",
    "description": "A collection of conversational markers that indicates the use of politeness.",
    "references": "(Danescu-Niculescu-Mizil et al., 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/politeness_strategies.html",
    "function": ChatLevelFeaturesCalculator.calculate_politeness_sentiment,
    "dependencies": [],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Politeness / Receptiveness Markers": {
    "columns": [
      "Impersonal_Pronoun_receptiveness_yeomans",
      "First_Person_Single_receptiveness_yeomans",
      "Hedges_receptiveness_yeomans",
      "Negation_receptiveness_yeomans",
      "Subjectivity_receptiveness_yeomans",
      "Negative_Emotion_receptiveness_yeomans",
      "Reasoning_receptiveness_yeomans",
      "Agreement_receptiveness_yeomans",
      "Second_Person_receptiveness_yeomans",
      "Adverb_Limiter_receptiveness_yeomans",
      "Disagreement_receptiveness_yeomans",
      "Acknowledgement_receptiveness_yeomans",
      "First_Person_Plural_receptiveness_yeomans",
      "For_Me_receptiveness_yeomans",
      "WH_Questions_receptiveness_yeomans",
      "YesNo_Questions_receptiveness_yeomans",
      "Bare_Command_receptiveness_yeomans",
      "Truth_Intensifier_receptiveness_yeomans",
      "Apology_receptiveness_yeomans",
      "Ask_Agency_receptiveness_yeomans",
      "By_The_Way_receptiveness_yeomans",
      "Can_You_receptiveness_yeomans",
      "Conjunction_Start_receptiveness_yeomans",
      "Could_You_receptiveness_yeomans",
      "Filler_Pause_receptiveness_yeomans",
      "For_You_receptiveness_yeomans",
      "Formal_Title_receptiveness_yeomans",
      "Give_Agency_receptiveness_yeomans",
      "Affirmation_receptiveness_yeomans",
      "Gratitude_receptiveness_yeomans",
      "Hello_receptiveness_yeomans",
      "Informal_Title_receptiveness_yeomans",
      "Let_Me_Know_receptiveness_yeomans",
      "Swearing_receptiveness_yeomans",
      "Reassurance_receptiveness_yeomans",
      "Please_receptiveness_yeomans",
      "Positive_Emotion_receptiveness_yeomans",
      "Goodbye_receptiveness_yeomans",
      "Token_count_receptiveness_yeomans"
    ],
    "file": "./features/politeness_v2.py, ./features/politeness_v2_helper.py, ./features/keywords.py",
    "level": "Chat",
    "semantic_grouping": "Engagement",
    "description": "A collection of conversational markers that indicates the use of politeness / receptiveness.",
    "references": "(Yeomans et al., 2020)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/politeness_receptiveness_markers.html",
    "function": ChatLevelFeaturesCalculator.calculate_politeness_v2,
    "dependencies": [],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Forward Flow": {
    "columns": ["forward_flow"],
    "file": "./features/fflow.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The extent to which a conversation “flows forward” — that is, evolves to new topics over time. The forward flow of a given message is the cosine similarity between the SBERT vector of the current message and the average SBERT vector of all previous messages. In other words, it captures how similar a message is to everything that has come before (so far).",
    "references": "(Gray et al., 2019)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/forward_flow.html",
    "function": ChatLevelFeaturesCalculator.get_forward_flow,
    "dependencies": [],
    "preprocess": [],
    "vect_data": True,
    "bert_sentiment_data": False
  },
  "Certainty": {
    "columns": ["certainty_rocklage"],
    "file": "./features/certainty.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "The extent to which a message expresses (un)certainty, as evaluated on a 1-9 scale. Very certain messages (e.g., “I am absolutely sure”) are higher on the scale; very uncertain messages (”I do not know for certain…”) are lower on the scale.",
    "references": "(Rocklage et al., 2023)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/certainty.html",
    "function": ChatLevelFeaturesCalculator.get_certainty_score,
    "dependencies": [],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
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
    "file": "./features/reddit_tags.py",
    "level": "Chat",
    "semantic_grouping": "Content",
    "description": "Calculates a number of metrics specific to communications in an online setting: 1. Num all caps: Number of words that are in all caps 2. Num links: Number of links to external resources 3. Num Reddit Users: Number of usernames referred to, in u/RedditUser format. 4. Num Emphasis: The number of times someone used **emphasis** in their message 5. Num Bullet Points: The number of bullet points used in a message. 6. Num Line Breaks: The number of line breaks in a message. 7. Num Quotes: The number of “quotes” in a message. 8. Num Block Quotes Responses: The number of times someone uses a block quote (”>”), indicating a longer quotation 9. Num Ellipses: The number of times someone uses ellipses (…) in their message 10. Num Parentheses: The number of sets of fully closed parenthetical statements in a message 11. Num Emoji: The number of emoticons in a message, e.g., “:)”",
    "references": "New",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/online_discussions_tags.html",
    "function": ChatLevelFeaturesCalculator.get_reddit_features,
    "dependencies": [],
    "preprocess": [preprocess_text_lowercase_but_retain_punctuation], # "message_lower_with_punc"
    "vect_data": False,
    "bert_sentiment_data": False
  },
  ### Conversation Level
  "Turn-Taking Index": {
    "columns": ["turn_taking_index"],
    "file": "./features/turn_taking_features.py",
    "level": "Conversation",
    "semantic_grouping": "Equality",
    "description": "Calculates a metric describing the extent to which individuals take turns speaking in a conversation. Adapted from Almaatouq et al. (2023), in which we treat each separate chat as equivalent to an in-game “solution”: ”A group’s turn-taking index for a given round is measured by dividing the number of turns taken … by the total number of [chats] on a particular task instance.”",
    "references": "(Almaatouq et al., 2023)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/turn_taking_index.html",
    "function": ConversationLevelFeaturesCalculator.get_turn_taking_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Equal Participation": {
    "columns": [
      "gini_coefficient_sum_num_words",
      "gini_coefficient_sum_num_chars",
      "gini_coefficient_sum_num_messages"
    ],
    "file": "./utils/gini_coefficient.py",
    "level": "Conversation",
    "semantic_grouping": "Equality",
    "description": "The extent to which each participant in a conversation engages equally, as measured by a Gini coefficient. We calculate three flavors of Gini coefficient, using the number of words, number of characters, and the number of messages, respectively.",
    "references": "(Tausczik & Pennebaker, 2013)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/gini_coefficient.html",
    "function": ConversationLevelFeaturesCalculator.get_gini_features,
    "dependencies": [ChatLevelFeaturesCalculator.text_based_features],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Conversation Level Aggregates": {
    "columns": [], 
    "file": "./utils/summarize_features.py",
    "level": "Conversation",
    "semantic_grouping": "N/A",
    "description": "Aggregation of utterance (chat)-level features at the conversation level",
    "references": "N/A",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features/index.html#features-technical",
    "function": ConversationLevelFeaturesCalculator.get_conversation_level_aggregates,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "User Level Aggregates": {
    "columns": [], 
    "file": "./utils/summarize_features.py, ./features/get_user_network.py, ./features/user_centroids.py",
    "level": "Conversation",
    "semantic_grouping": "N/A",
    "description": "Aggregation of utterance (chat)-level features at the speaker (user) level",
    "references": "N/A",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features/index.html#features-technical",
    "function": ConversationLevelFeaturesCalculator.get_user_level_aggregates,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Discursive Diversity": {
    "columns": [
      "discursive_diversity",
      "variance_in_DD",
      "incongruent_modulation",
      "within_person_disc_range"
    ],
    "file": "./features/get_all_DD_features.py, ./features/discursive_diversity.py, ./features/variance_in_DD.py, ./features/within_person_discursive_range.py",
    "level": "Conversation",
    "semantic_grouping": "Variance",
    "description": "Calculates metrics related to the extent to which members in a conversation speak similarly. 1. Discursive diversity: 1 - the average pairwise cosine distances between the centroids associated with each speaker in a conversation. 2. Variance in discursive diversity: the extent to which discursive diversity varies across the beginning, middle, and end of a conversation. 3. Incongruent modulation: the total variance, per speaker, between the (beginning, middle) and (middle, end) of a conversation. As described by the pape, this is the “team-level variance in members’ within-person discursive range” from stage 1 to stage 2, and from stage 2 to stage 3. 4. Within-person discursive range: The sum, across all speakers in the conversation, of each speaker’s average distance between their centroids for the (beginning, middle) and (middle, end) of a conversation.",
    "references": "(Lix et al., 2022)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/discursive_diversity.html",
    "function": ConversationLevelFeaturesCalculator.get_discursive_diversity_features,
    "dependencies": [],
    "preprocess": [],
    "vect_data": True,
    "bert_sentiment_data": False
  },
  "Team Burstiness": {
    "columns": ["team_burstiness"],
    "file": "./features/burstiness.py",
    "level": "Conversation",
    "semantic_grouping": "Pace",
    "description": "This conversation-level feature measures the level of burstiness of chats in a conversation. The metric takes a value between -1 and 1, with a higher value indicating higher levels of team burstiness. Teams with higher burstiness would have more spiked patterns in team activity, which tends to indicate a higher sense of responsiveness and connectedness within the team members.",
    "references": "(Reidl and Woolley, 2017)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/team_burstiness.html",
    "function": ConversationLevelFeaturesCalculator.calculate_team_burstiness,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  },
  "Information Diversity": {
    "columns": ["info_diversity"],
    "file": "./features/information_diversity.py",
    "level": "Conversation",
    "semantic_grouping": "Variance",
    "description": "This conversation-level feature uses topic modeling to measure the level of information diversity across a conversation. We first preprocess the data with lowercasing, lemmatization, removing stop words, and removing short words (less than length 3). We then use the gensim package to create an LDA Model for each conversation, generating a corresponding topic space with its number of dimensions = num_topics. To determine the number of topics used, we use a logarithmic scale relative to the number of chats in the conversation. A team's info diversity is then computed by looking at the average cosine dissimilarity between each chat's topic vector and the mean topic vector across the entire conversation. The value ranges between 0 and 1, with higher values indicating a higher level of information diversity/diversity in topics discussed throughout the conversation. As discussed in the paper above, typical info diversity values are quite small, with the paper having a mean score of 0.04 and standard deviation of 0.05.",
    "references": "(Reidl and Wooley, 2017)",
    "wiki_link": "https://conversational-featurizer.readthedocs.io/en/latest/features_conceptual/information_diversity.html",
    "function": ConversationLevelFeaturesCalculator.calculate_info_diversity,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  }
}

keys_to_keep = ["columns", "file", "level", "semantic_grouping", "description", "references", "wiki_link"]

filtered_dict = {feature_name: {key: value for key, value in feature_data.items() if key in keys_to_keep}
                 for feature_name, feature_data in feature_dict.items()}

with open('./filtered_dict.json', 'w') as json_file:
  json.dump(filtered_dict, json_file, indent=4)
