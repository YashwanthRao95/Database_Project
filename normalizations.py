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


def first_normalization_form(relation):
    one_flag = is_1nf(relation)

    if one_flag:
        return relation, one_flag
    else:
        for col in relation.columns:
            if relation[col].apply(is_list_or_set).any():
                relation = relation.explode(col)
        return relation, one_flag
