"""
file: featurize.py
---
This file is the main driver of the feature generating pipeline. 
It instantiates and calls the FeatureBuilder class which defines the logic used for feature creation.
"""

# Importing the Feature Generating Class
from feature_builder import FeatureBuilder
import pandas as pd
import chardet

# Main Function
if __name__ == "__main__":

	# detects CSV encoding of our datasets
	with open("../feature_engine/testing/data/cleaned_data/test_chat_level.csv", 'rb') as file:
		chat_encoding = chardet.detect(file.read())

	with open("../feature_engine/testing/data/cleaned_data/test_conv_level.csv", 'rb') as file:
		conv_encoding = chardet.detect(file.read())

	chat_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_chat_level.csv", encoding=chat_encoding['encoding'])
	conv_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_conv_level.csv", encoding=conv_encoding['encoding'])
	tiny_juries_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/test_data/juries_tiny_for_testing.csv", encoding='utf-8')
	tiny_multi_task_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/test_data/multi_task_TINY.csv", encoding='utf-8')
	tiny_multi_task_renamed_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/test_data/multi_task_TINY_cols_renamed.csv", encoding='utf-8')
	juries_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/jury_conversations_with_outcome_var.csv", encoding='utf-8')
	csop_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/csop_conversations_withblanks.csv", encoding='utf-8')
	csopII_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/csopII_conversations_withblanks.csv", encoding='utf-8')
	
	# TINY / TEST DATASETS -------------------------------#
	
	# # Tiny Juries
	# tiny_juries_feature_builder = FeatureBuilder(
	# 	input_df = tiny_juries_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/jury_TINY_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/jury_TINY_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/jury_TINY_output_conversation_level.csv",
	# 	turns = False,
	# )
	# feature_builder.featurize(col="message")

	# # Tiny multi-task
	# tiny_multi_task_feature_builder = FeatureBuilder(
	# 	input_df = tiny_multi_task_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/multi_task_TINY_output_chat_level_stageId_cumulative.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/multi_task_TINY_output_user_level_stageId_cumulative.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/multi_task_TINY_output_conversation_level_stageId_cumulative.csv",
	# 	turns = False,
	# 	conversation_id = "stageId",
	# 	cumulative_grouping = True
	# )
	# tiny_multi_task_feature_builder.featurize(col="message")

	"""
	Testing Package Task 1
	---
	In this test, we simply test the functionaality of everything after we rename everything ("Case 1").
	Here, we use a test dataset that has a different conversation ID, speaker ID, message column, and timestamp
	column compared to the defaults, and ensure that nothing breaks.
	"""
	testing_package_task_1 = FeatureBuilder(
		input_df = tiny_multi_task_renamed_df,
		conversation_id_col = "roundId",
		speaker_id_col = "speakerId",
		message_col = "text",
		timestamp_col = "time",
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/tiny_multi_task_PT1_level_chat.csv",
		output_file_path_user_level = "../feature_engine/output/user/tiny_multi_task_PT1_level_user.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/tiny_multi_task_PT1_level_conv.csv",
		turns = False,
	)
	testing_package_task_1.featurize(col="message")

	"""
	Testing Package Task 1 Advanced Features
	---
	In this test, we test the functionality of the advanced grouping features.
	
	"Case 2": .ngroup() feature
	- Group by ["gameId", "roundId", "stageId"] and assert that the number of groupings matches
		the stageId (which will confirm that it worked)

	"Case 3": Complex hieararchical grouping
	- ID: stageID; cumulative: True, within_task: False
	- ID: stageID; cumulative: True; within_task: True
	- ID: roundID; cumulative: True, within_task: True

	Improper examples:
	- grouping keys: ["roundID", "stageID"], ID: "gameID"
	"""
	testing_case_2 = FeatureBuilder(
		input_df = tiny_multi_task_renamed_df,
		conversation_id_col = "roundId",
		speaker_id_col = "speakerId",
		message_col = "text",
		timestamp_col = "time",
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/tiny_multi_task_case2_level_chat.csv",
		output_file_path_user_level = "../feature_engine/output/user/tiny_multi_task_case2_level_user.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/tiny_multi_task_case2_level_conv.csv",
		turns = False,
	)
	testing_case_2.featurize(col="message")



	# # testing chat features
	# testing_chat = FeatureBuilder(
	# 	input_df = chat_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/test_chat_level_chat.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/test_chat_level_user.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/test_chat_level_conv.csv",
	# 	turns = False,
	# )
	# testing_chat.featurize(col="message")

	# # testing conv features
	# testing_conv = FeatureBuilder(
	# 	input_df = conv_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/test_conv_level_chat.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/test_conv_level_user.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/test_conv_level_conv.csv",
	# 	turns = False,
	# )
	# testing_conv.featurize(col="message")

	# FULL DATASETS BELOW ------------------------------------- #
	
	# Juries
	# jury_feature_builder = FeatureBuilder(
	# 	input_df = juries_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/jury_output_chat_level.csv",
	# 	# output_file_path_chat_level = "",
	# 	output_file_path_user_level = "../feature_engine/output/user/jury_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/jury_output_conversation_level.csv",
	# 	turns = True
	# )
	# jury_feature_builder.featurize(col="message")

	# # CSOP (Abdullah)
	# csop_feature_builder = FeatureBuilder(
	# 	input_df = csop_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/csop_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/csop_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/csop_output_conversation_level.csv",
	# 	turns = True
	# )
	# csop_feature_builder.featurize(col="message")


	# # CSOP II (Nak Won Rim)
	# csopII_feature_builder = FeatureBuilder(
	# 	input_df = csopII_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/csopII_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/csopII_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/csopII_output_conversation_level.csv",
	# 	turns = True
	# )
	# csopII_feature_builder.featurize(col="message")
