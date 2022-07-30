import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import processor, helper

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = processor.processor(df,region_df)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','OverAll Analysis','CountryWise Analysis','AtheleteWise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == "OverAll" and selected_year == "OverAll":
        st.title("OverAll Tally")
    if selected_country == "OverAll" and selected_year != 'OverAll':
        st.title("Meadal Tally in "+ str(selected_year) + " Olympics")
    if selected_country != "OverAll" and selected_year == 'OverAll':
        st.title("Meadal Tally for "+ str(selected_country) + "in Olympics")
    if selected_country != "OverAll" and selected_year != 'OverAll':
        st.title("Meadal Tally for "+ str(selected_country) + " in "+ str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'OverAll Analysis':
    editions = df['Year'].nunique()-1
    city = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()


    st.title("Top Statistics")
    col1 , col2, col3 =st.columns(3)

    with col1:
        st.header("Editions")
        st.header(editions)
    with col2:
        st.header("Hosts")
        st.header(city)
    with col3:
        st.header("Sports")
        st.header(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.header(events)
    with col2:
        st.header("Nations")
        st.header(nations)
    with col3:
        st.header("Atheletes")
        st.header(athletes)

    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x = 'Edition', y= 'region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Atheletes over the years")
    st.plotly_chart(fig)

    st.title("No of Event over time (Every Sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count', fill_value=0),
                     annot=True)
    st.pyplot(fig)

    st.title("Most Succesfull Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'OverAll')

    selected_sport = st.selectbox('Select a sport', sport_list)

    x = helper.most_succesful(df, selected_sport)
    st.table(x)

if user_menu == 'CountryWise Analysis':

    st.title("CountryWise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.year_wise_medal_tally(df,selected_country)

    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))

    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title("Top 10 Atheletes of " + selected_country)
    top10_df = helper.most_succesful_athelete_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'AtheleteWise Analysis':
    athlete_df = df.drop_duplicates(['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['OverAll', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000,height = 600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'OverAll')

    selected_sport = st.selectbox('Select a sport', sport_list)

    st.title("Height vs Weight")
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'], hue = temp_df['Medal'],style = temp_df['Sex'], s=60)
    st.pyplot(fig)


    st.title("Men vs Women participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize = False,width = 1000,height = 600)
    st.plotly_chart(fig)
