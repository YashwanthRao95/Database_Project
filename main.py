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
max_normalization = input(
    'Please enter the highest desired level of normalization (1, 2, 3, B, 4, or 5): ')
if max_normalization in ["1", "2", "3", "4", "5"]:
    max_normalization = int(max_normalization)

# Enter Key
primary_key = input(
    "Enter Primary Key values separated by comma: ").split(', ')
print('\n')

keys = ()
for key in primary_key:
    keys = keys + (key,)

primary_key = keys

mvd_dependencies = {}
if max_normalization >= 4:
    with open('mvd_dependencies.txt', 'r') as file:
        mvd_lines = [line.strip() for line in file]

    print(mvd_lines)

    for mvd in mvd_lines:
        determinant, dependent = mvd.split(" ->-> ")
        determinant = determinant.split(
            ", ") if ", " in determinant else [determinant]
        determinant_str = str(determinant)
        if determinant_str in mvd_dependencies:
            mvd_dependencies[determinant_str].append(dependent)
        else:
            mvd_dependencies[determinant_str] = [dependent]

    print('MULTI-VALUED DEPENDENCIES')
    print(mvd_dependencies)
    print('\n')

input_file = input_parser.input_parser(input_file)

if max_normalization == 'B' or max_normalization >= 1:
    one_nf_table, one_flag = normalizations.first_normalization_form(
        input_file)

    if one_flag and max_normalization == 1:
        print('Already Normalized to 1NF')

if max_normalization == 'B' or max_normalization >= 2:
    two_nf_tables, two_flag = normalizations.second_normalization_form(
        one_nf_table, primary_key, dependencies)

    if two_flag and one_flag and max_normalization == 2:
        print('Already Normalized to 2NF')

if max_normalization == 'B' or max_normalization >= 3:
    three_nf_tables, three_flag = normalizations.third_normalization_form(
        two_nf_tables, primary_key, dependencies)

    if three_flag and two_flag and one_flag and max_normalization == 3:
        print('Already Normalized to 3NF')

if max_normalization == 'B' or max_normalization >= 4:
    bc_nf_tables, bcnf_flag = normalizations.bc_normalization_form(
        three_nf_tables, primary_key, dependencies)

    if bcnf_flag and three_flag and two_flag and one_flag and max_normalization == 'B':
        print('Already Normalized to BCNF')

if not max_normalization == 'B' and max_normalization >= 4:
    four_nf_tables, four_flag = normalizations.fourth_normalization_form(
        bc_nf_tables, mvd_dependencies)

    if four_flag and bcnf_flag and three_flag and two_flag and one_flag and max_normalization == 4:
        print('Already Normalized to 4NF')

if not max_normalization == 'B' and max_normalization >= 5:
    five_nf_tables, five_flag = normalizations.fivth_normalization_form(
        four_nf_tables, primary_key, dependencies)

    if five_flag and four_flag and bcnf_flag and three_flag and two_flag and one_flag and max_normalization == 5:
        print('Already Normalized to 5NF')
