from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.types import is_timedelta64_dtype


datadir = Path(__file__).parent / 'data'

GLOBAL_ARMSS_TABLE_FILES = {
    'original': datadir / 'Original-ARMSS.tsv',
}


def _load_armss_table(path):
    df = pd.read_csv(path, sep='\t')
    df = df.rename(columns=lambda x: x.replace('EDSS', 'ARMSS'))
    df = pd.wide_to_long(df, 'ARMSS', i='Age', j='EDSS', sep='.', suffix=r'\d\.\d')
    return df


def global_armss(df, ref='original', ds='edss', age='ageatedss'):
    if isinstance(ref, str) and ref in GLOBAL_ARMSS_TABLE_FILES:
        ref = _load_armss_table(GLOBAL_ARMSS_TABLE_FILES.get(ref))

    df = df[[ds, age]].copy()
    if is_timedelta64_dtype(df[age]):
        df[age] = df[age] // np.timedelta64(1, 'Y')
    df[age] = np.floor(df[age]).clip(upper=75)
    results = df.merge(ref, left_on=[age, ds], right_index=True, how='left')
    return results.ARMSS
