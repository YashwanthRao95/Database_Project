# This file is used to parse the input file and dependencies
def contains_comma(series):
    return series.str.contains(',').any()


def input_parser(input_file):
    input_file = input_file.astype(str)
    columns_with_commas = [
        col for col in input_file.columns if contains_comma(input_file[col])]

    for col in columns_with_commas:
        input_file[col] = input_file[col].str.split(
            ',').apply(lambda x: [item.strip() for item in x])

    return input_file
