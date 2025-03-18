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

        # Check if r=0 is available
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
