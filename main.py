# This is main file to read the csv files, and call other files, and for outputs
import pandas as pd
import csv
import normalizations
import input_parser


# Reading the input csv file and the dependencies text file
input_file = pd.read_csv('exampleInputTable.csv')
with open('dependencies.txt', 'r') as file:
    input_dependencies = file.read()

# Input from the user
max_normalization = int(input(
    'Please enter the highest desired level of normalization: '))

input_file = input_parser.input_parser(input_file)

if max_normalization <= 1:
    one_nf_table, one_flag = normalizations.first_normalization_form(
        input_file)

    if one_flag and max_normalization == 1:
        print('Already Normalized to 1NF')
