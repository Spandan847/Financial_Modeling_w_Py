#!/usr/bin/env python
# coding: utf-8

# # Overview 
# You Work for new startup that is trying to manufacture phones. You are tasked with building a model which will help determine how many machines to invest in and how much to spend on marketing.Each machine produces noutput phones per year. Each phone sells for $pphone and costs $cphones in variable costs to produce. After nlife years, the machine can no longer produce output,but may be scrapped for $pscrap. The machine will not be replaced, so you may end up with zero total output before your model time period ends. Equity investment is limited, so in each year you can spend cmachine to either buy a machine or buy advertisements. In the first year you must buy a machine. Any other machine purchases must be made one after another (advertising can only begin after machine buying is done). Demand for your phones start at d1. Each time you advertise, demand increases by gd% The prevailing market insterest rate is r. 

# # Notes
# * You may limit your model to 20 years and a maximum of 5 machines if it is helpful
# * For simplicity, assume that cmachine is paid in every year, even after all machines have shut down
# * Ensure that you can change the inputs and the outputs change as expected
# * For simplicity, assume that fractional phones can be sold, you do not need to round the quantity transacted.

# # Mobile Phones Startup Model
# 
# - [**Setup**](#Setup): Runs any imports and other setup
# - [**Input**](#Inputs): All necessary information to calculate the output of the project is inserted as dataclass
# - [**Machine&AD**](#Machine&AD): Determines the net cash inflow per yer from machine and advertising section
# - [**Revenue**](#Revenue): Determines the the net cash inflow per yer from machine and advertising section
# - [**CashFlow**](#CashFlow): Takes in the output of net cash flow from machine/ad section and revenue section to determine yearly cash flow in the company
# - [**NPVSection**](#NPVSection): Calculates the Net Present Value of the company by taking in yearly Cash Flow and Market Interest Rate

# ## Setup 
# All required packages are imported here

# In[27]:


import numpy_financial as npf
import matplotlib.pyplot as plt


# ## Inputs
# * All inputs will be loaded in this section under their respective criteria

# ### Machines Input
# * The following inputs are loaded here: Number of phones, scrap value of machine, cost per Machine or Advertising, number of years of life per machine

# In[7]:


from dataclasses import dataclass
@dataclass
class Machine_Inputs:
    number_of_phones: int = 100000
    scrap_value_of_machine: int = 50000
    cost_per_admachine: int = 1000000
    number_yrs_life_machine: int = 10
model_data1= Machine_Inputs()
model_data1


# ### Revenue Inputs
# * The following inputs are loaded here: price per phone, variable cost per phone, initial demand, demand growth per advertisement

# In[8]:


from dataclasses import dataclass
@dataclass
class Revenue_Inputs:
    price_per_phone: int = 500
    variable_cost_per_phone: int = 250
    initial_demand: int = 100000
    demand_growth_per_ad: float = 0.2
model_data2= Revenue_Inputs()
model_data2


# ### Business Decision Inputs
# * The following inputs are loaded here: number of machines

# In[9]:


from dataclasses import dataclass
@dataclass
class Business_Inputs:
    number_of_machines: int = 5
model_data3 = Business_Inputs()
model_data3


# ### TVM Inputs
# * The following inputs are loaded here: Interest Rate

# In[10]:


from dataclasses import dataclass
@dataclass
class TVM_Inputs:
    interest_rate: float = 0.05
model_data4 = TVM_Inputs()
model_data4


# ### Machine&AD
# * We find the total cash inflows and outflows at the end of this section

# In[33]:


cost_machines_ad=[]
for machine_yrs in range(1, 21):
    if machine_yrs < 2:
        cost_machine = machine_yrs * model_data1.cost_per_admachine
        print (f'Cost of Machine/Ad: Year {machine_yrs} = ${cost_machine}')
        cost_machines_ad.append(cost_machine)
        machine_yrs= machine_yrs + 1
    elif machine_yrs>= 2:
        num = machine_yrs - 1
        reduced_num = machine_yrs - num
        cost_machine2 = reduced_num * model_data1.cost_per_admachine
        cost_machines_ad.append(cost_machine2)
        print (f'Cost of Machine/Ad: Year {machine_yrs} = ${cost_machine2}')
        num = num + 1
        machine_yrs = machine_yrs + 1
cost_machines_ad


# In[13]:


# Running number of machines on every year
yr_machine1 = 11
yr_machine2 = 12
yr_machine3 = 13
yr_machine4 = 14
yr_machine5 = 15
machines_at_operations=[]
for operating_machine in range (1,21):
    if operating_machine < 6:
        mach = operating_machine
        machine_at_operation = mach
        machines_at_operations.append(machine_at_operation)
        operating_machine = operating_machine + 1
        operating_machine= operating_machine + 1
