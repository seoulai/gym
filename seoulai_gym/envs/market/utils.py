"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import pandas as pd


def trades_slicer(
    d: dict,
    start: int=0,
    end: int=1,
    keys: list=None,
    to: str="dict"
):
    """Slicing time series data.(trades)

    Args:
        d: dictionary. trades = {timestamp, price, volume, ask_bid, sid}
        start: start index
        end: end index
        keys: target columns. default : dict.keys()
        to: return type. default : dictionary. If you input 'df', It can get DataFrame.

    Returns:
        ret: dictionary or pd.DataFrame
    """
    if to not in ["dict", "df"]:
        msg = """ to = "dict" or "df" """
        raise AttributeError(f"invalid parameters! : {msg}")

    if keys is None:
        keys = list(d.keys())

    ret = {k: d[k][start:end] for k in keys}

    if to == "df":
        ret = pd.DataFrame.from_dict(ret)
        return ret

    return ret


def get_ohclv(
    d,
    to: str="dict"
):
    """Calculate open, high, close, low, volume data.

    Args:
        d: dictionary. or pd.DataFrame
        to: return type. default : dictionary. If you input 'df', It can get DataFrame.

    Returns:
        ret: dictionary or pd.DataFrame
    """
    if type(d) not in [dict, pd.DataFrame]:
        msg = """ type(d) = "dict" or "df" """
        raise AttributeError(f"invalid type! : {msg}")

    if to not in ["dict", "df"]:
        msg = """ to = "dict" or "df" """
        raise AttributeError("invalid parameters! : {msg}")

    df = d

    if type(d) == dict:
        df = pd.DataFrame.from_dict(d)

    price = df["price"]
    volume = df["volume"]

    open_price = price.iloc[0]
    high_price = price.max()
    close_price = price.iloc[-1]
    low_price = price.min()
    v = volume.sum()

    ret = {
        "open": open_price,
        "high": high_price,
        "close": close_price,
        "low": low_price,
        "volume": v,
        }

    if type(to) == "df":
        ret = pd.DataFrame.from_dict(ret)

    return ret
