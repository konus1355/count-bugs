import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trap Catch Density Estimator", page_icon="🦋")
st.title('🦋 Absolute Density vs. Trap Catch')

st.sidebar.header("📌 Adjustable Parameters (required)")

# Use text inputs with validation
spTfer0_input = st.sidebar.text_input("spTfer(0)", placeholder="Enter a value between 0 and 1")
D50_input = st.sidebar.text_input("D₅₀ (m)", placeholder="Enter a positive value")
Rmax_input = st.sidebar.text_input("Rₘₐₓ (m)", placeholder="Enter a positive value")

# Validate and convert inputs
valid_inputs = True

try:
    spTfer0 = float(spTfer0_input)
    if not (0 < spTfer0 <= 1):
        st.sidebar.error("spTfer(0) must be between 0 and 1")
        valid_inputs = False
except:
    if spTfer0_input:
        st.sidebar.error("spTfer(0) must be a number")
    valid_inputs = False

try:
    D50 = float(D50_input)
    if D50 <= 0:
        st.sidebar.error("D₅₀ must be a positive number")
        valid_inputs = False
except:
    if D50_input:
        st.sidebar.error("D₅₀ must be a number")
    valid_inputs = False

try:
    Rmax = float(Rmax_input)
    if Rmax <= 0:
        st.sidebar.error("Rₘₐₓ must be a positive number")
        valid_inputs = False
except:
    if Rmax_input:
        st.sidebar.error("Rₘₐₓ must be a number")
    valid_inputs = False

# Only proceed if all inputs are valid
if valid_inputs:
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
                       71.4202, 73.8099, 76.192, 78.5672, 80.9356, 83.2977,
                       85.6537]
    }

    chi2_df = pd.DataFrame(chi2_data)

    # μ calculation
    mu = 1 / (np.pi * (D50 ** 2) * np.log(1 + (Rmax ** 2 / D50 ** 2))) * (1 / spTfer0)

    # Compute densities
    Ms = chi2_df['M'].values
    lower_bounds = [(mu / 2) * chi2_df.loc[chi2_df['M'] == M, 'Chi2_lower'].values[0] * 10000 for M in Ms]
    upper_bounds = [(mu / 2) * chi2_df.loc[chi2_df['M'] == M, 'Chi2_upper'].values[0] * 10000 for M in Ms]
    most_probable = [mu * M * 10000 for M in Ms]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(Ms, most_probable, 'o-', color='blue', label='Most probable density')
    ax.fill_between(Ms, lower_bounds, upper_bounds, color='gray', alpha=0.3, label='95% Confidence Interval')

    ax.set_xlabel('Trap Catch (M)')
    ax.set_ylabel('Density (insects/ha)')
    ax.set_title('Trap Catch as a Function of Distance')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Output table
    result_df = pd.DataFrame({
        'Catch (M)': Ms,
        'Lower Bound': lower_bounds,
        'Most Probable': most_probable,
        'Upper Bound': upper_bounds
    })

    st.write("### 🌟 Absolute Density Estimates")
    st.dataframe(result_df)

else:
    st.warning("Please enter valid values for all parameters to generate results.")