for i in range (6,11):
    machines_at_operations.append(5)
machines_at_operations
a= 1
for i in range (11,21):
    if i==yr_machine1 or i==yr_machine2 or i==yr_machine3 or i==yr_machine4 or i==yr_machine5:
        operations = 5
        updated= operations - a
        machines_at_operations.append(updated)
        a=a+1
        i= i+1
    else:
        machines_at_operations.append(0)
machines_at_operations


# In[14]:


cash_inflows=[]
for i in range(1,21):
    if i <=10:
        cash_inflows.append(0)
        i =i +1
    elif i>10 and i <=15:
        cash_inflows.append(model_data1.scrap_value_of_machine)
        i = i+ 1
    else:
        cash_inflows.append(0)
cash_inflows


# In[15]:


print(f'Our cash inflows for 20 years in machine ad section = {cash_inflows}')
print(f'Our cash outflows for 20 years in machine ad section={cost_machines_ad}')


# In[16]:


net_cash_inflow_per_year = []
years= min(len(cost_machines_ad), len(cash_inflows))
for year in range(years):
    net_cash_inflow = cash_inflows[year]-cost_machines_ad[year]
    net_cash_inflow_per_year.append(net_cash_inflow)
net_cash_inflow_per_year


# ## Revenue
# * We calculate the total cash inflows and outflows from this section

# In[17]:


total_phones_demanded=[]
demand1= model_data2.initial_demand
for year in range (1,21):
    if year <6:
        demand = model_data2.initial_demand
        total_phones_demanded.append(demand)
        year=year+1
    elif year>=6:
        changed_demand= demand1 * model_data2.demand_growth_per_ad
        new_demand= changed_demand + demand1
        total_phones_demanded.append(round(new_demand))
        demand1= new_demand
        year=year+1
total_phones_demanded


# In[18]:


# Calculates the number of phones produced based on the machine
phones_produced=[]
for active_machine in machines_at_operations:
    produced_phones = active_machine * model_data1.number_of_phones
    phones_produced.append(produced_phones)
phones_produced


# In[19]:


# We calculate the revenue from the phone comparing the list 'phones_produced' & 'total_phones_demanded'
cash_inflows_revenue_from_selling_phones=[]
for produced, demanded in zip(phones_produced, total_phones_demanded):
    if produced > demanded:
        result = demanded * model_data2.price_per_phone
    else:
        result = produced * model_data2.price_per_phone
    cash_inflows_revenue_from_selling_phones.append(result)
print(cash_inflows_revenue_from_selling_phones)  


# In[20]:


# we calculate the cash outflows from cosidering the cost of the demanded phones
cash_outflows_cost=[]
for produced, demanded in zip(phones_produced, total_phones_demanded):
    if produced < demanded:
        result= produced * model_data2.variable_cost_per_phone
    else:
        result= demanded * model_data2.variable_cost_per_phone
    cash_outflows_cost.append(round(result))
cash_outflows_cost


# In[22]:


# we find the net cash inflow from revenue section
net_cash_inflows_revenue_sec=[]
for inflow, outflow in zip(cash_inflows_revenue_from_selling_phones, cash_outflows_cost):
    net_cash = inflow - outflow
    net_cash_inflows_revenue_sec.append(round(net_cash))
net_cash_inflows_revenue_sec


# ## CashFlow 

# In[24]:


startup_cash_flow_per_year =[]
for revenue1, revenue2 in zip(net_cash_inflows_revenue_sec, net_cash_inflow_per_year):
    cash_flow_value = revenue1 + revenue2
    startup_cash_flow_per_year.append(round(cash_flow_value))
startup_cash_flow_per_year


# ## NPVSection
# * We make use of the cash flow value for 20 yrs which is stored in the list 'startup_cash_flow_per_year' and by using the interest rate in TVM inputs, we calculate the NPV

# In[37]:


net_present_value=0
for i, cash_flow in enumerate(startup_cash_flow_per_year):
    present_value = cash_flow/(1+model_data4.interest_rate)**(i+1)
    net_present_value= net_present_value + present_value
print(f'Net Present Value is ${round(net_present_value)}')


# ## Visualization
# - We take in different outputs and will visualize the data below

# In[30]:


plt.plot(net_cash_inflows_revenue_sec, startup_cash_flow_per_year)
plt.xlabel('Net Cash Flow From Revenue Section')
plt.ylabel('Startup Cash Flow')
plt.title('Cash Flow From Revenue Against Net Cash Flow of the Company')
plt.show()


# In[31]:


plt.plot(net_cash_inflow_per_year, startup_cash_flow_per_year)
plt.xlabel('Net Cash Flow From MachineAd Section')
plt.ylabel('Startup Cash Flow')
plt.title('Cash Flow From Machine/Ad Against Net Cash Flow of the Company')
plt.show()

