import pytest
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# from utils import options

from friktionutils.options import Surface, Curve, find_strike

df = pd.read_csv("btc_call.csv")
df2 = pd.read_csv("btc_put.csv")
df3 = pd.read_csv("sol_put.csv")

CALL = Surface(df, datetime(2022, 1, 1), "C", "BTC", 20000)
PUT = Surface(df2, datetime(2022, 1, 1), "P", "BTC", 20000)
SOLPUT = Surface(df3, datetime(2022, 7, 18), "P", "SOL", 40)


@pytest.mark.parametrize(
    "strike, delta",
    [
        (
            1.0,
            0.1,
        ),
    ],
)
def test_getIvFromStrike(strike, delta):
    iv = SOLPUT.curves[0].getIvFromDelta(delta)
    strike = find_strike("P", SOLPUT.spot, 7 / 365, 0, iv / 100, delta)
    print(SOLPUT.spot, strike, delta, iv)
    assert iv


@pytest.mark.parametrize(
    "delta",
    [
        (0.1),
    ],
)
def test_getIvFromDelta_sol_put(delta):
    iv = SOLPUT.curves[0].getIvFromDelta(delta)
    print(SOLPUT.symbol)
    assert iv == 143.24369863013698
    print(delta, iv)


@pytest.mark.parametrize(
    "strike",
    [
        (100),
    ],
)
def test_getIvFromStrike_low_call(strike):
    iv = CALL.curves[0].getIvFromStrike(strike)
    assert iv == 67.6
    print(strike, iv)


@pytest.mark.parametrize(
    "strike",
    [
        (25000),
    ],
)
def test_getIvFromStrike_mid_call(strike):
    iv = CALL.curves[0].getIvFromStrike(strike)
    assert iv == 70.4
    print(strike, iv)


@pytest.mark.parametrize(
    "strike",
    [
        (250000),
    ],
)
def test_getIvFromStrike_mid_high(strike):
    iv = CALL.curves[0].getIvFromStrike(strike)
    assert iv == 137.9
    print(strike, iv)


@pytest.mark.parametrize(
    "strike",
    [
        (25200),
    ],
)
def test_getIvFromStrike_mid_put(strike):
    iv = PUT.curves[0].getIvFromStrike(strike)
    assert iv == 75.036
    print(strike, iv)


def test_find_strike():
    print(PUT.curves[0].getIvFromStrike(20000))
    print(PUT.curves[0].getIvFromDelta(0.4))
    print()
    assert False
