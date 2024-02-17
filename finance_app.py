import pandas as pd 
import numpy as np 
import streamlit as st 
from shared_code.finance_processing import *
from shared_code.my_sql_utils import *
from dotenv import load_dotenv
load_dotenv("/Users/samchernov/Desktop/Personal/Financials/newFinancialApp2024/newPFIApp/venv/secrets.env")




#-------------------------- End Shared Functions ----------------------------------------#

#---------------------------Start Streamlit Config ----------------------------------------#


def main():
    # User details for MySQL: 
    user_my_sql = {
        "u_name": os.environ.get("mysql_uName"),
        "pw": os.environ.get("mysql_pw"),
        "db_name": os.environ.get("mysql_dbName"),
        "host_name": 'localhost'
    }
    st.set_page_config(
        page_title='Finance Dashboard',
        page_icon= '💸',
        layout='wide'
    )
    st.title('Real time Finance Dashboard')

    # Load the data 
    if pd.read_csv(filepath_or_buffer='tempDataStore.csv').empty:
        data = load_csv_to_df(main_path=os.environ.get("TRANSACTION_PATH"),fType='.csv')
    else:
        data = pd.read_csv(filepath_or_buffer='tempDataStore.csv')

    # Get the transaction categories
    allowable_categories = query_my_sql(u_name=user_my_sql["u_name"],\
                                        pw=user_my_sql["pw"],\
                                            db_name=user_my_sql["db_name"],
                                                host_name= user_my_sql["host_name"],\
                                                    query="SELECT category_name FROM transaction_categories")
    allowable_cat_text = []
    for cat in allowable_categories:
        allowable_cat_text.append(cat[0])
    print(data)
    edited_df = st.data_editor(data=data,use_container_width=True,\
                   column_config={
                        "category": st.column_config.SelectboxColumn(
                            "Transaction Category",
                            help="Category of the transaction",
                            width="medium",
                            options=allowable_cat_text,
                            required=True,
                        )
                    },
                    disabled=("datePosted","merchant","amount")
    )
    edited_df.to_csv('tempDataStore.csv',index=False)
    bar_chart_df = data
    bar_chart_df['amount'] = abs(bar_chart_df['amount']) # Make values
    print(bar_chart_df)
    st.bar_chart(
        data=bar_chart_df,
        x='category',
        y='amount'
    )
    update_list_merchants(u_name=user_my_sql["u_name"],\
                          pw=user_my_sql["pw"],\
                            host_name=user_my_sql["host_name"],\
                                db_name=user_my_sql["db_name"])

if __name__ == '__main__':
    main()