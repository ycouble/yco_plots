"""
Module to update a dataframe (loaded from a CSV) with new stats.
Stats are boolean for each items (e.g. test result) and day

The CSV file (if existant) from which data are read should look like that:
    ,Test1,Test2,Test3,Test4,...,Test100
    2020-08-20,0,1,1,0,...,0
    2020-08-19,0,0,1,0,...,0

Where 0 means a successful test and 1 a failed test

Usage:
    To create, increment etc a status df, use:
        - `insert_results_for_day` to update a DF
        - `update_today_statuses_in_csv` to update directly a csv status file
    To read a status csv file, use `read_status_file`
    To plot from a notebook, use `generate_plot_from_df`
    To generate the plot from script use `getnerate_plot_from_csv`
        
"""
import datetime
import os
from typing import List

import pandas as pd
import plotly.graph_objects as go


def _fill_if_new_test(dataframe: pd.DataFrame, tests: List[str]):
    """
    Fill dataframe column with failed for tests that were not yet present
    in the dataframe
    """
    for test in tests:
        if test not in dataframe.columns:
            dataframe.insert(dataframe.shape[1], test, 1)


def _add_day_failed(
    dataframe: pd.DataFrame, day: datetime.date, failed_tests: List[str]
):
    """
    Complete dataframe with 1 if the day's result is failed else 0
    """
    passed_tests = list(set(dataframe.columns) - set(failed_tests))
    dataframe.loc[day, failed_tests] = 1
    dataframe.loc[day, passed_tests] = 0
    return dataframe.fillna(0)


def read_status_file(stats_path: str) -> pd.DataFrame:
    return (
        pd.read_csv(stats_path, index_col=0, parse_dates=True)
        if os.path.isfile(stats_path)
        else pd.DataFrame()
    )


def insert_results_for_day(
    dataframe: pd.DataFrame,
    day: datetime.date,
    failed_tests: List[str],
    tests: List[str],
):
    """
    Update dataframe with day's results and fills tests past results with 0 if new
    """
    _fill_if_new_test(dataframe, tests)
    return _add_day_failed(dataframe, day, failed_tests)


def update_today_statuses_in_csv(stats_path: str, failed_tests: List[str], tests: List[str]):
    """
    Reads and update stats for today's date
    """
    past_df = read_status_file(stats_path)
    updated_df = insert_results_for_day(
        past_df, datetime.date.today(), failed_tests, tests
    )
    updated_df.to_csv(stats_path)


def generate_plot_from_df(
    res_df: pd.DataFrame, colorscale: List[str] = None
) -> go.Figure:
    """
    Generates the status plot from a DF, and returns the plotly figure
    """
    colorscale = colorscale or ["lightgreen", "red"]
    nb_dates, nb_tests = res_df.shape

    fig = go.Figure(
        data=go.Heatmap(
            z=res_df.values,
            x=res_df.columns,
            y=res_df.index,
            colorscale=colorscale,
            showscale=False,
            xgap=1,
        )
    )

    fig.update_layout(
        yaxis_autorange="reversed",
        yaxis_nticks=nb_dates + 1,
        yaxis_tickformat="%Y-%m-%d",
        xaxis_nticks=nb_tests,
        xaxis_side="top",
        xaxis_tickangle=90,
        margin=go.layout.Margin(l=50, r=20, b=20, t=500),
        width=100 + (12 + 1) * nb_tests,
        height=520 + 12 * nb_dates,
    )
    return fig


def getnerate_plot_from_csv(
    stats_path: str, output_path: str, output_format: str = "html"
) -> go.Figure:
    """
    Generate the status plot from the csv file
    :param stats_path: path of the csv file containing the statuses by date and test
    :param output_path: the output file path
    :param output_format: the desired ouput format
    :raise ValueError: when the output format is not supported
    """
    implemented_fmts = ["html"]
    res_df = read_status_file(stats_path)
    fig = generate_plot_from_df(res_df)
    if output_format not in implemented_fmts:
        raise ValueError(f"Implemented output formats: {implemented_fmts}")
    if output_format == "html":
        fig.write_html(output_path)
