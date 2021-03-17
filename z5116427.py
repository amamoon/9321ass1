import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import re
from pandas.core.arrays import sparse
from pandas.io.json import json_normalize

studentid = os.path.basename(sys.modules[__name__].__file__)

def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    exp_df = pd.read_csv(exposure, sep=';', decimal=',',dtype={
        'Covid_19_Economic_exposure_index':float,
        'Covid_19_Economic_exposure_index_Ex_aid_and_FDI':float,
        'Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import':float
    }, na_values='x')
    exp_df.rename(columns={'country':'Country'}, inplace=True)
    country_df = pd.read_csv(countries,
                            converters={'Cities': lambda x: [json.loads(x) for x in x.split("|||")]},
                            nrows=5)
    """mylist=[]
    for chunk in pd.read_csv(countries,converters={'Cities': lambda x: [json.loads(x) for x in x.split("|||")]},dtype={'Country':'string'}, low_memory=False, encoding='utf-8',chunksize=2):
        mylist.append(chunk)
    country_df=pd.concat(mylist,axis=0)"""
    cities_df = pd.json_normalize(country_df['Cities'][0])
    i = 1
    while i != 5:
        cities_to_df = pd.json_normalize(country_df['Cities'][i])
        cities_df = cities_df.append(cities_to_df)
        i += 1
    exp_df = exp_df.dropna()
    df1 = pd.merge(cities_df, exp_df, on='Country')
    df1 = df1.set_index('Country')
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df2 = df1.copy()
    df2 =df2.reset_index()
    avg_lat = pd.DataFrame()
    avg_lat = df2.groupby('Country').Latitude.mean()
    avg_long = pd.DataFrame()
    avg_long = df2.groupby('Country').Longitude.mean()
    df2 = pd.merge(df2, avg_lat, on='Country')
    df2 = pd.merge(df2, avg_long, on='Country')
    df2 = df2.rename(columns={'Latitude_y':'avg_latitude', 'Longitude_y':'avg_longitude', 'Latitude_x':'Latitude','Longitude_x':'Longitude'})
    df2=df2.set_index('Country')
    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    r = 6373
    wuhan_lat = math.radians(30.5928)
    wuhan_long = math.radians(114.3055)
    df3 = df2.copy()
    df3 = df3.reset_index()
    df3['avg_latitude'] = np.deg2rad(df3['avg_latitude'])
    df3['avg_longitude'] = np.deg2rad(df3['avg_longitude'])
    df3['distance_to_Wuhan'] =0.0
    df3['distance_to_Wuhan']=df3[['avg_latitude','avg_longitude','distance_to_Wuhan']].apply(lambda row: r * math.acos(math.sin(row[0])*math.sin(wuhan_lat) + math.cos(row[0])*math.cos(wuhan_lat)*math.cos(row[1]-wuhan_long)), axis=1)
    df3 = df3.drop(['avg_latitude','avg_longitude'], axis=1)
    df3 = df3.set_index('Country')
    df3 = df3.sort_values('distance_to_Wuhan')
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3


def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    continents_df = pd.read_csv(continents)
    df2_cei=pd.DataFrame()
    df2 = df2.reset_index()
    df2_cei = df2[['Country','Covid_19_Economic_exposure_index']]
    df4 = pd.merge(continents_df, df2_cei, on='Country')
    print(df4.dtypes)
    avg_cei = df4.groupby('Continent').Covid_19_Economic_exposure_index.mean()
    print(avg_cei)
    df4 = pd.merge(df4, avg_cei, on='Continent')
    df4 = df4.drop(['Country','Covid_19_Economic_exposure_index_x'], axis=1)
    df4 = df4.rename(columns={'Covid_19_Economic_exposure_index_y':'average_covid_19_Economic_exposure_index'})
    df4 = df4.drop_duplicates()
    df4 = df4.set_index('Continent')
    #################################################

    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
        
    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5


def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return lst


def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7


def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("exposure.csv", "Countries.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3(df2.copy(True))
    df4 = question_4(df2.copy(True), "Countries-Continents.csv")
    df5 = question_5(df2.copy(True))
    lst = question_6(df2.copy(True))
    df7 = question_7(df2.copy(True))
    question_8(df2.copy(True), "Countries-Continents.csv")
    question_9(df2.copy(True))
    question_10(df2.copy(True), "Countries-Continents.csv")