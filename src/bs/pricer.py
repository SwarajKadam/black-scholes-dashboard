import math
from dataclasses import dataclass
import numpy as np

from .utils import norm_cdf, validate_non_negative, validate_positive


@dataclass(frozen=True)
class BSInputs:
    S: float      # spot
    K: float      # strike
    T: float      # time to expiry in years
    r: float      # risk-free rate (annual, cont comp)
    sigma: float  # volatility (annual)
    q: float = 0.0  # dividend yield (annual, cont comp)


def d1_d2_np(S, K, T, r, sigma, q=0.0):
    S = np.asarray(S, dtype=float)
    sigma = np.asarray(sigma, dtype=float)

    vsqrt = sigma * np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / vsqrt
    d2 = d1 - vsqrt
    return d1, d2


def price_call(S, K, T, r, sigma, q=0.0):
    d1, d2 = d1_d2_np(S, K, T, r, sigma, q)
    disc_q = np.exp(-q * T)
    disc_r = np.exp(-r * T)
    return S * disc_q * norm_cdf(d1) - K * disc_r * norm_cdf(d2)


def price_put(S, K, T, r, sigma, q=0.0):
    d1, d2 = d1_d2_np(S, K, T, r, sigma, q)
    disc_q = np.exp(-q * T)
    disc_r = np.exp(-r * T)
    return K * disc_r * norm_cdf(-d2) - S * disc_q * norm_cdf(-d1)


def price(option_type: str, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    """
    option_type: 'call' or 'put'
    """
    t = option_type.strip().lower()
    if t == "call":
        return price_call(S, K, T, r, sigma, q)
    if t == "put":
        return price_put(S, K, T, r, sigma, q)
    raise ValueError("option_type must be 'call' or 'put'")
