import numpy as np

# feature extraction
def extract_price_action_features(lows, highs):
    # find indices of structure highs (i.e., highest values in each consecutive sub-sequence)
    structure_highs_indices = np.argwhere(np.diff(np.sign(highs - np.roll(highs, 1))) < 0).flatten()

    # find indices of structure lows (i.e., lowest values in each consecutive sub-sequence)
    structure_lows_indices = np.argwhere(np.diff(np.sign(lows - np.roll(lows, 1))) > 0).flatten()

    # if high indices are consecutive, just take the last one
    structure_highs_consecutive_indices = np.where(np.diff(structure_highs_indices) == 1)[0]
    structure_highs_indices = structure_highs_indices[structure_highs_consecutive_indices + 1]

    # if low indices are consecutive, just take the last one
    structure_lows_consecutive_indices = np.where(np.diff(structure_lows_indices) == 1)[0]
    structure_lows_indices = structure_lows_indices[structure_lows_consecutive_indices + 1]

    # get the corresponding peak values using the structure highs indices
    structure_highs = highs[structure_highs_indices]

    # get the corresponding peak values using the structure lows indices
    structure_lows = lows[structure_lows_indices]

    # get the last two structure highs indices
    last_two_structure_highs_indices = structure_highs_indices[-2:]

    # get the last two structure lows indices
    last_two_structure_lows_indices = structure_lows_indices[-2:]

    # loop through structures to get the last 3 structures
    structure_index_1, structure_index_2, structure_index_3 = None, None, None
    structure_value_1, structure_value_2, structure_value_3 = None, None, None
    structure_1_is, structure_2_is, structure_3_is = None, None, None
    for i in range(1, -1, -1): # loop backwards, starting from the second index which is 1, looping back to 0
        while True:
            # loop status
            new_loop = True

            # get structure indices
            high_index = last_two_structure_highs_indices[i]
            low_index = last_two_structure_lows_indices[i]

            # get structure values
            high = highs[high_index]
            low = lows[low_index]
            
            # check if last structure is a high / low, or a combination of both
            if structure_3_is == None and new_loop == True:
                new_loop = False
                if high_index == low_index:
                    structure_3_is = 'both'
                    structure_2_is = 'both'
                    structure_value_3 = high
                    structure_value_2 = low
                    structure_index_3 = high_index
                    structure_index_2 = low_index
                elif high_index > low_index:
                    structure_3_is = 'high'
                    structure_value_3 = high
                    structure_index_3 = high_index
                elif low_index > high_index:
                    structure_3_is = 'low'
                    structure_value_3 = low
                    structure_index_3 = low_index
            
            # check if 1st from last structure is a high / low, or a combination of both
            if structure_2_is == None and new_loop == True:
                new_loop = False
                if high_index == low_index:
                    structure_2_is = 'both'
                    structure_1_is = 'both'
                    structure_value_2 = high
                    structure_value_1 = low
                    structure_index_2 = high_index
                    structure_index_1 = low_index
                elif structure_3_is == 'high':
                    structure_2_is = 'low'
                    index_of_first_low_from_high = [z for z in last_two_structure_lows_indices if z < structure_index_3][-1]
                    structure_value_2 = lows[index_of_first_low_from_high]
                    structure_index_2 = index_of_first_low_from_high
                elif structure_3_is == 'low':
                    structure_2_is = 'high'
                    index_of_first_high_from_low = [z for z in last_two_structure_highs_indices if z < structure_index_3][-1]
                    structure_value_2 = highs[index_of_first_high_from_low]
                    structure_index_2 = index_of_first_high_from_low
            
            # check if 2nd from last structure is a high / low, or a combination of both
            if structure_1_is == None and new_loop == True:
                new_loop = False
                if structure_2_is == 'both':
                    if high_index == low_index:
                        structure_1_is = 'both'
                        structure_value_1 = high
                        structure_index_1 = high_index
                    elif high_index > low_index:
                        structure_1_is = 'high'
                        structure_value_1 = high
                        structure_index_1 = high_index
                    elif low_index > high_index:
                        structure_1_is = 'low'
                        structure_value_1 = low
                        structure_index_1 = low_index
                elif structure_2_is == 'high':
                    structure_1_is = 'low'
                    index_of_first_low_from_high = [z for z in last_two_structure_lows_indices if z < structure_index_3][-1]
                    structure_value_1 = lows[index_of_first_low_from_high]
                    structure_index_1 = index_of_first_low_from_high
                elif structure_2_is == 'low':
                    structure_1_is = 'high'
                    index_of_first_high_from_low = [z for z in last_two_structure_highs_indices if z < structure_index_3][-1]
                    structure_value_1 = highs[index_of_first_high_from_low]
                    structure_index_1 = index_of_first_high_from_low

            # if we are now on index 0 and structure_1_is == None, repeat the index 0 loop, else break loop
            if i == 0 and structure_1_is == None:
                new_loop = True
            else:
                break

    # gradient calculation ... m = (y2 - y1) / (x2 - x1) ... price is y, indexes are x
    gradient_1 = (structure_value_2 - structure_value_1) / (structure_index_2 - structure_index_1)
    gradient_2 = (structure_value_3 - structure_value_2) / (structure_index_3 - structure_index_2)
    
    # return price action features
    return structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2