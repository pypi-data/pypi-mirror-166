__version__ = "0.1.0"

import pandas as pd


def missing_vals(df, drop=False, threshold=70):

    missing_df = (
        df.isnull()
        .sum()
        .to_frame(name="counts")
        .query("counts > 0")
        .assign(percentage=lambda x: round((x.counts / len(df)) * 100, 2))
        .sort_values("counts", ascending=False)
    )

    if drop == True:
        to_drop = list(missing_df.query(f"percentage > {threshold}").index)
        print(f"dropped columns {to_drop}")
        df = df.drop(to_drop, axis=1)
        return df

    return missing_df
