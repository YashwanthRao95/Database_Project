import pandas as pd
from itertools import combinations
import re
# This file is used for all the normalizations


def is_list_or_set(item):
    return isinstance(item, (list, set))


def is_superkey(relation, determinant):
    grouped = relation.groupby(
        list(determinant)).size().reset_index(name='count')
    return not any(grouped['count'] > 1)


def powerset(s):
    x = len(s)
    for i in range(1 << x):
        yield [s[j] for j in range(x) if (i & (1 << j)) > 0]


def bcnf_decomposition(relation, dependencies):
    for determinant, dependents in dependencies.items():
        if set(determinant).issubset(relation.columns) and not is_superkey(relation, determinant):
            dependent_cols = list(determinant) + dependents
            new_relation1 = relation[dependent_cols].drop_duplicates()
            remaining_cols = list(set(relation.columns) - set(dependents))
            new_relation2 = relation[remaining_cols].drop_duplicates()
            return [new_relation1, new_relation2]
    return [relation]


def is_1nf(relation):
    if relation.empty:
        return False

    for column in relation.columns:
        unique_types = relation[column].apply(type).nunique()
        if unique_types > 1:
            return False
        if relation[column].apply(lambda x: isinstance(x, (list, dict, set))).any():
            return False

    return True


def is_2nf(primary_key, dependencies):
    partial_dependencies_not_found = True
    for determinant, dependent in dependencies.items():
        if set(determinant).issubset(primary_key) and set(determinant) != set(primary_key):
            partial_dependencies_not_found = False
            break

    return partial_dependencies_not_found


def is_3nf(relations, dependencies):
    for relation in relations:
        attributes = set(relations[relation].columns)
        non_prime_attributes = attributes - set(relation)

        for determinant, dependents in dependencies.items():
            if all(attr in non_prime_attributes for attr in determinant):
                for dependent in dependents:
                    if dependent in non_prime_attributes:
                        return False
    return True


def is_bcnf(relations, primary_key, dependencies):
    for relation in relations:
        for determinant, dependents in dependencies.items():
            if set(determinant).issubset(relation.columns):
                if not is_superkey(relation, determinant):
                    return False
    return True


def is_4nf(relations, mvd_dependencies):
    for relation in relations:
        for determinant, dependents in mvd_dependencies.items():
            for dependent in dependents:
                if isinstance(determinant, tuple):
                    determinant_cols = list(determinant)
                else:
                    determinant_cols = [determinant]

                if all(col in relation.columns for col in determinant_cols + [dependent]):
                    grouped = relation.groupby(determinant_cols)[
                        dependent].apply(set).reset_index()
                    if len(grouped) < len(relation):
                        print(
                            f"Multi-valued dependency violation: {determinant} ->-> {dependent}")
                        return False

    return True


def is_5nf(relations):
    i = 0
    candidate_keys_dict = {}
    for relation in relations:
        print(relation)
        user_input = input("Enter the candidate keys (e.g., (A, B), (C, D)): ")
        print('\n')
        tuples = re.findall(r'\((.*?)\)', user_input)
        candidate_keys = [tuple(map(str.strip, t.split(','))) for t in tuples]
        candidate_keys_dict[i] = candidate_keys
        i += 1

    print(f'Candidate Keys for tables:')
    print(candidate_keys_dict)
    print('\n')

    j = 0
    for relation in relations:
        candidate_keys = candidate_keys_dict[j]
        j += 1

        data_tuples = [tuple(row) for row in relation.to_numpy()]

        # Function to project the data tuples onto a set of attributes
        def project(data, attributes):
            return {tuple(row[attr] for attr in attributes) for row in data}

        # Function to check if a set of attributes is a superkey
        def is_superkey(attributes):
            for key in candidate_keys:
                if set(key).issubset(attributes):
                    return True
            return False, candidate_keys_dict

        for i in range(1, len(relation.columns)):
            for attrs in combinations(relation.columns, i):
                # If the attributes form a superkey, then they satisfy any join dependency by definition
                if is_superkey(attrs):
                    continue

                # Project the data onto the attributes and their complement
                projected_data = project(data_tuples, attrs)
                complement_attrs = set(relation.columns) - set(attrs)
                complement_data = project(data_tuples, complement_attrs)

                # Join the projected data and check if it is equal to the original data
                joined_data = {(row1 + row2)
                               for row1 in projected_data for row2 in complement_data}
                if set(data_tuples) != joined_data:
                    print("Failed 5NF check for attributes:", attrs)
                    return False, candidate_keys_dict

    return True, candidate_keys_dict


