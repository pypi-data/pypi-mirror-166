# coding=utf-8
import numpy as np
import pandas as pd
from scipy.ndimage.filters import generic_filter, minimum_filter1d
from scipy.ndimage.measurements import label
from scipy.signal import argrelextrema


def minimum_filter(ts, **kwargs):
    """Return stationary base flow

    The base flow is set to the minimum observed flow.

    :param ts:
    :return:
    """
    minimum = min(ts)
    out_values = minimum * np.ones(len(ts))
    baseflow = pd.Series(data=out_values, index=ts.index)
    quickflow = ts - baseflow
    baseflow.name = "baseflow"
    quickflow.name = "quickflow"
    return baseflow, quickflow


def fixed_interval_filter(ts, size):
    """USGS HYSEP fixed interval method

    The USGS HYSEP fixed interval method as described in `Sloto & Crouse, 1996`_.

    .. _Slot & Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for Streamflow Hydrograph Separation and
        Analysis.” USGS Numbered Series. Water-Resources Investigations Report. Geological Survey (U.S.), 1996.
        http://pubs.er.usgs.gov/publication/wri964040.


    :param size:
    :param ts:
    :return:
    """
    intervals = np.arange(len(ts)) // size
    baseflow = pd.Series(data=ts.groupby(intervals).transform("min"), index=ts.index)
    quickflow = ts - baseflow


# -*- coding: utf-8 -*-
"""Tools for hydrology.

hydrotoolbox baseflow --area 59.1 --area_units 'mile**2' linear < daily.csv
hydrotoolbox baseflow sliding < daily.csv
hydrotoolbox baseflow eckardt,sliding < daily.csv
...

hydrotoolbox recession """


import importlib
import os.path
import sys
import warnings

import numpy as np
import pandas as pd
from mando import Program
from mando.rst_text_formatter import RSTHelpFormatter
from scipy.ndimage import generic_filter, minimum_filter1d
from scipy.signal import lfilter
from toolbox_utils import tsutils

from . import baseflow_lib
from .utils import nstar

warnings.filterwarnings("ignore")

program = Program("hydrotoolbox", "0.0")

program.add_subprog("baseflow_sep")


