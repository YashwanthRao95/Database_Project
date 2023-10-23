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


def is_2nf(relation, primary_key, dependencies):
    partial_dependencies_not_found = True
    for determinant, dependent in dependencies.items():
        if {determinant}.issubset(primary_key) and {determinant} != set(primary_key):
            partial_dependencies_not_found = False
            break

    return partial_dependencies_not_found


def is_3nf(relations, primary_key, dependencies):
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
    two_flag = is_2nf(relation, primary_key, dependencies)

    if two_flag:
        return relation, two_flag
    else:
        print('RELATIONS AFTER 2NF')
        for determinant, dependent in dependencies.items():
            cols = [determinant] + dependent
            relations[determinant] = relation[cols].drop_duplicates(
            ).reset_index(drop=True)
            print(relations[determinant])
        print('\n')
        return relations, two_flag


def third_normalization_form(relations, primary_key, dependencies):
    three_relations = {}
    three_flag = is_3nf(relations, primary_key, dependencies)

    if three_flag:
        return relations, three_flag
    else:
        return relations, three_flag
