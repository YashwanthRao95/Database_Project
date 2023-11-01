# This file is used to generate ouput as per reqiurements
def pd2sql(dtype):
    """Function to convert pandas dtype to SQL data type."""
    if "int" in str(dtype):
        return "INT"
    elif "float" in str(dtype):
        return "FLOAT"
    elif "object" in str(dtype):
        return "VARCHAR(255)"
    elif "datetime" in str(dtype):
        return "DATETIME"
    else:
        return "TEXT"


def output_1NF(primary_keys, df):
    table_name = "_".join(primary_keys) + "_table"
    # Start creating the SQL query
    query = f"CREATE TABLE {table_name} (\n"

    # Iterate through the DataFrame columns to create the SQL query
    for column, dtype in zip(df.columns, df.dtypes):
        if column in primary_keys:
            query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
        else:
            query += f"  {column} {pd2sql(dtype)},\n"

    # Remove the last comma and close the query
    query = query.rstrip(',\n') + "\n);"

    print(query)


def output_2_3(relations):
    for relation in relations:
        primary_keys = relation
        primary_keys = (primary_keys,) if isinstance(
            primary_keys, str) else primary_keys
        table_name = "_".join(primary_keys) + '_table'

        relation = relations[relation]

        # Start creating the SQL query
        query = f"CREATE TABLE {table_name} (\n"

        # Iterate through the DataFrame columns to create the SQL query
        for column, dtype in zip(relation.columns, relation.dtypes):
            if column in primary_keys:
                query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
            elif '_fk' in column:
                query += f" FOREIGN KEY ({column}) REFERENCES {column.replace('_fk','')}_table({column.replace('_fk','')}),\n"
            else:
                query += f"  {column} {pd2sql(dtype)},\n"

        # Remove the last comma and close the query
        query = query.rstrip(',\n') + "\n);"

        print(query)


def output_BCNF_4_5(relations):
    for relation in relations:
        primary_key = relation.columns[0]
        table_name = f'{primary_key}_table'

        # Start creating the SQL query
        query = f"CREATE TABLE {table_name} (\n"

        # Iterate through the DataFrame columns to create the SQL query
        for column, dtype in zip(relation.columns, relation.dtypes):
            if column == primary_key:
                query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
            elif '_fk' in column:
                query += f" FOREIGN KEY ({column}),\n"
            else:
                query += f"  {column} {pd2sql(dtype)},\n"

        # Remove the last comma and close the query
        query = query.rstrip(',\n') + "\n);"

        print(query)