def first_normalization_form(relation):
    one_flag = is_1nf(relation)

    if one_flag:
        return relation, one_flag
    else:
        for col in relation.columns:
            if relation[col].apply(is_list_or_set).any():
                relation = relation.explode(col)

        print('RELATION AFTER 1NF')
        print(relation)
        print('\n')
        return relation, one_flag


def second_normalization_form(relation, primary_key, dependencies):
    relations = {}
    original_relation = relation
    two_flag = is_2nf(primary_key, dependencies)

    if two_flag:
        relations[primary_key] = relation
        return relations, two_flag
    else:
        print('RELATIONS AFTER 2NF')
        dependency_keys = list(dependencies.keys())
        for determinant, dependents in dependencies.items():
            modified_dependents = [
                dep + '_fk' if (dep,) in dependency_keys else dep for dep in dependents]

            cols = list(determinant) + dependents
            relations[tuple(determinant)] = relation[cols].drop_duplicates(
            ).reset_index(drop=True)

            rename_dict = {dep: modified_dep for dep,
                           modified_dep in zip(dependents, modified_dependents)}
            relations[tuple(determinant)].rename(
                columns=rename_dict, inplace=True)

            print(relations[determinant])
            print('\n')

        junction_cols = []
        relation_name = ''
        for relation in relations:
            if set(relation).issubset(primary_key):
                relation_name += "_".join(relation)
                junction_cols.append(relation)

        if len(junction_cols) > 1:
            jun_cols = list(junction_cols)
            cols = [element for tup in jun_cols for element in tup]
            temp_df = original_relation[cols].drop_duplicates(
            ).reset_index(drop=True)

            renamed_cols = [col + '_fk' for col in cols]
            temp_df.columns = renamed_cols + \
                [col for col in temp_df.columns if col not in cols]

            temp_df[relation_name] = range(1, len(temp_df) + 1)
            columns_order = [relation_name] + renamed_cols
            temp_df = temp_df[columns_order]
            relations[relation_name] = temp_df
            print(relations[relation_name])
            print('\n')

        return relations, two_flag


def third_normalization_form(relations, primary_key, dependencies):
    three_relations = {}
    three_flag = is_3nf(relations, dependencies)

    if three_flag:
        return relations, three_flag
    else:
        print('RELATIONS AFTER 3NF')
        dependency_keys = list(dependencies.keys())
        for relation in relations:
            original_relation = relations[relation]
            for determinant, dependents in dependencies.items():
                modified_dependents = [
                    dep + '_fk' if (dep,) in dependency_keys else dep for dep in dependents]

                cols = list(determinant) + dependents
                three_relations[tuple(determinant)] = relations[relation][cols].drop_duplicates(
                ).reset_index(drop=True)

                rename_dict = {dep: modified_dep for dep,
                               modified_dep in zip(dependents, modified_dependents)}
                three_relations[tuple(determinant)].rename(
                    columns=rename_dict, inplace=True)
                print(three_relations[determinant])
                print('\n')

        junction_cols = []
        relation_name = ''
        for relation in three_relations:
            relation_name += "_".join(relation)
            junction_cols.append(relation)

        print(relation_name)

        if len(junction_cols) > 1:
            jun_cols = list(junction_cols)
            cols = [element for tup in jun_cols for element in tup]
            temp_df = original_relation[cols].drop_duplicates(
            ).reset_index(drop=True)

            renamed_cols = [col + '_fk' for col in cols]
            temp_df.columns = renamed_cols + \
                [col for col in temp_df.columns if col not in cols]

            temp_df[relation_name] = range(1, len(temp_df) + 1)
            columns_order = [relation_name] + renamed_cols
            temp_df = temp_df[columns_order]
            three_relations[relation_name] = temp_df
            print(three_relations[relation_name])
            print('\n')

        return three_relations, three_flag


def bc_normalization_form(relations, primary_key, dependencies):
    relations = list(relations.values())
    bcnf_relations = []
    bcnf_flag = is_bcnf(relations, primary_key, dependencies)

    if bcnf_flag:
        return relations, bcnf_flag
    else:
        print('RELATIONS AFTER BCNF')
        for relation in relations:
            bcnf_decomposed_relation = bcnf_decomposition(
                relation, dependencies)
            if len(bcnf_decomposed_relation) == 1:
                bcnf_relations.append(bcnf_decomposed_relation)
            else:
                relations.extend(bcnf_decomposed_relation)

    return bcnf_relations, bcnf_flag


def fourth_normalization_form(relations, mvd_dependencies):
    four_relations = []
    four_flag = is_4nf(relations, mvd_dependencies)

    if four_flag:
        return relations, four_flag
    else:
        print('RELATIONS AFTER 4NF')
        for relation in relations:
            for determinant, dependents in mvd_dependencies.items():
                for dependent in dependents:
                    if isinstance(determinant, tuple):
                        determinant_cols = list(determinant)
                    else:
                        determinant_cols = [determinant]

                    if all(col in relation.columns for col in determinant_cols + [dependent]):
                        # Check for multi-valued dependency
                        grouped = relation.groupby(determinant_cols)[
                            dependent].apply(set).reset_index()
                        if len(grouped) < len(relation):
                            # Decomposition
                            table_1 = relation[determinant_cols +
                                               [dependent]].drop_duplicates()
                            table_2 = relation[determinant_cols + [col for col in relation.columns if col not in [
                                dependent] + determinant_cols]].drop_duplicates()

                            # Update tables list
                            four_relations.extend([table_1, table_2])

                            break
                else:
                    continue
                break
            else:
                four_relations.append(relation)

    if len(four_relations) == len(relations):
        return four_relations  # All tables are in 4NF
    else:
        return fourth_normalization_form(four_relations, mvd_dependencies)


def decompose_5nf(dataframe, candidate_keys):
    # Function to project a DataFrame onto a set of attributes
    def project(df, attributes):
        return df[list(attributes)].drop_duplicates().reset_index(drop=True)

    # Function to check if a decomposition is lossless
    def is_lossless(df, df1, df2):
        common_columns = set(df1.columns) & set(df2.columns)
        if not common_columns:
            return False
        joined_df = pd.merge(df1, df2, how='inner', on=list(common_columns))
        return df.equals(joined_df)

    # Initialize the list of decomposed tables with the original table
    decomposed_tables = [dataframe]

    # Iterate over each candidate key and try to decompose the table
    for key in candidate_keys:
        new_tables = []
        for table in decomposed_tables:
            # If the key is a subset of the table's columns, decompose the table
            if set(key).issubset(set(table.columns)):
                table1 = project(table, key)
                remaining_columns = set(table.columns) - set(key)
                table2 = project(table, remaining_columns | set(key))

                # Check if the decomposition is lossless
                if is_lossless(table, table1, table2):
                    new_tables.extend([table1, table2])
                else:
                    new_tables.append(table)
            else:
                new_tables.append(table)
        decomposed_tables = new_tables

    return decomposed_tables


def fivth_normalization_form(relations, primary_key, dependencies):
    five_relations = []
    five_flag, candidate_keys_dict = is_5nf(relations)

    if five_flag:
        return relations, five_flag
    else:
        print('RELATIONS AFTER 5NF')
        i = 0
        for relation in relations:
            candidate_keys = candidate_keys_dict[i]
            i += 1
            decomposed_relations = decompose_5nf(relation, candidate_keys)
            five_relations.append(decomposed_relations)

    return five_relations, five_flag
