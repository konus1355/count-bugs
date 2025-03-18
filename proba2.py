import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# --- Page title ---
st.title('🦋 Estimate D₅₀ from Your Trap Data')

# --- User uploads CSV ---
uploaded_file = st.file_uploader("Upload your CSV file with columns 'distance' and 'spTfer_r':", type="csv")

# Define your model function
def spTfer_model(r, spTfer0, D50):
    return spTfer0 / (1 + (r / D50)**2)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    if 'distance' not in data.columns or 'spTfer_r' not in data.columns:
        st.error("🚨 Your file must contain 'distance' and 'spTfer_r' columns.")
    else:
        r = data['distance'].values
        observed = data['spTfer_r'].values

        # Estimate spTfer0 directly from data at distance closest to 0
        spTfer0_guess = observed[r.argmin()]
        
        # Initial guess for D50
        initial_guess = [spTfer0_guess, np.median(r)]

        try:
            # Fit the model
            popt, pcov = curve_fit(spTfer_model, r, observed, p0=initial_guess, bounds=(0, np.inf))
            spTfer0_fit, D50_fit = popt

            # Display results
            st.subheader("🎯 Fitted Parameters")
            st.write(f"**spTfer(0)**: {spTfer0_fit:.3f}")
            st.write(f"**D₅₀**: {D50_fit:.2f} m")

            # Plot observed vs fitted
            r_fit = np.linspace(0, r.max(), 200)
            spTfer_fit = spTfer_model(r_fit, spTfer0_fit, D50_fit)

            fig, ax = plt.subplots()
            ax.scatter(r, observed, label='Observed data', color='blue')
            ax.plot(r_fit, spTfer_fit, label='Fitted model', color='red')
            ax.set_xlabel('Distance (m)')
            ax.set_ylabel('Capture Probability (spTfer)')
            ax.legend()
            st.pyplot(fig)

        except RuntimeError:
            st.error("🚨 Model fitting failed. Check your data quality and ensure it follows expected patterns.")
