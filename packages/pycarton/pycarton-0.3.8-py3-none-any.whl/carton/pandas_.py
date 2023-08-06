# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Callable, Optional, Union

import pandas as pd
from pandas import DataFrame


def explode_json_array(
    df: DataFrame, col: str, prefix: Optional[Union[str, Callable[[str], str]]] = None
) -> DataFrame:
    """Explode a JSON array column.

    Example:
    >>> df = pd.DataFrame([
        {'x': 1, 'y': [{'a': 2, 'b': 7}, {'a': 3, 'b': 1}]},
        {'x': 2, 'y': [{'a': 9, 'b': 8}, {'a': 5, 'b': 2}]}
    ])

    >>> df
       x                                     y
    0  1  [{'a': 2, 'b': 7}, {'a': 3, 'b': 1}]
    1  2  [{'a': 9, 'b': 8}, {'a': 5, 'b': 2}]

    [2 rows x 2 columns]

    >>> explode_json_array(df, 'y')
       x  y.a  y.b
    0  1    2    7
    1  1    3    1
    2  2    9    8
    3  2    5    2

    [4 rows x 3 columns]
    """
    df_exploded = df.explode(col).reset_index(drop=True)

    df_inner = pd.DataFrame(df_exploded[col].tolist())
    if callable(prefix):
        df_inner.rename(prefix, axis=1, inplace=True)
    elif prefix is None:
        df_inner.rename(lambda x: f"{col}.{x}", axis=1, inplace=True)
    elif isinstance(prefix, str):
        if prefix:
            df_inner.rename(lambda x: f"{prefix}.{x}", axis=1, inplace=True)
    else:
        raise ValueError(
            (
                "`prefix` should be str or callable if not None",
                f", but {type(prefix)} is given",
            )
        )

    df_exploded.drop(col, axis=1, inplace=True)
    df = pd.concat([df_exploded, df_inner], axis=1)

    return df
