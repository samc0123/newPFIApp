import pandas as pd 
import numpy as np
import os
import glob
from dotenv import load_dotenv
from shared_code.my_sql_utils import *


load_dotenv('PATH_TO_ENV')


def load_csv_to_df(main_path:str,fType:str) -> pd.DataFrame: 
    '''Load all csvs from given fp and return dataframe '''
    '''Returns a concatenated dataframe of '''
    # Read all files of given type from given path
    path_csv = os.path.join(main_path , f"*{fType}")
    all_files = glob.glob(path_csv)
    
    # Specify column structure from downloaded banks CSVs
    cols_downloaded_from_bank_statement = {
        'Chase_cc':np.asarray(['Transaction Date','Post Date','Description',\
            'Category','Type','Amount','Memo']),
        'BofA_cc':np.asarray(['Posted Date','Reference Number','Payee','Address'\
            ,'Amount']),
        'BofA_deposits': np.asarray(['Date','Description','Amount','Running Bal.'])
    }

    # Specify columns needed for processing 
    cols_to_keep_from_bank_statemts = {
        'Chase_cc':np.asarray(['Transaction Date','Description','Amount']),
        'BofA_cc':np.asarray(['Posted Date','Payee','Amount']),
        'BofA_deposits':np.asarray(['Date','Description','Amount'])
    }

    # Specify final dataframe column names 
    final_cols = ['datePosted','merchant','amount']


    # Import files into list for concatenation
    li = [] # list of final dataframes 

    for file in all_files:
        # Read current file into temporary dataframe
        temp_df = pd.read_csv(filepath_or_buffer=file,index_col=None, header=0)
        
        # Find statement type by checking headers of current statemnt and comparing with dict
        statement_type = [k for k,v in \
            cols_downloaded_from_bank_statement.items()\
                if np.array_equiv(a1=np.asarray(temp_df.columns.values),a2=v)].pop()
        
        # Keep the appropriate columns and add dataframe to list for concat
            # by popping the statement type and then using this val in the dict
            # to return the appropriate columns to keep from temp_df
        temp_df = temp_df[cols_to_keep_from_bank_statemts[statement_type]]
        # Reassign column names
        temp_df.columns = final_cols 


        # Add current df to be concated for final list of transactions
        li.append(temp_df)

    # Concat & format frame to return
    transaction_frame = pd.concat(objs=li,axis=0,ignore_index=True)

    # Replace commas in thousands #'s
    transaction_frame['amount'] = transaction_frame['amount'].replace(',','',regex=True)

    # Sort values 
    transaction_frame.sort_values(by='datePosted',ascending=False)
    
    # Add placeholder for categories 
    transaction_frame['category'] = pd.Series(dtype='string')
    return(transaction_frame)

def process_transaction_csv() -> pd.DataFrame:
    '''Process csvs and return in df format'''
    main_df = load_csv_to_df(main_path=os.environ.get("TRANSACTION_PATH"),fType='.csv')

    return main_df

def update_list_merchants(u_name:str,pw:str,host_name:str,db_name:str) -> str:
    '''Update the merchants table to include any new ones'''

    # Get current list of merchants 
    query = "SELECT merchant_name from merchants"
    cur_list_merchants = query_my_sql(u_name=u_name,pw=pw,host_name=host_name,db_name=db_name,query=query)

    # Print list of merchants 
    print(cur_list_merchants)

    return 'Sucess'



