import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

st.subheader("Heatmap: Option Price vs Spot (S) and Volatility (σ)")

heat_option = st.selectbox("Heatmap for", ["Call", "Put"], index=0)

colA, colB, colC = st.columns(3)
with colA:
    s_min = st.number_input("S min", min_value=0.01, value=max(0.01, S * 0.8), step=1.0)
with colB:
    s_max = st.number_input("S max", min_value=0.01, value=S * 1.2, step=1.0)
with colC:
    s_steps = st.number_input("S steps", min_value=5, value=25, step=5)

colD, colE, colF = st.columns(3)
with colD:
    v_min = st.number_input("σ min", min_value=1e-6, value=max(1e-6, sigma * 0.5), step=0.01, format="%.4f")
with colE:
    v_max = st.number_input("σ max", min_value=1e-6, value=sigma * 1.5, step=0.01, format="%.4f")
with colF:
    v_steps = st.number_input("σ steps", min_value=5, value=25, step=5)

if s_min >= s_max:
    st.error("S min must be < S max")
elif v_min >= v_max:
    st.error("σ min must be < σ max")
else:
    S_grid = np.linspace(float(s_min), float(s_max), int(s_steps))
    V_grid = np.linspace(float(v_min), float(v_max), int(v_steps))

    Z = np.zeros((len(V_grid), len(S_grid)), dtype=float)

    # compute grid
    for i, vol in enumerate(V_grid):
        for j, spot in enumerate(S_grid):
            if heat_option == "Call":
                Z[i, j] = price_call(S=spot, K=K, T=T, r=r, sigma=vol, q=q)
            else:
                Z[i, j] = price_put(S=spot, K=K, T=T, r=r, sigma=vol, q=q)

    fig, ax = plt.subplots()
    im = ax.imshow(
        Z,
        origin="lower",
        aspect="auto",
        extent=[S_grid[0], S_grid[-1], V_grid[0], V_grid[-1]],
        cmap="RdYlGn_r"
    )
    ax.set_xlabel("Spot (S)")
    ax.set_ylabel("Volatility (σ)")
    ax.set_title(f"{heat_option} Price Heatmap (K={K}, T={T}, r={r}, q={q})")
    fig.colorbar(im, ax=ax, label="Option Price")

    st.pyplot(fig)


st.divider()
# st.write("Sanity check (Put-Call Parity):")
# parity_lhs = call - put
# parity_rhs = S * math.exp(-q * T) - K * math.exp(-r * T)
# st.write(f"Call - Put = {parity_lhs:.6f}")
# st.write(f"S e^(-qT) - K e^(-rT) = {parity_rhs:.6f}")
# st.write(f"Diff = {(parity_lhs - parity_rhs):.6e}")