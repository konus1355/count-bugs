import streamlit as st
import numpy as np
import pandas as pd

st.title('🦋 Absolute Population Density Estimator')

st.sidebar.header("📌 Input Parameters")

# User inputs
spTfer0 = st.sidebar.number_input('spTfer(0)', min_value=0.0001, max_value=1.0, value=0.37, step=0.01)
D50 = st.sidebar.number_input('D₅₀ (m)', min_value=0.1, value=26.0, step=0.1)
Rmax = st.sidebar.number_input('Rₘₐₓ (m)', min_value=1, value=1600, step=10)
M = st.sidebar.number_input('Trap catch (M)', min_value=0, value=1, step=1)

# Chi-square quantile table provided by the user
chi2_data = {
    'M': np.arange(0, 31),
    'Chi2_lower': [0, 0.0506356, 0.484419, 1.23734, 2.17973, 3.24697, 4.40379,
                   5.62873, 6.90766, 8.23075, 9.59078, 10.9823, 12.4012,
                   13.8439, 15.3079, 16.7908, 18.2908, 19.8063, 21.3359,
                   22.8785, 24.433, 25.9987, 27.5746, 29.1601, 30.7545,
                   32.3574, 33.9681, 35.5863, 37.2116, 38.8435, 40.4817],
    'Chi2_upper': [7.37776, 11.1433, 14.4494, 17.5345, 20.4832, 23.3367,
                   26.1189, 28.8454, 31.5264, 34.1696, 36.7807, 39.3641,
                   41.9232, 44.4608, 46.9792, 49.4804, 51.966, 54.4373,
                   56.8955, 59.3417, 61.7768, 64.2015, 66.6165, 69.0226,
                   71.4202, 73.8099, 76.192, 78.5672, 80.9356, 83.2977,
                   85.6537]
}

chi2_df = pd.DataFrame(chi2_data)

# Density multiplier (μ) calculation
mu = 1 / (np.pi * (D50**2) * np.log(1 + (Rmax**2 / D50**2))) * (1 / spTfer0)

# Look up Chi-square values based on trap catch M
if M in chi2_df['M'].values:
    chi2_lower = chi2_df.loc[chi2_df['M'] == M, 'Chi2_lower'].iloc[0]
    chi2_upper = chi2_df.loc[chi2_df['M'] == M, 'Chi2_upper'].iloc[0]

    # Calculate densities
    lower_bound = (mu / 2) * chi2_lower * 1000
    upper_bound = (mu / 2) * chi2_upper * 1000
    most_probable = mu * M * 1000

    st.subheader("🌟 Density Estimation Results")
    st.write(f"**Lower bound (95%):** {lower_bound:.2f} insects/ha")
    st.write(f"**Most probable density:** {most_probable:.2f} insects/ha")
    st.write(f"**Upper bound (95%):** {upper_bound:.2f} insects/ha")
else:
    st.error("🚨 Catch number exceeds available quantile data.")
