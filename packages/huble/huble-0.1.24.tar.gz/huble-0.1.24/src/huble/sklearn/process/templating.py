def return_function(node):
    if node["data"]["value"] == "Remove NAN values":
        return remove_nan_values(node)
    elif node["data"]["value"] == "Replace NAN values":
        return replace_nan_values(node)
    elif node["data"]["value"] == "Dropping rows or columns":
        return drop_rows_columns(node)
    elif node["data"]["value"] == "Remove Outliers":
        return remove_outliers(node)
    elif node["data"]["value"] == "Drop Duplicates":
        return drop_duplicates(node)
    elif node["data"]["value"] == "Change Data Type":
        return change_data_type(node)
    elif node["data"]["value"] == "Round Data":
        return round_data(node)
    elif node["data"]["value"] == "Filter DataFrame":
        return filter_dataframe(node)
    elif node["data"]["value"] == "Truncate DataFrame":
        return truncate_dataframe(node)
    elif node["data"]["value"] == "Sort Values":
        return sort_values(node)
    elif node["data"]["value"] == "Transpose DataFrame":
        return transpose(node)
    elif node["data"]["value"] == "Min Max Scalar":
        return min_max_scale(node)
    elif node["data"]["value"] == "Max Abs Scalar":
        return max_abs_scale(node)
    elif node["data"]["value"] == "Robust Scalar":
        return robust_scale(node)
    elif node["data"]["value"] == "Stanadrd Scalar":
        return standard_scale(node)
    elif node["data"]["value"] == "Normalization":
        return normalize(node)
    elif node["data"]["value"] == "Ordinal Encoding":
        return ordinal_encode(node)
    elif node["data"]["value"] == "One Hot Encoding":
        return one_hot_encode(node)


def remove_nan_values(params):
    return f"data = huble.sklearn.remove_nan_values(data=data,axis={params['axis']}, how='{params['how']}',inplace={params['inplace']},subset={params['subset']})"


def replace_nan_values(params):
    return f"data = huble.sklearn.replace_nan_values(data=data,missing_values={params['missing_values']}, strategy='{params['strategy']}',fill_value={params['fill_value']})"


def drop_rows_columns(params):
    return f"data = huble.sklearn.drop_rows_columns(data=data,labels={params['labels']},axis={params['axis']},index={params['index']},columns={params['columns']},inplace={params['inplace']},errors='{params['errors']}')"


def remove_outliers(params):
    return (
        f"data = huble.sklearn.remove_outliers(data=data,columns='{params['columns']}')"
    )


def drop_duplicates(params):
    return f"data = huble.sklearn.drop_duplicates(data=data,subset={params['subset']}, keep={params['keep']},inplace={params['inplace']},ignore_index='{params['ignore_index']}')"


def change_data_type(params):
    return f"data = huble.sklearn.change_data_type(data=data,column={params['column']}, data_type={params['data type']})"


def round_data(params):
    return f"data = huble.sklearn.round_data(data=data,columns={params['columns']}, decimals={params['decimals']})"


def filter_dataframe(params):
    return f"data = huble.sklearn.filter_dataframe(data=data,items={params['like']},like={params['like']},regex={params['regex']},axis={params['axis']})"


def truncate_dataframe(params):
    return f"data = huble.sklearn.truncate_datfarame(data=data,before={params['before']}, after={params['after']}, copy={params['copy']}, axis={params['axis']})"


def sort_values(params):
    return f"data = huble.sklearn.sort_values(data=data,by={params['by']},axis={params['axis']},ascending={params['ascending']},inplace={params['inplace']},kind={params['kind']},na_position={params['na_position']},ignore_index={params['ignore_index']})"


def transpose():
    return f"data = huble.sklearn.transpose(data=data)"


def min_max_scale(params):
    return f"data = huble.sklearn.min_max_scalar(data=data, columns={params['columns']}, feature_range={params['feature_range']}, copy={params['copy']}, clip={params['clip']})"


def max_abs_scale(params):
    return f"data = huble.sklearn.max_abs_scalar(data=data, columns={params['columns']}, copy={params['copy']})"


def robust_scale(params):
    return f"data = huble.sklearn.robust_scalar(data=data, column={params['column']}, with_centering={params['with_centering']}, with_scaling={params['with_scaling']}, copy={params['copy']}, unit_varianc={params['unit_varianc']}, quantile_range={params['quantile_range']})"


def standard_scale(params):
    return f"data = huble.sklearn.standard_scalar(data=data, column={params['column']}, copy={params['copy']}, with_mean={params['with_mean']}, with_std={params['with_std']})"


def normalize(params):
    return f"data = huble.sklearn.normalize(data=data, column={params['column']}, norm={params['norm']})"


def ordinal_encode(params):
    return f"data = huble.sklearn.ordinal_encode(data=data, categories={params['categories']}, dtype={params['dtype']}, handle_unknown={params['handle_unknown']}, unknown_value={params['unknown_value']}, encoded_missing_value={params['encoded_missing_value']})"


def one_hot_encode(params):
    return f"data = huble.sklearn.one_hot_encode(data=data, categorical_features={params['categorical_features']}, dtype={params['dtype']}, handle_unknown={params['handle_unknown']}, n_values={params['n_values']}, sparse={params['sparse']})"


# def normalize(params):
#   '''
#   Template for normalization function
#   '''
#   #TODO: Convert node data to normalize function parameters

#   return f"data = huble.sklearn.normalize(column_name='{params['column_name']}', data=data)"

# def fillna(params):
#   '''
#   Template for fillna function
#   '''
#   pass

# def drop_duplicates():
#   '''
#   Template for drop_duplicates function
#   '''
#   return "huble.sklearn.drop_duplicates(data)"
