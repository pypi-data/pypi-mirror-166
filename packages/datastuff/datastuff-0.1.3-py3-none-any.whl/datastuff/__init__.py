"""
This module contains a collection of functions I use for data stuff
"""

__version__ = "0.1.0"


def missing_vals(df, drop=False, threshold=70):
    """
    Returns a dataframe with the number of missing values and the
    percentage of missing values. Also drops columns with more than a
    certain percentage of missing values based on threshold
    """
    missing_df = (
        df.isnull()
        .sum()
        .to_frame(name="counts")
        .query("counts > 0")
        .assign(percentage=lambda x: round((x.counts / len(df)) * 100, 2))
        .sort_values("counts", ascending=False)
    )

    if drop:
        to_drop = list(missing_df.query(f"percentage > {threshold}").index)
        print(f"dropped columns {to_drop}")
        df = df.drop(to_drop, axis=1)
        return df

    return missing_df
