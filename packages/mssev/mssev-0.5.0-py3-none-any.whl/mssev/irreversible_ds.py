import numpy as np
import pandas as pd


def _first_irreversible_ds(df):
    for ds in df.ids:
        i = np.where(df.dss == ds)[0][-1]
        if np.all(df.dss[i:] >= ds):
            return ds
    return np.nan


def _calculate_irreversible_ds_from(df, ds, t, min_period):
    ndim = len(df)  # number of assessments
    ts = np.tile(df[t], ndim).reshape((ndim, ndim))
    tsdelta = ts.T - ts

    # ts:
    #
    #   [[T0 T1 T2 ... Tn]
    #    [T0 T1 T2 ... Tn]
    #    [      T2 ...   ]
    #    [T0 T1 T2 ... Tn]]
    #

    # tsdelta:
    #
    #   [[(T0-T0) (T0-T1) ... (T0-Tn)]
    #    [(T1-T0) (T1-T1) ... (T1-Tn)]
    #    [                ...        ]
    #    [(Tn-T0) (Tn-T1) ... (Tn-Tn)]]
    #

    dsm = np.tile(df[ds], ndim).reshape((ndim, ndim))
    idsm = dsm = np.where(tsdelta >= np.timedelta64(0), dsm, np.nan)

    if min_period is not None:
        tsvalid = np.tile(df[t] + min_period, ndim).reshape((ndim, ndim))

        # tsvalid:
        #
        #   [[(T0+X) (T1+X) ... (Tn+X)]
        #    [(T0+X) (T1+X) ... (Tn+X)]
        #    [              ...       ]
        #    [(T0+X) (T1+X) ... (Tn+X)]]
        #

        idsm = np.where(ts.T >= tsvalid, dsm, np.nan)

    dss = (pd.Series(np.split(dsm.ravel(), ndim), name='dss', index=df.index)
             .map(lambda ds: ds[~np.isnan(ds)]))

    ids = (pd.Series(np.split(idsm.ravel(), ndim), name='ids', index=df.index)
             .map(lambda ds: np.unique(ds[~np.isnan(ds)])[::-1]))

    scores = pd.concat([dss, ids], axis=1)
    return scores.apply(_first_irreversible_ds, axis=1)


def irreversible_ds(df, pid='pid', ds='edss', t='date', min_period=None):
    results = pd.Series([], dtype=df[ds].dtype)
    grouped = df.sort_values(t).groupby(pid)
    for _, rows in grouped:
        idss = _calculate_irreversible_ds_from(rows, ds, t, min_period)
        results = pd.concat([results, idss])
    return results
