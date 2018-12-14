"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import numpy as np
import pandas as pd

# from seoulai_gym.envs.checkers.base import Constants
# from seoulai_gym.envs.checkers.rules import Rules


def trades_slicer(
    d: dict,
    start: int=0,
    end: int=1,
    keys: list=None,
    to: str='dict'
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
    if to not in ['dict', 'df']:
        raise AttributeError("invalid parameters! : to = 'dict' or 'df'")

    if keys is None:
        keys = list(d.keys())

    ret = {k: d[k][start:end] for k in keys}

    if to == 'df':
        ret = pd.DataFrame.from_dict(ret)
        return ret

    return ret

def get_ohclv(
    d,
    to: str='dict'
):
    """Calculate open, high, close, low, volume data.

    Args:
        d: dictionary. or pd.DataFrame
        to: return type. default : dictionary. If you input 'df', It can get DataFrame.

    Returns:
        ret: dictionary or pd.DataFrame
    """
    if type(d) not in [dict, pd.DataFrame]:
        raise AttributeError("invalid type! : type(d) = 'dict' or 'df'")

    if to not in ['dict', 'df']:
        raise AttributeError("invalid parameters! : to = 'dict' or 'df'")

    df = d

    if type(d) == dict:
        df = pd.DataFrame.from_dict(d) 

    price = df['price']
    volume = df['volume']

    o = price.iloc[0]
    h = price.max()
    c = price.iloc[-1]
    l = price.min()
    v = volume.sum() 

    ret = {
        "open":o,
        "high":h,
        "close":c,
        "low":l,
        "volume":v,}

    if type(to) == 'df':
        ret = pd.DataFrame.from_dict(ret) 

    return ret

     
        
