import numpy as np
import csv
import pandas as pd

"""
file: turn-taking_features.py
---
Calculates the turn-taking index for each speaker
"""

"""
function: count_turns

Returns the total number of turns for each speaker
"""

"""
@param input_date = a dataframe of conversations, in which each row is one chat
"""

def count_turns(input_data):
    temp_turn_count = 1
    consolidated_actions = []

    start_index = input_data.index[0] + 1
    end_index = len(input_data) + input_data.index[0]

    for turn_index in range(start_index, end_index):

        if input_data["speaker_nickname"][turn_index] == input_data["speaker_nickname"][turn_index - 1]:
            temp_turn_count += 1
        else:
            consolidated_actions.append((input_data["speaker_nickname"][turn_index - 1], temp_turn_count))
            temp_turn_count = 1

        if turn_index == max(range(start_index, end_index)):
            consolidated_actions.append((input_data["speaker_nickname"][turn_index], temp_turn_count))

    assert sum(x[1] for x in consolidated_actions) == len(input_data)

    df_consolidated_actions = pd.DataFrame(columns=["speaker_nickname", "turn_count"], data=consolidated_actions)

    return df_consolidated_actions

"""
function: count_turn_taking_index


Returns the turn-taking index for each speaker
"""

def count_turn_taking_index(input_data):
    if(len(input_data) == 1): # there is only 1 speaker for one row; catch a divide by zero error
        return 0
    else:
        return (len(count_turns(input_data)) - 1) / (len(input_data) - 1)

def get_turn(input_data):
    turn_calculated_2 = input_data.groupby("conversation_num").apply(lambda x : count_turn_taking_index(x)).reset_index().rename(columns={0: "turn_taking_index"})
    return turn_calculated_2
