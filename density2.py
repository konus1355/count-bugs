import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

st.title('🦋 Absolute Density Estimator (All Data Points)')

uploaded_file = st.file_uploader("Upload CSV (columns: 'r', 'spTfer(r)')", type=['csv'])

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

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    if 'r' not in data.columns or 'spTfer(r)' not in data.columns:
        st.error("🚨 CSV must have columns 'r' and 'spTfer(r)'.")
    else:
        r = data['r'].values
        spTfer_r = data['spTfer(r)'].values

        if 0 in r:
            spTfer0 = spTfer_r[r == 0][0]
        else:
            st.error("🚨 Data must contain r=0 to determine spTfer(0).")
            st.stop()

        def model(r, D50):
            return spTfer0 / (1 + (r / D50)**2)

        popt, _ = curve_fit(model, r, spTfer_r, p0=[np.median(r[r > 0])], bounds=(0.01, np.inf))
        D50_fit = popt[0]

        Rmax = st.sidebar.number_input('Rₘₐₓ (m)', min_value=1, value=1600, step=10)
        mu = 1 / (np.pi * D50_fit**2 * np.log(1 + (Rmax**2 / D50_fit**2))) * (1 / spTfer0)

        densities = []
        for catch in spTfer_r:
            M = int(np.round(catch * 1000))  # Example conversion for demonstration
            if M in chi2_df['M'].values:
                chi2_lower = chi2_df.loc[chi2_df['M'] == M, 'Chi2_lower'].iloc[0]
                chi2_upper = chi2_df.loc[chi2_df['M'] == M, 'Chi2_upper'].iloc[0]

                lower = (mu / 2) * chi2_lower * 1000
                upper = (mu / 2) * chi2_upper * 1000
                most_probable = mu * M * 1000

                densities.append((lower, most_probable, upper))
            else:
                densities.append((np.nan, np.nan, np.nan))

        density_df = pd.DataFrame(densities, columns=['Lower Bound', 'Most Probable', 'Upper Bound'])
        result_df = pd.concat([data, density_df], axis=1)

        st.write("### 🌟 Density Estimation Results")
        st.dataframe(result_df)

        plt.figure(figsize=(10, 6))
        plt.plot(r, density_df['Most Probable'], 'o-', label='Most Probable', color='blue')
        plt.fill_between(r, density_df['Lower Bound'], density_df['Upper Bound'], color='blue', alpha=0.2, label='95% CI')
        plt.xlabel('Distance r (m)')
        plt.ylabel('Density (insects/ha)')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

