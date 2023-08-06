from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.types import is_timedelta64_dtype


datadir = Path(__file__).parent / 'data'

GLOBAL_MSSS_TABLE_FILES = {
    'original': datadir / 'Original-MSSS.tsv',
    'updated': datadir / 'Updated-MSSS.tsv',
}


def _load_msss_table(path):
    df = pd.read_csv(path, sep='\t')
    df = df.rename(columns={'dd': 'Duration'})
    df.Duration = df.Duration.str.replace('dd', '').astype(int)
    df = df.rename(columns=lambda x: x.replace('EDSS', 'MSSS'))
    df = pd.wide_to_long(df, 'MSSS', i='Duration', j='EDSS', sep='.', suffix=r'\d\.\d')
    return df


def global_msss(df, ref='original', ds='edss', duration='dd'):
    if isinstance(ref, str) and ref in GLOBAL_MSSS_TABLE_FILES:
        ref = _load_msss_table(GLOBAL_MSSS_TABLE_FILES.get(ref))

    df = df[[duration, ds]].copy()
    if is_timedelta64_dtype(df[duration]):
        df[duration] = df[duration] // np.timedelta64(1, 'Y')
    df[duration] = np.floor(df[duration]).clip(upper=30)
    results = df.merge(ref, left_on=[duration, ds], right_index=True, how='left')
    return results.MSSS
