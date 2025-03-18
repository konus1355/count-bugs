import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

st.title('🦋 Estimate D₅₀ from Trap Data')

uploaded_file = st.file_uploader("Upload CSV (columns: 'r', 'spTfer(r)')", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Check explicitly for required columns
    if 'r' not in data.columns or 'spTfer(r)' not in data.columns:
        st.error("🚨 CSV must have columns 'r' and 'spTfer(r)'.")
    else:
        # Automatically use observed spTfer(0) from data (r=0)
        if 0 in data['r'].values:
            spTfer0 = data.loc[data['r'] == 0, 'spTfer(r)'].iloc[0]
            st.write(f"✅ Automatically detected spTfer(0): **{spTfer0:.3f}**")

            r = data['r'].values
            observed = data['spTfer(r)'].values

            # Define model clearly
            def spTfer_model(r, D50):
                return spTfer0 / (1 + (r / D50)**2)

            # Initial guess
            initial_guess = [np.median(r[r > 0])]

            # Fit the model
            try:
                popt, pcov = curve_fit(spTfer_model, r, observed, p0=initial_guess, bounds=(0, np.inf))
                D50_fit = popt[0]

                st.subheader('🌟 **Estimated D₅₀**')
                st.write(f"**D₅₀:** {D50_fit:.2f} m")

                # Plot observed vs fitted
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
            st.error("🚨 Your dataset must include a measurement at r = 0.")
