import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date
import warnings
warnings.filterwarnings("ignore")


df1 = pd.read_csv("Date_Page.csv")
df2 = pd.read_csv("Date_Page (2).csv")
df3 = pd.read_csv("Date_Page (3).csv")

df_country = pd.read_csv("country.csv")
df_city =pd.read_csv("city.csv")
df_browser = pd.read_csv("browser.csv")


df_country["Users"]= df_country["Users"].str.replace(",",'')
df_country["Bounce Rate"] = df_country["Bounce Rate"].str.replace("%",'')
df_country.dropna(how="any",inplace=True)
df_country["Users"] = df_country["Users"].astype(int)
df_country["Bounce Rate"] = df_country["Bounce Rate"].astype(float)
df_city["Users"] = df_city["Users"].str.replace(",",'')
df_city["Users"]=df_city["Users"].astype(int)
df_city.dropna(how="any",inplace=True)
df_city1 = df_city.sort_values(by="Users",ascending=False)[0:20]

df = pd.concat([df1,df2,df3],axis=0)
df.dropna(how="any",inplace=True)
df_browser["Users"] = df_browser["Users"].str.replace(",",'')
df_browser["Users"]=df_browser["Users"].astype(int)

def name(x):
    try:
        x = x.split("/")[4].replace("-",' ')
    except:
        pass
    return x
df["Page"]=df["Page"].apply(name)

def time(x):
    x =  date(int(x[0:4]),int(x[4:6]),int(x[6:9]))
    return x
df["Date"]=df["Date"].apply(time)

df_final = df.iloc[:,0:5]

def avgt(x): 
    x = x.split(":")[1:]
    x = int(x[0])*60+int(x[1])
    return x

df_final["Avg. Time on Page"]=df_final["Avg. Time on Page"].apply(avgt)
df_final["Year"]=df_final["Date"].apply(lambda x:x.year)
df_final["Month"]=df_final["Date"].apply(lambda x:x.month)
df_final["Day"]=df_final["Date"].apply(lambda x:x.day)

df_final["Pageviews"]=df_final["Pageviews"].astype(int)
df_final["Unique Pageviews"]= df_final["Unique Pageviews"].astype(int)

df_final["Weekday"]= df_final["Date"].apply(lambda x:x.strftime("%A"))
df_final["Month_n"]= df_final["Date"].apply(lambda x:x.strftime("%B"))


st.write("Total number of pages viewed till now : ",df_final["Pageviews"].sum())
st.write("Total hours spend on the website by the visitors in hours : ",df_final["Avg. Time on Page"].sum()/3600)


st.title('Line Charts')
option = st.selectbox("",('Day wise', 'Monthtly wise', 'Cumulative Daily wise','Averge time on the Website Daily in seconds wise'))

st.write('You selected:', option)

if option=='Day wise' :
    st.line_chart(df_final.groupby("Date")["Pageviews"].sum())
if option=='Monthtly wise':
    st.line_chart(df_final.groupby("Month")["Pageviews"].sum())
if option =="Cumulative Daily wise":
    st.line_chart(df_final.groupby("Day")["Pageviews"].sum())

if option =='Averge time on the Website Daily in seconds wise':
    st.line_chart(df_final.groupby("Date")["Avg. Time on Page"].sum())



st.title('Bar Chart ')
option1 = st.selectbox("",('Cumulative Monthly Count' ,'Cumulative Daily Count'))

st.write('You selected:', option1)

if option1 =="Cumulative Monthly Count":
    index= df_final.groupby(["Month_n"])["Pageviews"].sum().index
    values = df_final.groupby("Month_n")["Pageviews"].sum().values
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(index,values)
    ax.set_xlabel("Months",fontsize=10)
    ax.set_ylabel("Count of Users",fontsize=10)
    ax.set_xticklabels(index,rotation=90 )
    st.pyplot(fig)
    


if option1=="Cumulative Daily Count":
    index= df_final.groupby(["Weekday"])["Pageviews"].sum().index
    values = df_final.groupby("Weekday")["Pageviews"].sum().values
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(index,values)
    ax.set_xlabel("Days",fontsize=10)
    ax.set_ylabel("Count of Users",fontsize=10)
    ax.set_xticklabels(index,rotation=90 )
    st.pyplot(fig)








def avgt(x): 
    x = x.split(":")[1:]
    x = int(x[0])*60+int(x[1])
    return x
df_country["Avg. Session Duration"]=df_country["Avg. Session Duration"].apply(avgt)
df_country["Pages / Session"] = df_country["Pages / Session"].astype(float)





st.title("Bar Charts")
option2 = st.selectbox("",('Number of visitors from different countries Top 5' ,'Number of visitors from different cities Top 20',
                           'Visitors as per Browser','Top 10 Page Viewed on the Website','Avg. Session Duration country wise Top 10'))

st.write('You selected:', option2)

if option2=='Number of visitors from different countries Top 5':
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df_country["Country"][0:5],df_country["Users"][0:5])
    ax.set_xlabel("Country",fontsize=10)
    ax.set_ylabel("Count of Users",fontsize=10)
    ax.set_xticklabels( df_country["Country"][0:5],rotation=90 )
    st.pyplot(fig)

if option2=="Avg. Session Duration country wise Top 10":
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df_country["Country"][0:10],df_country["Avg. Session Duration"][0:10])
    ax.set_xlabel("Country",fontsize=10)
    ax.set_ylabel("Time in seconds",fontsize=10)
    ax.set_xticklabels( df_country["Country"][0:10],rotation=90 )
    st.pyplot(fig)


if option2=="Number of visitors from different cities Top 20":
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df_city1["City"],df_city1["Users"])
    ax.set_xlabel("Cities",fontsize=10)
    ax.set_ylabel("Count of Users",fontsize=10)
    ax.set_xticklabels(df_city1["City"],rotation=90 )
    st.pyplot(fig)


if option2 =="Visitors as per Browser":
    st.write('')
    st.write('')
    st.write('')
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df_browser["Browser"],df_browser["Users"])
    ax.set_xlabel("Browsers",fontsize=10)
    ax.set_ylabel("Count of Users",fontsize=10)
    ax.set_xticklabels(df_browser["Browser"],rotation=90 )
    st.pyplot(fig)


if option2 =='Top 10 Page Viewed on the Website':

    st.write('')
    st.write('')
    st.write('')
    top_10=df_final.groupby(["Page"])["Page","Pageviews"].sum().reset_index()
    index = top_10.sort_values("Pageviews",ascending=False)[1:11]["Page"].values
    values = top_10.sort_values("Pageviews",ascending=False)[1:11]["Pageviews"].values
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(index,values)
    ax.set_xlabel("Song Name",fontsize=10)
    ax.set_ylabel("Views",fontsize=10)
    ax.set_xticklabels(index,rotation=90 )
    st.pyplot(fig)



st.header("Visitors from countries")
countries =df_country["Country"].unique().tolist()
st.write(countries)

