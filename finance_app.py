import pandas as pd 
import numpy as np 
import streamlit as st 
from shared_code.finance_processing import *


#-------------------------- Start Shared Functions ----------------------------------------#





#-------------------------- End Shared Functions ----------------------------------------#

#---------------------------Start Streamlit Config ----------------------------------------#

st.set_page_config(
    page_title='Finance Dashboard',
    page_icon= '💸',
    layout='wide'
)

st.title('Real time Finance Dashboard')
data = process_transaction_csv()
print(data)
st.table(data=data)