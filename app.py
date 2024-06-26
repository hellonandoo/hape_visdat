import time  #

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import plotly.graph_objects as go
import altair as alt
import math
from PIL import Image

import seaborn as sns
from pandas import DataFrame

st.set_page_config(
    page_title="RectoGadget",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_option("deprecation.showPyplotGlobalUse", False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)

dataset_url = "https://raw.githubusercontent.com/hellonandoo/hape_visdat/main/clean/smartphone.csv"


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


phone = get_data()

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
> Sections Introduction
1. [Top 5 Smartphones with the Highest Prices](#top-5-smartphones-with-the-highest-prices)
2. [Sales focus based on processor](#sales-focus-based-on-processor)
3. [Best Rated phones](#best-rated-phones)
4. [Distribution of Processors by Manufacturer and Brand](#distribution-of-processors-by-manufacturer-and-brand)
5. [Percentage of Smartphone by ram and internal](#percentage-of-smartphone-by-ram-and-internal)
""",
    unsafe_allow_html=True,
)

# Set Dashboard Title
st.write("""<h2 style="text-align: center; margin-top:0;">Smartphone Dashboard Sales</h2>""", unsafe_allow_html=True)
st.markdown("***")

col1, col2 = st.columns((2))

#membuat sidebar         
st.sidebar.header("Choose your filter: ")

#Create filter for brand name
brand = st.sidebar.multiselect("Pick your brand",phone["brand_name"].unique())
if not brand:
    phone2 = phone.copy()
else:
    phone2 = phone[phone["brand_name"].isin(brand)]

#Create filter for Rating
rating = st.sidebar.multiselect("Pick your Rating",phone2["rating"].unique())
if not rating:
    phone3 = phone2.copy()
else:
    phone3 = phone2[phone2["rating"].isin(rating)]

#Create filter for Prosesor
procie = st.sidebar.multiselect("Pick your Prosesor",phone3["processor_brand"].unique())
if not procie:
    phone4 = phone3.copy()
else:
    phone4 = phone3[phone3["processor_brand"].isin(procie)]

#Create filter for refresh rate
refreshrate = st.sidebar.multiselect("Refresh rate phone?",phone4["refresh_rate"].unique())

st.sidebar.header("(for section 1 & 2)")

# Filter based on brand, rating, procie, and refreshrate card
if not brand and not rating and not procie and not refreshrate:
    filtere_phone = phone
elif not rating and not procie and not refreshrate:
    filtere_phone = phone[phone["brand_name"].isin(brand)]
elif not brand and not procie and not refreshrate:
    filtere_phone = phone[phone["rating"].isin(rating)]
elif not brand and not rating and not refreshrate:
    filtere_phone = phone[phone["processor_brand"].isin(procie)]
elif rating and procie and refreshrate:
    filtere_phone = phone4[phone4["rating"].isin(rating) & phone4["processor_brand"].isin(procie) & phone4["refresh_rate"].isin(refreshrate)]
elif brand and procie and refreshrate:
    filtere_phone = phone4[phone4["brand_name"].isin(brand) & phone4["processor_brand"].isin(procie) & phone4["refresh_rate"].isin(refreshrate)]
elif brand and rating and refreshrate:
    filtere_phone = phone4[phone4["brand_name"].isin(brand) & phone4["rating"].isin(rating) & phone4["refresh_rate"].isin(refreshrate)]
elif rating and refreshrate:
    filtere_phone = phone4[phone4["rating"].isin(rating) & phone4["refresh_rate"].isin(refreshrate)]
elif brand and refreshrate:
    filtere_phone = phone4[phone4["brand_name"].isin(brand) & phone4["refresh_rate"].isin(refreshrate)]
elif procie and refreshrate:
    filtere_phone = phone4[phone4["processor_brand"].isin(procie) & phone4["refresh_rate"].isin(refreshrate)]
else:
    filtere_phone = phone4

col1, col2 = st.columns((2))

category_df = filtere_phone.groupby(by = ["model"], as_index = False)["price"].sum()
category_df = category_df.sort_values(by = ["price"], ascending=False,)
category_df = category_df.head(5)

#Chart HP paling termahal
with col1:
    st.subheader("Top 5 Smartphones with the Highest Prices")
    fig = px.bar(category_df, x = "model", y = "price", text = ['Rp{:,.0f}'.format(x) for x in category_df["price"]], template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)


# Grafik Penjualan berdasarkan wilayah
with col2:
    st.subheader("Sales focus based on processor")
    fig = px.pie(filtere_phone, values = "price", names = "processor_brand", hole = 0.5)
    fig.update_traces(text = filtere_phone["processor_brand"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

# RATINGS

st.header("Best Rated phones")

rating_col_1, rating_col_2 = st.columns([3, 9])
with rating_col_1:
    st.write("\n")
    # st.write("Insert amount")
    #color = st.select_slider(
    #    "Set the number of data to be displayed",
    #    options=[5, 10, 15, 20, 25, 30, 40, 50],
    #    key="rating_1",
    #)
    #st.write(f"Top {color} \n phone Ratings")
with rating_col_2:
    #rating_5, rating_4, rating_3, rating_2, rating_1 = st.tabs(
    #    [
    #        "Rating :five:",
    #        "Rating :four:",
    #        "Rating :three:",
    #        "Rating :two:",
    #        "Rating :one:",
    #    ]
    #)
    pass


# FUNC DOT PLOTS RATING
def dot_plots_rating_phone(brand_filter, rating):
    # Filter data berdasarkan brand dan rating
    filtered_data = phone[(phone["brand_name"] == brand_filter) & (phone["rating"] == rating)]
    
    # Plot bar chart
    fig = px.bar(filtered_data, x="model", 
                 title=f"Top {len(filtered_data)} phone Ratings for {brand_filter} (Rating {rating})", 
                 template="seaborn")
    fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Memanggil fungsi dengan filter brand dan rating yang diinginkan
with rating_col_2:
    st.write("\n")
    selected_brand = st.selectbox("Select Brand", phone['brand_name'].unique())
    selected_rating = st.slider("Select Rating", min_value=1, max_value=5, value=5)

    dot_plots_rating_phone(brand_filter=selected_brand, rating=selected_rating)



# FUNC PIE CHART
def pie_chart(columns, by, values, labels, names, color, title):
    fig = px.pie(
        phone.loc[(phone[columns] == by)],
        values=values,
        labels=labels,
        names=names,
        color=color,
        title=f"{title}",
    )

    fig.update_layout(xaxis_title=option, yaxis_title="Count of " + option)
    st.plotly_chart(fig, use_container_width=True)


# FUNC BAR CHART
def bar_chart(by, columns, return1, return2, title, orientation):
    value_counts = phone[phone[by] == option][columns].value_counts().reset_index()

    value_counts.columns = [return1, return2]

    fig = px.bar(
        value_counts,
        x=value_counts.columns[0],
        y=value_counts.columns[1],
        text=value_counts.columns[1],
        color=value_counts.columns[0],
        title=f"{title}",
        orientation=orientation,
    )

    fig.update_layout(
        xaxis_title=value_counts.columns[0],
        yaxis_title="Count of " + value_counts.columns[0],
    )

    st.plotly_chart(fig, use_container_width=True)


# FUNC SELECT BOX CUSTOM
def select_box(title, column, key):
    data = st.selectbox(title, phone[column].unique(), key=key)
    return data

st.header("Distribution of Smartphone Prices by Processor Speed")

# Filter by brand
option_brand = select_box(
    title="Choose a Brand to Filter Prices:",
    column="brand_name",
    key="procie_brand_filter"
)

# Filter by chipset
option_chipset = select_box(
    title="Choose Chipset:",
    column="processor_brand",
    key="procie_chipset_filter"
)

# Get unique processor speeds including "All"
unique_speeds = ["All"] + list(phone["processor_speed"].unique())

# Filter by processor speed
option_speed = select_box(
    title="Choose Processor Speed:",
    column="processor_speed",
    key="procie_speed_filter"
)

filtered_phone = phone[
    (phone["brand_name"] == option_brand)
    & (phone["processor_brand"] == option_chipset)
]

if option_speed != "All":
    filtered_phone = filtered_phone[phone["processor_speed"] == option_speed]

# Plot the distribution of prices for the selected brand, chipset, and speed
fig = px.bar(
    filtered_phone,
    x="price",
    y="model",
    title=f"Distribution of Smartphone Prices for {option_chipset} Chipset with Processor Speed {option_speed if option_speed != 'All' else 'All'} GHz",
    labels={"model": "Smartphone Model", "price": "Price ($)"},
    orientation="h"  # Horizontal bar plot
)

fig.update_layout(
    xaxis_title="Price ($)",
    yaxis_title="Smartphone Model",
)

st.plotly_chart(fig, use_container_width=True)




st.header("Percentage of Smartphone by ram and internal")  #

option = select_box(
    title="Choose a column to plot count. Try Selecting Brand ",
    column="brand_name",
    key="ram_internal",
)
ram, internal = st.columns([6, 6])

with ram:
    pie_chart(
        columns="brand_name",
        by=option,
        values="ram_capacity",
        labels="ram_capacity",
        names="ram_capacity",
        color="ram_capacity",
        title=f"Distribution of ram capacity by {option} Brand ",
    )

with internal:
    pie_chart(
        columns="brand_name",
        by=option,
        values="internal_memory",
        labels="internal_memory",
        names="internal_memory",
        color="internal_memory",
        title=f"Distribution internal memory by {option} Brand ",
    )
