"""
Common portfolio metrics
"""

import numpy as np
import pandas as pd


def sharpe_ratio_daily(returns, risk_free_rate=0):
    """
    Compute the Sharpe ratio of a strategy.

    Assumes index is a datetime of days.

    Not sure how NaNs are handled.
    """
    retseries = returns.values
    return np.sqrt(365) * (np.mean(retseries) - risk_free_rate) / np.std(retseries)


def sortino_ratio_daily(returns, risk_free_rate=0):
    """
    Compute the Sortino ratio of a strategy.

    Assumes index is a datetime of days.

    Also not sure how NaNs are handled.
    """
    retseries = returns.values

    if len(retseries[retseries < 0]) > 1:
        downside_returns = retseries[retseries < 0]
    else:
        return np.inf
    return (
        np.sqrt(365) * (np.mean(retseries) - risk_free_rate) / np.std(downside_returns)
    )


def romad_ratio_daily(returns, risk_free_rate=0):
    """
    Compute the romad ratio of a strategy.

    Assumes index is a datetime of days.
    """
    retseries = returns.values

    if retseries.min() < 0:
        drawdown = abs(retseries.min())
    else:
        return np.inf
    return annualized_return(returns) / drawdown


def annualized_return(returns, days_in_year=365):
    """
    Compute the annualized return of a strategy.

    Assumes index is a datetime of days.
    """
    period = returns.shape[0]
    retseries = returns.values
    return np.power(np.e, np.log(1 + retseries).sum() * days_in_year / period) - 1


def cumulative_return(returns):
    """
    Compute the cumulative return of a strategy.

    Assumes index is a datetime of days.
    """
    retseries = returns.values
    return (1 + retseries).cumprod()[-1] - 1


def max_drawdown(returns):
    """
    Compute the max drawdown of a strategy.

    Assumes index is a datetime of days.
    """
    retseries = returns.values

    return abs(retseries.min()) if retseries.min() < 0 else 0


def annualized_volatility(returns, days_in_year=365):
    """
    Compute the daily volatility of a strategy.

    Assumes index is a datetime of days.
    """
    retseries = returns.values
    return retseries.std() * np.sqrt(days_in_year) * 100


def value_at_risk(returns, percentile=5):
    """
    Compute the VaR of a strategy.
    """
    retseries = returns.values
    return np.percentile(retseries, percentile)


def expected_shortfall(returns, percentile=5):
    """
    Compute the expected_shortfall of a strategy.
    """
    retseries = returns.values

    thresh = np.percentile(retseries, percentile)
    return retseries[retseries < thresh].mean()


def tear_sheet(returns, format=False):
    """
    Generate a tear sheet of a strategy.
    """
    df = pd.DataFrame()
    df["Annualized Return"] = annualized_return(returns)
    df["Cumulative Return"] = cumulative_return(returns)
    df["Sharpe"] = sharpe_ratio_daily(returns)
    df["Sortino"] = sortino_ratio_daily(returns)
    df["RoMaD"] = romad_ratio_daily(returns)
    df["Max Drawdown"] = max_drawdown(returns)
    df["Annualized Volatility"] = annualized_volatility(returns)
    df["Value at Risk"] = value_at_risk(returns)
    df["Expected Shortfall"] = expected_shortfall(returns)
    df = pd.DataFrame(
        (
            annualized_return(returns),
            cumulative_return(returns),
            sharpe_ratio_daily(returns),
            sortino_ratio_daily(returns),
            romad_ratio_daily(returns),
            max_drawdown(returns),
            annualized_volatility(returns),
            value_at_risk(returns),
            expected_shortfall(returns),
        ),
        index=[
            "Annualized Return",
            "Cumulative Return",
            "Sharpe",
            "Sortino",
            "RoMaD",
            "Max Drawdown",
            "Annualized Volatility",
            "Value at Risk",
            "Expected Shortfall",
        ],
    ).T

    if format:
        df["Annualized Return"] = ((df["Annualized Return"] * 100).round(2)).astype(
            "str"
        ) + "%"
        df["Cumulative Return"] = ((df["Cumulative Return"] * 100).round(2)).astype(
            "str"
        ) + "%"
        df["Sharpe"] = df["Sharpe"].round(2)
        df["Sortino"] = df["Sortino"].round(2)
        df["RoMaD"] = df["RoMaD"].round(2)
        df["Max Drawdown"] = ((df["Max Drawdown"] * 100).round(2)).astype("str") + "%"
        df["Annualized Volatility"] = ((df["Annualized Volatility"]).round(2)).astype(
            "str"
        ) + "%"
        df["Value at Risk"] = (df["Value at Risk"] * 100).round(2).astype("str") + "%"
        df["Expected Shortfall"] = (df["Expected Shortfall"] * 100).round(2).astype(
            "str"
        ) + "%"

    return df
