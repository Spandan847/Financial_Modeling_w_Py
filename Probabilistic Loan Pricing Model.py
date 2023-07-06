#!/usr/bin/env python
# coding: utf-8

# # Startup Lending Model (Project 2)
# ## Overview
# This model considers that probabilistic loan pricing, from bank's/ lender's perspective, based on different default probabilities of bankruptcy. An entity takes the loan from the bank and pays interests on the amount every single year. On the last year, it pays the full principal amount. However, there are different, pre-assumed, probabilities of default that the bank (we) have to consider over a specific amount of loan time. default probabilities will be calculate by the formula, pt_default = pt-1_default * Decaydefault, where Decaydefault is a constant. For the year of default and the year after, the lender will not collect any cash flows, and then two years after default, the lender will collect rrecoverypricemachine. Note that this means the number of years of cash flows may be up to two years greater than the life of the loan. 
# ## Main Question
# You are the commercial loan analyst trying to decide if this loan makes sense for the bank. You want to give the lending officer all the information she would need to negotiate a rate for this loan. Given the inputs, what is the expected IRR of the loan for a variety of interest rates on the loan? The lending officer would like you to evaluate rates in 5% increments from 30% to 40%.
# The lending officer is also worried that she may have estimated pdefault1 incorrectly. She is hoping for the answers to the above questions considering that pdefault1 may vary. Evaluate the above questions for pdefault1 = 0.1, 0.3 in addition to the base case of 0.2. Finally, the lending officer is unsure for how long she should extend the loan. So she would like to see all of the previously mentioned results with loan lifes of 5, 10, and 20 years. You should visualize the results of your model through graphs, conditional formatting, etc.
# 
# ## Table of Contents
# - [**Setup**](#Setup): Packages' and libraries' import
# - [**Input**](#Inputs): All required inputs are stored as dataclass
# - [**Model**](#Setup): Incorporates different functions to run the model
# - [**Output**](#Output): Displays the IRR values as datatable with color gradient based on the values

# ## Setup
# * All necessary packages and libraries are imported in this section.

# In[1]:


import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from tqdm import tqdm
from IPython.display import display


# ## Input
# * All required inputs are stored as dataclass in this section.

# In[2]:


# Define the LoanParameters class
@dataclass
class LoanParameters:
    price_machine: float = 1000000
    loan_life: int = 5
    initial_default: float = 0.2
    default_decay: float = 0.9
    final_default: float = 0.4
    recovery_rate: float = 0.4
    interest: float = 0.3
    num_iterations: int = 10


# ## Model
# * My main model starts from this section
# * The model incorporates several distinct functions to calculate:
#     * Default Probabilities for a specific loan life
#     * Unadjusted cash flow for the specific loan life and interest rate
#     * Adjusted cash flow based on default probabilities, interest rates, and unadjusted cash flows
#     * Internal Rate of Return (IRR) based on the adjusted cash flows
#     * Iterated values of IRR, incorporating randomess from defined number of iterations, with each IRR's Standard Deviation   adjusted average amount

# #### Function to Calculate Default Probability

# In[3]:


# Function to calculate default probability
def calculate_default_probability(loan_life, default_decay, initial_default, final_default, recovery_rate):
    default_probability_values = []
    for i in range(1, loan_life + 3):
        if i == 1:
            df = initial_default
            default_probability_values.append(df)
        if loan_life > i > 1:
            df = default_decay * initial_default
            default_probability_values.append(df)
            initial_default = df
        if loan_life == i:
            df = final_default
            default_probability_values.append(df)
        if i == loan_life + 1:
            df = 0
            default_probability_values.append(df)
        if i == loan_life + 2:
            df = recovery_rate
            default_probability_values.append(df)
    return default_probability_values


# #### Function to Calculate Unadjusted Cash Flow

# In[4]:


# Function to calculate unadjusted cash flow
def calculate_unadjusted_cashflow(price_machine, interest_rate, loan_life):
    unad_cf = []
    for i in range(1, loan_life + 3):
        if i == 1:
            uad_cf = -price_machine + (interest_rate * price_machine)
            unad_cf.append(uad_cf)
        if loan_life > i > 1:
            uad_cf = price_machine * interest_rate
            unad_cf.append(uad_cf)
        if i == loan_life:
            uad_cf = price_machine
            unad_cf.append(uad_cf)
        if loan_life < i < loan_life + 3:
            uad_cf = 0
            unad_cf.append(uad_cf)
    return unad_cf


# #### Function to Calculate Adjusted Cash Flow

# In[5]:


