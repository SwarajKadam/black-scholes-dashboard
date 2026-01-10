import math
import streamlit as st

from bs.pricer import price_call, price_put

st.set_page_config(page_title="Black-Scholes MVP", layout="centered")

st.title("Black-Scholes MVP")
st.caption("Fast pricing for European options (call/put).")

col1, col2 = st.columns(2)

with col1:
    S = st.number_input("Spot (S)", min_value=0.01, value=100.0, step=1.0)
    K = st.number_input("Strike (K)", min_value=0.01, value=100.0, step=1.0)
    T = st.number_input("Time to expiry (T, years)", min_value=1e-6, value=1.0, step=0.25)

with col2:
    r = st.number_input("Risk-free rate (r)", value=0.05, step=0.01, format="%.4f")
    q = st.number_input("Dividend yield (q)", value=0.00, step=0.01, format="%.4f")
    sigma = st.number_input("Volatility (sigma)", min_value=1e-6, value=0.20, step=0.01, format="%.4f")

call = price_call(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
put = price_put(S=S, K=K, T=T, r=r, sigma=sigma, q=q)

st.subheader("Results")
c1, c2 = st.columns(2)
c1.metric("Call Price", f"{call:.4f}")
c2.metric("Put Price", f"{put:.4f}")

st.divider()
st.write("Sanity check (Put-Call Parity):")
parity_lhs = call - put
parity_rhs = S * math.exp(-q * T) - K * math.exp(-r * T)
st.write(f"Call - Put = {parity_lhs:.6f}")
st.write(f"S e^(-qT) - K e^(-rT) = {parity_rhs:.6f}")
st.write(f"Diff = {(parity_lhs - parity_rhs):.6e}")