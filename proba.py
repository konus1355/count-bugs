import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('🦋 Interactive Absolute Density vs. Trap Catch')

st.sidebar.header("📌 Adjustable Parameters")

# User inputs
spTfer0 = st.sidebar.number_input('spTfer(0)', min_value=0.0001, max_value=1.0, value=0.37, step=0.01)
D50 = st.sidebar.number_input('D₅₀ (m)', min_value=0.1, value=26.0, step=0.1)
Rmax = st.sidebar.number_input('Rₘₐₓ (m)', min_value=1, value=1600, step=10)

# Chi-square quantile table
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
                   71.4202, 73.8099, 76.192, 78.5672, 80.9356, 83.2977, 85.6537]
}

chi2_df = pd.DataFrame(chi2_data)

# Calculate μ based on provided parameters
mu = 1 / (np.pi * (D50 ** 2) * np.log(1 + (1600 ** 2 / D50**2))) * (1 / spTfer0)

# Calculate densities for catches (M) from 0 to 30
Ms = chi2_df['M'].values
lower_bounds = (mu / 2) * chi2_df['Chi2_lower'] * 1000
upper_bounds = (mu / 2) * chi2_df['Chi2_upper'] * 1000
most_probable = mu * chi2_df['M'] * 1000

# Plot results
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(chi2_df['M'], most_probable, 'o-', color='blue', label='Most probable density')
ax.fill_between(chi2_df['M'], lower_bounds, upper_bounds, color='gray', alpha=0.3, label='95% Confidence Interval')

ax.set_xlabel('Trap Catch (M)')
ax.set_ylabel('Density (insects/ha)')
ax.set_title('Estimated Absolute Density vs. Trap Catch')
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Optionally display the dataframe clearly
result_df = pd.DataFrame({
    'Catch (M)': chi2_df['M'],
    'Lower Bound': lower_bound,
    'Most Probable': most_probable,
    'Upper Bound': upper_bounds
})

st.write("### 🌟 Detailed Density Estimates")
st.dataframe(result_df)
