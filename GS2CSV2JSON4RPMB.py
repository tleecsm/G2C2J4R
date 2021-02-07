# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:18:50 2021

@author: Tanner Lee
https://github.com/tleecsm
"""

import pandas
import random

GOOGLE_SHEETS = r'https://docs.google.com/spreadsheets/d/e/2PACX-1vRXfifiTT4f-Y5hVgy4202yTpV3A2oig6UXNXFNxuus2yfev5tu_G0EIlXyWhT6PDHb5KbCDdKE3pYx/pub?output=csv'

OUTPUT_FILE = "output.json"

# Bingo board is 5 x 5
# Therefore we need to base everything on 25 elements
BOARD_SIZE = 25

###############################################################################
#               GRAB THE DATA AND FORMAT IT AS USABLE DATA                    #
###############################################################################

dataframe = pandas.read_csv(GOOGLE_SHEETS, encoding='utf8')
headers = [h for h in dataframe]
data = {}
for header in headers:
    current_column = dataframe[header].dropna()
    data[header] = [element for element in current_column]

category_selection = []
for i in range(BOARD_SIZE):
    category_selection.extend(headers)
    
print(data)
    
###############################################################################
#             GENERATE THE ELEMENTS THAT WILL GO ON THE BOARD                 #
###############################################################################

board_elements = []
while len(board_elements) < BOARD_SIZE:
    # Start by selecting a category
    category_index = random.randint(0, len(category_selection)-1)
    # Remove the category after it is selected
    # This will reduce the likelyhood that it is selected again
    category = category_selection.pop(category_index)
    
    if len(data[category]) == 0:
        # If there are no elements left in this category, remove it
        category_selection = [h for h in category_selection if h != category]
        continue
    
    element_index = random.randint(0, dataframe[category].count()-1)
    current_element = data[category][element_index]
    # Ensure the element we have picked is unique
    if current_element in board_elements:
        continue
    board_elements.append(current_element)

###############################################################################
#                      CONVERT THE BOARD ELEMENTS TO JSON                     #
###############################################################################

with open(OUTPUT_FILE, 'w') as f:
    output_string = '[ '
    for element in board_elements:
        output_string += f'{{"name": "{element}"}},'
    output_string = output_string[:-1] + ' ]'
    f.write(output_string)
