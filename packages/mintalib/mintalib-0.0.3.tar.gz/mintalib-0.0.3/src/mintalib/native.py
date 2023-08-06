""" fincalc native routines """

import numpy as np
import pandas as pd

from .core import calc_ema, calc_rma, calc_atr, calc_trange


# TODO do we need to rename pandas specific functions to distinguish them the numeric calc functions ?
# TODO do we need to rename summary calc functions to distinguish from the rolling calc functions ?


def export(func):
    globals().setdefault('__all__', []).append(func.__name__)
    return func


@export
def shift_array(data, n=1, fill_value=np.nan):
    """ Shifts numpy array by given offset """

    xs = np.asarray(data)
    result = np.empty_like(xs)

    if n > 0:
        result[:n] = fill_value
        result[n:] = xs[:-n]
    elif n < 0:
        result[n:] = fill_value
        result[:n] = xs[-n:]
    else:
        result[:] = xs

    return result


@export
def calc_mid(prices):
    """ Calculates mid prices (used in calc_price) """

    result = prices.filter(['high', 'low', 'close']).mean(axis=1).rename('mid')
    return result


@export
def calc_log(prices):
    """ Calculates log prices (used in calc_price) """

    return np.log(prices.close).rename('log')


@export
def calc_price(prices, item='close'):
    """ looks up or calculates standard item """

    if item in prices:
        return prices.get(item)

    if item == 'mid':
        return calc_mid(prices)

    if item == 'log':
        return calc_log(prices)

    raise ValueError(f"Invalid item {item}") from None


# TODO rename calc_logret into calc_logdiff ?


@export
def calc_logret(series, n=1):
    """ Calculates log return over number of periods """

    xs = np.asarray(series)
    ys = shift_array(xs, n)
    result = np.log(xs / ys)
    return result


@export
def date_span(series, basis="365d", *, dropna=True):
    """ series date span relative to basis (requires datetimeindex) """

    if dropna:
        series = series.dropna()

    dates = series.index.get_level_values('date')

    if dates.empty:
        return np.nan

    sdate, edate = dates[0], dates[-1]

    span = (edate - sdate) / pd.Timedelta(basis)

    return span


@export
def date_sampling(series, basis="365d", *, dropna=True):
    """ series date sampling relative to basis (requires datetime index) """

    if dropna:
        series = series.dropna()

    dates = series.index.get_level_values('date')

    periods = dates.size - 1.0

    if periods <= 0:
        return np.nan

    sdate, edate = dates[0], dates[-1]

    span = (edate - sdate) / pd.Timedelta(basis)

    if span > 0:
        return periods / span

    return np.nan


@export
def calc_cagr(price):
    """ Compound Annual Growth Rate (requires datetimeindex) """

    price = price.dropna()

    if len(price) <= 1:
        return np.nan

    span = date_span(price)

    if not span > 0:
        return np.nan

    first = price.iloc[0]
    last = price.iloc[-1]

    if first <= 0 and last <= 0:
        raise ValueError("negative price")

    result = (last / first) ** (1 / span) - 1.0

    return result


@export
def calc_volatility(price):
    """ series volatility (requires a datetimeindex) ! """

    sampling = date_sampling(price, "365d")

    if not sampling > 0:
        return np.nan

    log_returns = price.apply(np.log).diff()
    result = log_returns.std() * np.sqrt(sampling)

    return result


@export
def price_density(prices, window=20):
    """ Calculates price density (cf Kaufman) """

    trading_range = (prices.high - prices.low).abs().rolling(window).sum()
    high = prices.high.rolling(window).max()
    low = prices.low.rolling(window).min()
    result = trading_range / (high - low)

    return result


@export
def tracking_error(prices, series, window=14, relative=True):
    """ Calculates average tracing error of an EMA as multiple of true range """

    delta = np.abs(series - prices.close)
    result = calc_rma(delta, window, wrap=True)

    if relative:
        atr = calc_atr(prices, window)
        return result / atr

    return result

