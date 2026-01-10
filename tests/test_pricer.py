import math

from bs.pricer import price_call, price_put


def test_put_call_parity_holds():
    S, K, T = 100.0, 100.0, 1.0
    r, q, sigma = 0.05, 0.02, 0.2

    call = price_call(S, K, T, r, sigma, q)
    put = price_put(S, K, T, r, sigma, q)

    lhs = call - put
    rhs = S * math.exp(-q * T) - K * math.exp(-r * T)

    assert abs(lhs - rhs) < 1e-7
