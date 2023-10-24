# This is main file to read the csv files, and call other files, and for outputs
import pandas as pd
import csv
import normalizations
import input_parser


# Reading the input csv file and the dependencies text file
input_file = pd.read_csv('exampleInputTable.csv')
print('INPUT RELATION')
print(input_file)
print('\n')

with open('dependencies.txt', 'r') as file:
    lines = [line.strip() for line in file]

dependencies = {}
for line in lines:
    determinant, dependent = line.split(" -> ")
    # Splitting the determinant by comma to make it a list
    determinant = determinant.split(", ")
    dependencies[tuple(determinant)] = dependent.split(", ")
print('DEPENDENCIES')
print(dependencies)
print('\n')
# Input from the user
max_normalization = int(input(
    'Please enter the highest desired level of normalization: '))

# Enter Key
primary_key = input("Enter Primary Key values separated by comma: ").split(',')
print('\n')

keys = ()
for key in primary_key:
    keys = keys + (key,)

primary_key = keys

input_file = input_parser.input_parser(input_file)

if max_normalization >= 1:
    one_nf_table, one_flag = normalizations.first_normalization_form(
        input_file)

    if one_flag and max_normalization == 1:
        print('Already Normalized to 1NF')

if max_normalization >= 2:
    two_nf_tables, two_flag = normalizations.second_normalization_form(
        one_nf_table, primary_key, dependencies)

    if two_flag and one_flag and max_normalization == 2:
        print('Already Normalized to 2NF')

if max_normalization >= 3:
    three_nf_tables, three_flag = normalizations.third_normalization_form(
        two_nf_tables, primary_key, dependencies)

    if three_flag and two_flag and one_flag and max_normalization == 3:
        print('Already Normalized to 3NF')