# Function to calculate adjusted cash flow
def calculate_adjusted_cashflow(initial_default, probabilities_default, unadjusted_cashflows, recovery_rate, price_machine, interest_rate, loan_life):
    adjusted_cash_flows = []
    for defaults, unadjusted_amt in zip(probabilities_default, unadjusted_cashflows):
        if defaults == initial_default:
            interest_adjusted_amt = interest_rate * price_machine
            with_def_prob_amt = interest_adjusted_amt * (1 - defaults)
            adjusted_cash = -price_machine + with_def_prob_amt
            adjusted_cash_flows.append(adjusted_cash)
        elif defaults == recovery_rate and unadjusted_amt == price_machine:
            new_unadjusted_money = (interest_rate * price_machine) * (1 - defaults)
            adjusted_cash_flows.append(new_unadjusted_money)
        elif defaults == recovery_rate and unadjusted_amt != price_machine:
            adjusted_cash = recovery_rate * price_machine
            adjusted_cash_flows.append(adjusted_cash)
        elif defaults == 0 and unadjusted_amt == 0:
            adjusted_cash_flows.append(0)
        else:
            adjusted_cash = unadjusted_amt * (1 - defaults)
            adjusted_cash_flows.append(adjusted_cash)
    return adjusted_cash_flows


# #### Function to Calculate the Internal Rate of Return (IRR)

# In[6]:


# Function to calculate IRR
def calculate_irr(cash_flows):
    return npf.irr(cash_flows)


# #### Function to run Interations on all Parameters in the Model Inputs

# In[7]:


def run_iterations(parameters, num_iterations=100):
    results = []

    interest_rates = np.arange(0.3, 0.41, 0.05)  # Interest rates in 5% increments
    default_probabilities = [0.1, 0.2, 0.3]  # Default probabilities to evaluate
    loan_lives = [5, 10, 20]  # Loan lives to evaluate

    pbar = tqdm(total=num_iterations, desc='Running iterations', unit='iter')

    # Lists to store individual output values
    irr_values = []
    interest_rate_values = []
    default_prob_values = []
    loan_life_values = []

    for _ in range(num_iterations):
        for interest_rate in interest_rates:
            for default_probability in default_probabilities:
                for loan_life in loan_lives:
                    parameters.interest = interest_rate
                    parameters.initial_default = default_probability
                    parameters.loan_life = loan_life

                    # Calculate the required values
                    prob_defaults = calculate_default_probability(
                        parameters.loan_life,
                        parameters.default_decay,
                        parameters.initial_default,
                        parameters.final_default,
                        parameters.recovery_rate
                    )
                    unadjusted_cash_flows = calculate_unadjusted_cashflow(
                        parameters.price_machine,
                        parameters.interest,
                        parameters.loan_life
                    )
                    adjusted_amount_of_cashflow = calculate_adjusted_cashflow(
                        parameters.initial_default,
                        prob_defaults,
                        unadjusted_cash_flows,
                        parameters.recovery_rate,
                        parameters.price_machine,
                        parameters.interest,
                        parameters.loan_life
                    )
                    irr = calculate_irr(adjusted_amount_of_cashflow)

                    # Store the individual output values
                    irr_values.append(irr)
                    interest_rate_values.append(interest_rate)
                    default_prob_values.append(default_probability)
                    loan_life_values.append(loan_life)

                    result = {
                        'Interest Rate':"{:.2%}".format(interest_rate),
                        'Loan Life': loan_life,
                        'Initial Default Probability': "{:.2%}".format(default_probability),
                        'IRR': irr
                    }
                    results.append(result)

                    pbar.set_postfix({'Progress': f'{(len(results) / num_iterations) * 100:.2f}%'})
                    pbar.update(1)  # Update the progress bar

    pbar.close()  # Close the progress bar

    # Create a DataFrame with the results
    df_results = pd.DataFrame(results)

    # Calculate the average values of individual outputs
    average_results = df_results.groupby(['Interest Rate', 'Loan Life', 'Initial Default Probability']).mean().reset_index()

    # Calculate the standard deviation of IRR values
    std_dev = np.std(irr_values)

    # Modify the output values with the standard deviation
    average_results['IRR'] = average_results['IRR'] - std_dev

    # Create a color map for IRR values (reversed)
    cmap = sns.color_palette("RdYlGn", as_cmap=True)

    # Create the data table with color gradient
    data_table = pd.pivot_table(
        average_results,
        values='IRR',
        index=['Interest Rate', 'Loan Life'],
        columns='Initial Default Probability',
        fill_value=0
    )

    # Apply the color map to the data table
    styled_table = data_table.style.background_gradient(cmap=cmap)
    
    # Format IRR values as percentage with 2 decimal places
    styled_table = styled_table.format("{:.2%}")
    
    return styled_table


# In[8]:


# Create an instance of LoanParameters
loan_params = LoanParameters()


# ## Output
# * This section runs all the functions in the model to get the IRR values for respective variables

# #### Running Iterations

# In[9]:


# Run iterations and get the results
results_table= run_iterations(loan_params)


# #### Displaying Results

# In[10]:


display(results_table)


# In[ ]:




