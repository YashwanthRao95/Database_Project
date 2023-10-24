# This file is used for all the normalizations
# A function to check if an item is a list or a set
def is_list_or_set(item):
    return isinstance(item, (list, set))


def is_1nf(relation):
    if relation.empty:
        return False

    # Check if each column has atomic values and values are of the same type
    for column in relation.columns:
        unique_types = relation[column].apply(type).nunique()
        if unique_types > 1:
            return False

        # Check for non-atomic values like list, dict, or set within the columns
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
    i = 0
    keys_as_list = list(dependencies.keys())
    for relation in relations:
        attributes = set(relations[relation].columns)
        non_prime_attributes = attributes - set(keys_as_list[i])
        i += 1

        for determinant, dependents in dependencies.items():
            if all(attr in non_prime_attributes for attr in determinant):
                for dependent in dependents:
                    if dependent in non_prime_attributes:
                        return False
    return True


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
    two_flag = is_2nf(primary_key, dependencies)

    if two_flag:
        relations[primary_key] = relation
        return relations, two_flag
    else:
        print('RELATIONS AFTER 2NF')
        for determinant, dependent in dependencies.items():
            cols = list(determinant) + dependent
            relations[tuple(determinant)] = relation[cols].drop_duplicates(
            ).reset_index(drop=True)
            print(relations[determinant])
            print('\n')
        return relations, two_flag


def third_normalization_form(relations, primary_key, dependencies):
    three_relations = {}
    three_flag = is_3nf(relations, dependencies)

    if three_flag:
        return relations, three_flag
    else:
        print('RELATIONS AFTER 3NF')
        for relation in relations:
            for determinant, dependent in dependencies.items():
                cols = list(determinant) + dependent
                three_relations[tuple(determinant)] = relations[relation][cols].drop_duplicates(
                ).reset_index(drop=True)
                print(three_relations[determinant])
                print('\n')

        return three_relations, three_flag