@program.baseflow_sep.command(
    "boughton", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def boughton_cli(
    k,
    C,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Boughton double-parameter filter (Boughton, 2004)

    !             C             k
    !    Qb   = -----  Q   +  -----  Qb
    !      i    1 + C   i     1 + C    (i-1)

    Parameters
    ----------
    k: float
        recession coefficient
    C: float
        calibrated in baseflow.param_estimate
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        boughton(
            k,
            C,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def boughton(
    k,
    C,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    if print_input is True:
        ntsd = Q.copy()
    for col in Q.columns:
        Q.loc[:, col] = lfilter([C / (1 + C)], [1.0, -k / (1 + C)], Q.loc[:, col])
    return tsutils.return_input(print_input, ntsd, Q, suffix="boughton")


@program.baseflow_sep.command(
    "chapman", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def chapman_cli(
    a,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Chapman filter (Chapman, 1991)

    Parameters
    ----------
    a float
        recession coefficient
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        chapman(
            a,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def chapman(
    a,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    if print_input is True:
        ntsd = Q.copy()
    a = float(a)
    Qb = Q.copy()
    for col in range(len(Q.columns)):
        for i in range(1, len(Q.index)):
            Qb.iloc[i, col] = (3 * a - 1) / (3 - a) * Qb.iloc[i - 1, col] + 2 / (
                3 - a
            ) * (Q.iloc[i, col] - a * Q.iloc[i - 1, col])
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="chapman")


@program.baseflow_sep.command("cm", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(tsutils.docstrings)
def cm_cli(
    k,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """CM filter (Chapman and Maxwell, 1996)

           1 - k           k
    Qb   = -----  Q   +  -----  Qb
      i    2 - k   i     2 - k    (i-1)

    Parameters
    ----------
    a: float
        recession coefficient
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        cm(
            k,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def cm(
    k,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    k = float(k)
    if print_input is True:
        ntsd = Q.copy()
    for col in Q.columns:
        Q.loc[:, col] = lfilter([(1 - k) / (2 - k)], [1.0, -k / (2 - k)], Q.loc[:, col])
    return tsutils.return_input(print_input, ntsd, Q, suffix="cm")


@program.baseflow_sep.command(
    "eckhardt", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def eckhardt_cli(
    a,
    BFImax,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Eckhardt filter (Eckhardt, 2005)

    Parameters
    ----------
    a: float
        recession coefficient
    BFImax: float
        maximum value of baseflow index (BFI)
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        eckhardt(
            a,
            BFImax,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def eckhardt(
    a,
    BFImax,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.copy()
    for col in range(len(Q.columns)):
        for i in range(1, len(Q.index)):
            Qb.iloc[i, col] = (
                (1 - BFImax) * a * Qb.iloc[i - 1, col]
                + (1 - a) * BFImax * Q.iloc[i, col]
            ) / (1 - a * BFImax)
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="eckhardt")


@program.baseflow_sep.command("ewma", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(tsutils.docstrings)
def ewma_cli(
    span,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Exponential Weighted Moving Average (EWMA) filter (Tularam and Ilahee, 2008)

    Parameters
    ----------
    span: float
        alpha = 2/(span + 1)
        smoothing parameter
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        ewma(
            span,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def ewma(
    span,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    span = float(span)
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.ewm(span=span).mean()
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="ewma")


@program.baseflow_sep.command(
    "fixed", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def fixed_cli(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Fixed interval method from USGS HYSEP program `Sloto and Crouse, 1996`_.

    Parameters
    ----------
    area: float
        basin area in mile^2
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}

    .. _Slot and Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for
        Streamflow Hydrograph Separation and Analysis.” USGS Numbered Series.
        Water-Resources Investigations Report. Geological Survey (U.S.), 1996.
        http://pubs.er.usgs.gov/publication/wri964040.
    """
    tsutils.printiso(
        fixed(
            area=area,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def fixed(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    size = nstar(area, "miles**2")
    intervals = np.arange(len(Q)) // size
    Qb = pd.DataFrame(data=Q.groupby(intervals).transform("min"), index=Q.index)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="fixed")


@program.baseflow_sep.command(
    "furey", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def furey(
    a,
    A,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Furey digital filter (Furey and Gupta, 2001, 2003)

    Parameters
    ----------
    a: float
        recession coefficient
    A: float
        calibrated in baseflow.param_estimate
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        furey(
            a,
            A,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def furey(
    a,
    A,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.copy()
    for col in range(len(Q.columns)):
        for i in range(1, len(Q.index)):
            Qb.iloc[i, col] = (a - A * (1 - a)) * Qb.iloc[i - 1, col] + A * (
                1 - a
            ) * Q.iloc[i - 1, col]
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, "furey")


@program.baseflow_sep.command("lh", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(tsutils.docstrings)
def lh_cli(
    input_ts="-",
    beta=0.925,
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """LH digital filter (Lyne and Hollick, 1979)

    Parameters
    ----------
    beta: float
        filter parameter, 0.925 recommended by (Nathan and McMahon, 1990)
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        lh(
            beta=beta,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def lh(
    input_ts="-",
    beta=0.925,
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    beta = float(beta)
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.copy()
    for col in range(len(Q.columns)):
        # first pass
        Qb.iloc[0:col] = Q.iloc[0:col] / 2
        for i in range(len(Q.index) - 1):
            Qb.iloc[i + 1, col] = beta * Q.iloc[i, col] + (1 - beta) / 2 * (
                Q.iloc[i, col] + Q.iloc[i + 1, col]
            )

        # second pass
        Qb1 = Qb.copy()
        for i in range(len(Q.index) - 2, -1, -1):
            Qb1.iloc[i, col] = beta * Qb.iloc[i + 1, col] + (1 - beta) / 2 * (
                Qb.iloc[i + 1, col] + Qb.iloc[i, col]
            )
    return tsutils.return_input(print_input, ntsd, Qb1, suffix="lh")


@program.baseflow_sep.command(
    "local", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def local_cli(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Local minimum graphical method from HYSEP program (Sloto and Crouse, 1996)

    Parameters
    ----------
    area: float
        basin area in mile^2
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        local(
            area=area,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def local(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()

    size = nstar(area, "miles^2")
    Qb = Q.copy()
    for col in range(len(Q.columns)):
        baseflow_min = pd.Series(
            generic_filter(Q.iloc[:, col].astype("float64"), _local_minimum, size=size),
            index=Q.index,
        )
        Qb.iloc[:, col] = baseflow_min.interpolate(method="linear")
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="local")


def _local_minimum(window):
    win_center_ix = int(np.floor(window.size / 2))
    win_center_val = window[win_center_ix]
    win_minimum = np.min(window)
    if win_center_val == win_minimum:
        return win_center_val
    return np.nan


@program.baseflow_sep.command(
    "slide", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def slide_cli(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """USGS HYSEP sliding interval method

    The USGS HYSEP sliding interval method described in
    `Sloto and Crouse, 1996`_.

    The flow series is filter with scipy.ndimage.genericfilter1D using
    numpy.nanmin function over a window of size `size`

    .. _Slot and Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for
        Streamflow Hydrograph Separation and Analysis.” USGS Numbered Series.
        Water-Resources Investigations Report. Geological Survey (U.S.), 1996.
        http://pubs.er.usgs.gov/publication/wri964040.

    Parameters
    ----------
    area: float
        Area of watershed in miles**2
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        slide(
            area=area,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def slide(
    area=None,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    size = nstar(area, "miles**2")
    Qb = Q.copy()
    for col in Q.columns:
        ts = Q.loc[:, col].astype("float")
        if ts.isnull().values.any():
            blocks, nfeatures = label(~ts.isnull())
            block_list = [ts[blocks == i] for i in range(1, nfeatures + 1)]
            na_df = ts[blocks == 0]
            block_bf = [
                pd.Series(
                    data=minimum_filter1d(block, size, mode="reflect"),
                    index=block.index,
                )
                for block in block_list
            ]
            baseflow = pd.concat(block_bf + [na_df], axis=0)
            baseflow.sort_index(inplace=True)
        else:
            baseflow = pd.Series(
                data=minimum_filter1d(ts, size, mode="reflect"), index=Q.index
            )
        Qb.loc[:, col] = baseflow
    Qb = Qb.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="slide")


@program.baseflow_sep.command("ukih", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(tsutils.docstrings)
def ukih_cli(
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Graphical method developed by UK Institute of Hydrology (UKIH, 1980)

    Parameters
    ----------
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        ukih(
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def ukih(
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.copy()
    N = 5
    block_end = len(Q.index) // N * N
    for col in range(len(Q.columns)):
        idx_min = np.argmin(
            np.array(Q.iloc[:block_end, col].values).reshape(-1, N), axis=1
        )
        idx_min = idx_min + np.arange(0, block_end, N)
        idx_turn = UKIH_turn(Q.iloc[:, col], idx_min)
        Qb.iloc[:, col] = linear_interpolation(Q.iloc[:, col], idx_turn)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="ukih")


def UKIH_turn(Q, idx_min):
    idx_turn = np.zeros(idx_min.shape[0], dtype=np.int64)
    for i in range(idx_min.shape[0] - 2):
        if (0.9 * Q[idx_min[i + 1]] < Q[idx_min[i]]) & (
            0.9 * Q[idx_min[i + 1]] < Q[idx_min[i + 2]]
        ):
            idx_turn[i] = idx_min[i + 1]
    return idx_turn[idx_turn != 0]


def linear_interpolation(Q, idx_turn):
    b = np.zeros(len(Q.index))

    n = 0
    for i in range(idx_turn[0], idx_turn[-1] + 1):
        if i == idx_turn[n + 1]:
            n += 1
            b[i] = Q[i]
        else:
            b[i] = Q[idx_turn[n]] + (Q[idx_turn[n + 1]] - Q[idx_turn[n]]) / (
                idx_turn[n + 1] - idx_turn[n]
            ) * (i - idx_turn[n])
        if b[i] > Q[i]:
            b[i] = Q[i]
    return b


@program.baseflow_sep.command(
    "willems", formatter_class=RSTHelpFormatter, doctype="numpy"
)
@tsutils.doc(tsutils.docstrings)
def willems_cli(
    a,
    w,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Digital filter (Willems, 2009)

    Parameters
    ----------
    a: float
        recession coefficient
    w: float
        case-speciﬁc average proportion of the quick ﬂow
        in the streamflow, calibrated in baseflow.param_estimate
    input_ts
        Streamflow
    {columns}
    {source_units}
    {start_date}
    {end_date}
    {dropna}
    {clean}
    {round_index}
    {skiprows}
    {index_type}
    {names}
    {target_units}
    {print_input}
    {tablefmt}
    """
    tsutils.printiso(
        willems(
            a,
            w,
            input_ts=input_ts,
            columns=columns,
            source_units=source_units,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt=tablefmt,
    )


def willems(
    a,
    w,
    input_ts="-",
    columns=None,
    source_units=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    target_units=None,
    print_input=False,
):
    Q = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts,
            skiprows=skiprows,
            names=names,
            index_type=index_type,
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
    )
    ntsd = pd.DataFrame()
    if print_input is True:
        ntsd = Q.copy()
    Qb = Q.copy()
    v = (1 - w) * (1 - a) / (2 * w)
    for col in range(len(Q.columns)):
        for i in range(len(Q.index) - 1):
            Qb.iloc[i + 1, col] = (a - v) / (1 + v) * Qb.iloc[i, col] + v / (1 + v) * (
                Q.iloc[i, col] + Q.iloc[i + 1, col]
            )
    Qb = Q.mask(Qb > Q, Q)
    return tsutils.return_input(print_input, ntsd, Qb, suffix="willems")


@program.command()
def about():
    """Display version number and system information."""
    tsutils.about(__name__)


def main():
    """Set debug and run mando.main function."""
    if not os.path.exists("debug_hydrotoolbox"):
        sys.tracebacklimit = 0
    program()


if __name__ == "__main__":
    main()
    baseflow.name = "baseflow"
    quickflow.name = "quickflow"

    return baseflow, quickflow


def sliding_interval_filter(ts, size):
    """USGS HYSEP sliding interval method

        The USGS HYSEP sliding interval method as described in `Sloto & Crouse, 1996`_.

        The flow series is filter with scipy.ndimage.genericfilter1D using numpy.nanmin function
        over a window of size `size`

    .. _Slot & Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for Streamflow Hydrograph Separation and
        Analysis.” USGS Numbered Series. Water-Resources Investigations Report. Geological Survey (U.S.), 1996.
        http://pubs.er.usgs.gov/publication/wri964040.

    :param size:
    :param ts:
    :return:
    """
    # TODO ckeck the presence of nodata
    if (ts.isnull()).any():
        blocks, nfeatures = label(~ts.isnull())
        block_list = [ts[blocks == i] for i in range(1, nfeatures + 1)]
        na_df = ts[blocks == 0]
        block_bf = [
            pd.Series(
                data=minimum_filter1d(block, size, mode="reflect"), index=block.index
            )
            for block in block_list
        ]
        baseflow = pd.concat(block_bf + [na_df], axis=0)
        baseflow.sort_index(inplace=True)
    else:
        baseflow = pd.Series(
            data=minimum_filter1d(ts, size, mode="reflect"), index=ts.index
        )

    quickflow = ts - baseflow

    baseflow.name = "baseflow"
    quickflow.name = "quickflow"

    return baseflow, quickflow


def local_minimum_filter(ts, size):
    """USGS HYSEP local minimum method

        The USGS HYSEP local minimum method as described in `Sloto & Crouse, 1996`_.

    .. _Slot & Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for Streamflow Hydrograph Separation and
        Analysis.” USGS Numbered Series. Water-Resources Investigations Report. Geological Survey (U.S.), 1996.
        http://pubs.er.usgs.gov/publication/wri964040.

    :param size:
    :param ts:
    :return:
    """

    origin = int(size) / 2
    baseflow_min = pd.Series(
        generic_filter(ts, _local_minimum, footprint=np.ones(size)), index=ts.index
    )
    baseflow = baseflow_min.interpolate(method="linear")
    # interpolation between values may lead to baseflow > streamflow
    errors = baseflow > ts
    while errors.any():
        print("hello world")
        error_labelled, n_features = label(errors)
        error_blocks = [ts[error_labelled == i] for i in range(1, n_features + 1)]
        error_local_min = [argrelextrema(e.values, np.less)[0] for e in error_blocks]
        print(error_local_min)
        break
    quickflow = ts - baseflow
    baseflow.name = "baseflow"
    quickflow.name = "quickflow"

    return baseflow, quickflow


def eckhardt_filter(ts, size):
    return fixed_interval_filter(ts, size)


def _local_minimum(window):
    win_center_ix = len(window) / 2
    win_center_val = window[win_center_ix]
    win_minimum = np.min(window)
    if win_center_val == win_minimum:
        return win_center_val
    else:
        return np.nan


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    data = pd.Series.from_csv(
        "test/hysep_data.csv", parse_dates=True, index_col=0, header=0
    )
    b, q = local_minimum_filter(data, 93)
    plt.plot(data)
    plt.plot(b)
    plt.show()
