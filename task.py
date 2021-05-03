# Importing libraries
import numpy as np
import pandas as pd  # data processing
import datetime  # for datetime conversion
from pandas_datareader import data as pdr  # for loading Yahoo finance data

def csv_file_operation(df):
    # Concatenating Trader Name for convenience
    df["Trader_name"] = df["firstName"] + df["lastName"]  # Concatenateing Traders' name
    df['tradeDatetime'] = pd.to_datetime(df['tradeDatetime']) # Converting Datatype of column to "Datetime"
    df_amazon = df.loc[df["stockSymbol"] == "AMZN"]  # Slicing dataset for Amazon stock
    df_amazon['Date'] = df_amazon['tradeDatetime'].dt.date # Extracting date from tradeDatetime
    df_amazon['Date'] = pd.to_datetime(df_amazon['Date'], format='%Y-%m-%d') # Converting Datatype of column to "Datetime"
    return df_amazon  # returns Amazon data from given CSV file


def yahoo_file_operation(data):
    data["Date"] = data.index # creating "Date" column for merging
    data.reset_index(drop=True, inplace=True)
    data.columns = data.columns.droplevel(1)  #dropping secondary index
    return data # returns Data from Yahoo finance


def merged(df_amazon, data):
    merged = pd.merge(df_amazon, data, on='Date', how='outer')  #merging Amazon data with Yahoo finance data
    suspicious_high = merged[merged.iloc[:, 7] >= merged["High"]] # Condition for suspicious trader
    suspicious_low = merged[merged.iloc[:, 7] <= merged["Low"]] # Condition for suspicious trader
    suspicious = pd.concat([suspicious_high, suspicious_low])  # merging suspicious dataframe
    list_susp = suspicious["Trader_name"].value_counts()  # This returns suspicious traders list
    print(list_susp)  # Printing the result
    return list_susp # This is list of suxpicious traders



if __name__ == "__main__":
    # path of the dataset
    path = '/home/beast/PycharmProjects/Question_Answering/traders_data.csv'

    ##  initializing Parameters
    start = "2020-02-01"
    end = "2021-03-31"
    symbols = ["AMZN"]

    # Getting the data from yahoo finance
    data = pdr.get_data_yahoo(symbols, start, end)

    # Reading the csv file given
    df = pd.read_csv(path)

    merged(csv_file_operation(df), yahoo_file_operation(data))