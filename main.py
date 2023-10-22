# This is main file to read the csv files, and call other files, and for outputs
import pandas as pd
import csv
import normalizations


def contains_comma(series):
    """Check if a pandas Series contains comma-separated values."""
    return series.str.contains(',').any()


# Reading the input csv file and the dependencies text file
input_file = pd.read_csv('exampleInputTable.csv')
with open('dependencies.txt', 'r') as file:
    input_dependencies = file.read()

# Input from the user
max_normalization = input(
    'Please enter the highest desired level of normalization: ')

input_file = input_file.astype(str)
columns_with_commas = [
    col for col in input_file.columns if contains_comma(input_file[col])]
print(columns_with_commas)
for col in columns_with_commas:
    input_file[col] = input_file[col].str.split(
        ',').apply(lambda x: [item.strip() for item in x])

one_nf_table, one_flag = normalizations.first_normalization_form(input_file)
print(one_nf_table)
print(one_flag)
