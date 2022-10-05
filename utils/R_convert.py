"""
Colection of functions to convert between Python objects and R objects.
"""

import os

# Set correctly R home path
os.environ["R_HOME"] = r"C:/Program Files/R/R-4.2.0"

import rpy2.robjects as ro
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri


def _convert_pydf(pydf):
    """Convert pandas df to R dataframe"""

    with localconverter(ro.default_converter + pandas2ri.converter):
        data = ro.conversion.py2rpy(pydf)

    return data


def _convert_rdf(rdf):
    """Convert (a list of) R dataframes to pandas ones"""

    if isinstance(rdf, ro.vectors.DataFrame):
        with localconverter(ro.default_converter + pandas2ri.converter):
            df = ro.conversion.rpy2py(rdf)
        return df
    else:
        df_list = []
        for r_df in rdf:
            with localconverter(ro.default_converter + pandas2ri.converter):
                df = ro.conversion.rpy2py(r_df)
                df_list.append(df)
        return df_list


def run_R_test_regs(
    source_path, df_data, var, save_path, save_name_add="", convert=True
):
    """Run test over categories (regions) in R file and return pandas objects."""

    # First, make the index a column
    df_data_r = df_data.reset_index()

    # Convert df_data to R object
    data = _convert_pydf(df_data_r)

    # Run test in R file
    r = ro.r
    r.source(source_path)
    r_df_list = r.compute_test(data, var, save_path, save_name_add)

    # Convert a list of R dataframes to pandas ones
    if convert:
        df_list = _convert_rdf(r_df_list)
        return df_list

    return r_df_list


def run_R_test_regs_multiple(
    source_path, df_data, save_path, save_name_add="", convert=True
):
    """Run test over categories (regions) for multiple 'steps'
    in R file and return pandas objects."""

    # First, make the index a column
    df_data_r = df_data.reset_index()

    # Convert df_data to R object
    data = _convert_pydf(df_data_r)

    # Run test in R file
    r = ro.r
    r.source(source_path)
    r_df_list = r.compute_test(data, save_path, save_name_add)

    # Convert a list of R dataframes to pandas ones
    if convert:
        df_list = _convert_rdf(r_df_list)
        return df_list

    return r_df_list


def run_R_test_corr(
    source_path,
    df_data,
    var_x,
    var_y,
    save_path,
    save_name_add="",
    run_single=True,
    convert=True,
):
    """Run test of correlations in R file and return pandas objects."""

    # First, make the index a 'pat' column
    df_data.index = df_data.index.set_names(["pat"])
    df_data_r = df_data.reset_index()

    # Then, keep only pat, region, var_x and var_y varibles and re-name
    df_data_r = df_data_r.loc[:, ["pat", "region", var_x, var_y]]
    df_data_r.rename(columns={var_x: "x", var_y: "y"}, inplace=True)

    # Convert df_data to R object
    data = _convert_pydf(df_data_r)

    # Run test in R file
    r = ro.r
    r.source(source_path)
    r_df = r.compute_test(data, var_x, var_y, save_path, save_name_add, run_single)

    # Convert a list of R dataframes to pandas ones
    if convert:
        df = _convert_rdf(r_df)
        return df

    return r_df

