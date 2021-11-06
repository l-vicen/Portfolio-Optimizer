import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Visualizing Central Limit Theorem")

POP_MIN, POP_MAX = st.sidebar.slider('Select the population range (Example: range of age is 0-100)',0, 10000, (0, 1000))


pop_size = st.sidebar.slider(label="Choose the Population size ('N') - Creates a population of size 'N' within the population range",
          min_value=1000,
          max_value=20000,
          value=5000,
          step=10)

    
@st.cache
def generate_population():
    np.random.seed(11)
    population = np.random.randint(low=POP_MIN, high=POP_MAX, size=pop_size)
    return population

population = generate_population()
st.sidebar.write(f'(Population mean, std): ({np.round(np.mean(population),2)}, {np.round(np.std(population),2)})')

          
sample_size = st.sidebar.slider(label='Choose the sample size (n)',
          min_value=10,
          max_value=2000,
          value=100,
          step=10)

sample_number = st.sidebar.slider(label='Choose the number of samples',
          min_value=10,
          max_value=2000,
          value=100,
          step=10)


@st.cache
def generate_samples():
          np.random.seed(11)
          sample_index = np.random.randint(low=0, high=len(population), size=(sample_number * sample_size))
          sample = population[sample_index].reshape(sample_number, sample_size)
          sample_means = np.mean(sample, axis=1)
          return sample_means

          
sample_means = generate_samples()

fig = plt.figure()
plt.hist(sample_means,density=True)
plt.axis("off")
plt.title("Sampling distribution of sample means")
st.pyplot(fig)

fig1 = plt.figure()
plt.hist(population,density=True)
plt.axis("off")
plt.title("Population distribution")
st.pyplot(fig1)

st.sidebar.write(f'(Mean, std of sample means): ({np.round(np.mean(sample_means), 2)}, {np.round(np.std(sample_means), 2)})')
st.sidebar.write(f'pop std / sqrt(n): {np.round(np.std(population) / np.sqrt(sample_size), 2)}')