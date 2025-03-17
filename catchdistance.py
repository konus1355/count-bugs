import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Trap Catch as a Function of Distance 🦋")

uploaded_file = st.file_uploader("Upload your CSV data", type=['csv'])

D = st.slider("Trap D50 (meters)", 10, 100, 26)
spTfer0 = st.slider("Probability at r=0 (spTfer(0))", 0.01, 1.0, 0.37)
R_max = st.number_input("Max dispersal (Rmax, meters)", value=1600)

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    r = data['r']  # Assume user has distance column
    spTfer = spTfer0 / (1 + (r/D)**2)
    spTfer[r > R_max] = 0
    
    fig, ax = plt.subplots()
    ax.scatter(r, spTfer, alpha=0.7)
    ax.set_xlabel('Distance from trap (m)')
    ax.set_ylabel('Probability of Capture (spTfer)')
    st.pyplot(fig)
