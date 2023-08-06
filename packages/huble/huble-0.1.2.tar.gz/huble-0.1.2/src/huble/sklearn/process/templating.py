def return_function(node):
    parameters = node["parameters"]
    if node["data"]["value"] == "Normalization":
        return normalize_template(parameters)
    elif node["data"]["value"] == "Drop Duplicates":
        return drop_duplicates_template(parameters)


def normalize_template(params):
    """
    Template for normalization function
    """
    # TODO: Convert node data to normalize function parameters

    return f"data = huble.sklearn.normalize(column_name='{params['column_name']}', data=data)"


def fillna_template(params):
    """
    Template for fillna function
    """
    pass


def drop_duplicates_template(params):
    """
    Template for drop_duplicates function
    """
    return f"huble.sklearn.drop_duplicates(data_frame=data,subset={params['subset']},keep=\"{params['keep']}\")"