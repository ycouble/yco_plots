# Status tracking plots
Module to update a dataframe (loaded from a CSV) with new stats.
Stats are boolean for each items (e.g. test result) and day

## Status file format
The CSV file (if existant) from which data are read should look like that:
```
    ,Test1,Test2,Test3,Test4,...,Test100
    2020-08-20,0,1,1,0,...,0
    2020-08-19,0,0,1,0,...,0
```

Where 0 means a successful test and 1 a failed test

## Usage
    * To create, increment etc a status df, use:
      * `insert_results_for_day` to update a DF
      * `update_today_statuses_in_csv` to update directly a csv status file
    * To read a status csv file, use `read_status_file`
    * To plot from a notebook, use `generate_plot_from_df`
    * To generate the plot from script use `getnerate_plot_from_csv`
