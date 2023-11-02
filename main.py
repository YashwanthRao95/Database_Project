# This is main file to read the csv files, and call other files, and for outputs
import pandas as pd
import csv
import normalizations
import input_parser
from output_generator import output_1NF, output_2_3, output_BCNF_4_5


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
    'Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF): ')
if max_normalization in ["1", "2", "3", "4", "5"]:
    max_normalization = int(max_normalization)

# Find the highest normal form of the input relation
find_high_nf = int(
    input('Find the highest normal form of the input table? (1: Yes, 2: No): '))
high_nf = 'Not normalized yet to any normal form'

# Enter Key
primary_key = input(
    "Enter Primary Key values separated by comma: ").split(', ')
print('\n')

keys = ()
for key in primary_key:
    keys = keys + (key,)

primary_key = keys

mvd_dependencies = {}
if not max_normalization == 'B' and max_normalization >= 4:
    with open('mvd_dependencies.txt', 'r') as file:
        mvd_lines = [line.strip() for line in file]

    print(mvd_lines)

    for mvd in mvd_lines:
        determinant, dependent = mvd.split(" ->> ")
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
        input_file, primary_key)

    if one_flag:
        high_nf = 'Highest Normal Form of input table is: 1NF'

    if max_normalization == 1:
        if one_flag:
            print('Already Normalized to 1NF')
            print('\n')

        print('OUPUT QUERIES AFTER 1NF:')
        print('\n')
        output_1NF(primary_key, one_nf_table)

if max_normalization == 'B' or max_normalization >= 2:
    two_nf_tables, two_flag = normalizations.second_normalization_form(
        one_nf_table, primary_key, dependencies)

    if one_flag and two_flag:
        high_nf = 'Highest Normal Form of input table is: 2NF'

    if max_normalization == 2:
        if two_flag and one_flag:
            print('Already Normalized to 2NF')
            print('\n')

        print('OUPUT QUERIES AFTER 2NF:')
        print('\n')
        output_2_3(two_nf_tables)

if max_normalization == 'B' or max_normalization >= 3:
    three_nf_tables, three_flag = normalizations.third_normalization_form(
        two_nf_tables, primary_key, dependencies)

    if one_flag and two_flag and three_flag:
        high_nf = 'Highest Normal Form of input table is: 3NF'

    if max_normalization == 3:
        if three_flag and two_flag and one_flag:
            print('Already Normalized to 3NF')
            print('\n')

        print('OUPUT QUERIES AFTER 3NF:')
        print('\n')
        output_2_3(three_nf_tables)

if max_normalization == 'B' or max_normalization >= 4:
    bc_nf_tables, bcnf_flag = normalizations.bc_normalization_form(
        three_nf_tables, primary_key, dependencies)

    if one_flag and two_flag and three_flag and bcnf_flag:
        high_nf = 'Highest Normal Form of input table is: BCNF'

    if max_normalization == 'B':
        if bcnf_flag and three_flag and two_flag and one_flag:
            print('Already Normalized to BCNF')
            print('\n')

        print('OUPUT QUERIES AFTER BCNF:')
        print('\n')
        output_2_3(bc_nf_tables)

if not max_normalization == 'B' and max_normalization >= 4:
    four_nf_tables, four_flag = normalizations.fourth_normalization_form(
        bc_nf_tables, mvd_dependencies)

    if one_flag and two_flag and three_flag and bcnf_flag and four_flag:
        high_nf = 'Highest Normal Form of input table is: 4NF'

    if max_normalization == 4:
        if four_flag and bcnf_flag and three_flag and two_flag and one_flag:
            print('Already Normalized to 4NF')
            print('\n')

        print('OUPUT QUERIES AFTER 4NF:')
        print('\n')
        output_2_3(four_nf_tables)

if not max_normalization == 'B' and max_normalization >= 5:
    five_nf_tables, five_flag = normalizations.fivth_normalization_form(
        four_nf_tables, primary_key, dependencies)

    if one_flag and two_flag and three_flag and bcnf_flag and four_flag and five_flag:
        high_nf = 'Highest Normal Form of input table is: 5NF'

    if max_normalization == 5:
        if five_flag and four_flag and bcnf_flag and three_flag and two_flag and one_flag:
            print('Already Normalized to 5NF')
            print('\n')

        print('OUPUT QUERIES AFTER 5NF:')
        print('\n')
        output_BCNF_4_5(five_nf_tables)

if find_high_nf == 1:
    print('\n')
    print(high_nf)
    print('\n')
