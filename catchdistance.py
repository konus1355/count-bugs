import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

st.title('🦋 Estimate D₅₀ from Trap Data')

uploaded_file = st.file_uploader("Upload CSV (columns: 'r', 'spTfer(r)')", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    if 'r' not in data.columns or 'spTfer(r)' not in data.columns:
        st.error("🚨 CSV must have columns 'r' and 'spTfer(r)'.")
    else:
        r = data['r'].values
        observed = data['spTfer(r)'].values

        if 0 in r:
            spTfer0 = data.loc[data['r'] == 0, 'spTfer(r)'].iloc[0]
            st.write(f"✅ Automatically detected spTfer(0): **{spTfer0:.3f}**")

            def spTfer_model(r, D50):
                return spTfer0 / (1 + (r / D50)**2)

            initial_guess = [np.median(r[r > 0])]
            bounds = (0.01, np.inf)

            try:
                popt, pcov = curve_fit(spTfer_model, r, observed, p0=initial_guess, bounds=bounds)
                D50_fit = popt[0]

                st.subheader('🌟 **Estimated D₅₀**')
                st.write(f"**D₅₀:** {D50_fit:.2f} m")

                r_fit = np.linspace(0, r.max(), 200)
                spTfer_fit = spTfer_model(r_fit, D50_fit)

                fig, ax = plt.subplots()
                ax.scatter(r, observed, color='blue', label='Observed')
                ax.plot(r_fit, spTfer_fit, color='red', label='Fitted model')
                ax.set_xlabel('Distance r (m)')
                ax.set_ylabel('Capture Probability (spTfer)')
                ax.legend()
                st.pyplot(fig)

            except RuntimeError:
                st.error("🚨 Fitting failed. Please check your data.")
        else:
            st.warning("⚠️ No measurement at r=0 found; estimating both spTfer(0) and D₅₀.")

            def spTfer_model_estimate(r, spTfer0, D50):
                return spTfer0 / (1 + (r / D50)**2)

            initial_guess = [observed.max(), np.median(r)]
            bounds = ([0.001, 0.01], [1.0, np.inf])

            try:
                popt, pcov = curve_fit(spTfer_model_estimate, r, observed, p0=initial_guess, bounds=bounds)
                spTfer0_fit, D50_fit = popt

                st.subheader('🌟 **Estimated Parameters**')
                st.write(f"**spTfer(0):** {spTfer0_fit:.3f}")
                st.write(f"**D₅₀:** {D50_fit:.2f} m")

                r_fit = np.linspace(0, r.max(), 200)
                spTfer_fit = spTfer_model_estimate(r_fit, spTfer0_fit, D50_fit)

                fig, ax = plt.subplots()
                ax.scatter(r, observed, color='blue', label='Observed')
                ax.plot(r_fit, spTfer_fit, color='green', label='Fitted model (estimated spTfer(0))')
                ax.set_xlabel('Distance r (m)')
                ax.set_ylabel('Capture Probability (spTfer)')
                ax.legend()
                st.pyplot(fig)

            except RuntimeError:
                st.error("🚨 Fitting failed. Please check your data.")
