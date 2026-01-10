import math
from dataclasses import dataclass

from .utils import norm_cdf, validate_non_negative, validate_positive


@dataclass(frozen=True)
class BSInputs:
    S: float      # spot
    K: float      # strike
    T: float      # time to expiry in years
    r: float      # risk-free rate (annual, cont comp)
    sigma: float  # volatility (annual)
    q: float = 0.0  # dividend yield (annual, cont comp)


def d1_d2(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> tuple[float, float]:
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("T", T)
    validate_positive("sigma", sigma)

    vsqrt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / vsqrt
    d2 = d1 - vsqrt
    return d1, d2


def price_call(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    disc_q = math.exp(-q * T)
    disc_r = math.exp(-r * T)
    return S * disc_q * norm_cdf(d1) - K * disc_r * norm_cdf(d2)


def price_put(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    disc_q = math.exp(-q * T)
    disc_r = math.exp(-r * T)
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
