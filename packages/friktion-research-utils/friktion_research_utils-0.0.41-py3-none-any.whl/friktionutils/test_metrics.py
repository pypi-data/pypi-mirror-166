import pytest
import pandas as pd
from datetime import datetime
import numpy as np

from friktionutils.metrics import (
    sharpe_ratio_daily,
    sortino_ratio_daily,
    calmar_ratio_daily,
    annualized_return,
    cumulative_return,
    max_drawdown,
    annualized_volatility,
    value_at_risk,
    expected_shortfall,
    tear_sheet,
)
from friktionutils.options import random_walk

df = pd.DataFrame()
df.index = pd.date_range(start="1/1/2020", periods=700, freq="D")
df["returns"] = random_walk(1, 700, 0, 100)
df["returns"] = df.returns - 1
print(df)


@pytest.mark.parametrize(
    "returns",
    [
        (df),
    ],
)
def test_sharpe_ratio_daily(returns):
    print(tear_sheet(df.returns))
    assert False
    # assert np.mean(df.returns) == df.mean().iloc[0]
    # assert x == (df.mean() / df.std() * np.sqrt(700)).iloc[0]
