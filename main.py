import streamlit as st
import pandas as pd
import folium
from pandas import DataFrame
from plotly import graph_objects as go
from streamlit_folium import st_folium
import plotly.express as px

APP_TITLE = 'AdSight'
APP_SUB_TITLE = 'Advertisement Impact Dashboard'

IMPRESSIONS = "Impressions"
VIEWERS = "Viewers"
SEARCHERS = "Search Audience"

ALL_PANELS = "all billboards"


# Parts of the code taken from: https://github.com/zakariachowdhury/streamlit-map-dashboard (MIT License)

def display_map(width, height):
    # Frankfurt Airport coordinates
    frankfurt_airport_lat = 50.0505
    frankfurt_airport_lon = 8.574

    # Create a map centered around Frankfurt Airport
    map_center = [frankfurt_airport_lat, frankfurt_airport_lon]
    map = folium.Map(location=map_center, zoom_start=18, scrollWheelZoom=True, tiles='CartoDB positron')

    choropleth = folium.Choropleth(
        geo_data='data/billboards.geojson',
        data=None,
        columns=(),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels=False)
    )

    st_map = st_folium(map, width=width, height=height)

    last_clicked_rectangle = None
    if st_map['last_active_drawing']:
        print(f"Hello, you clicked {st_map['last_active_drawing']['properties']['name']}")
        last_clicked_rectangle = st_map['last_active_drawing']['properties']['name']
    return last_clicked_rectangle

def get_color(val, mean):
    print(val)
    print(mean)
    if val < mean:
        return '#ff6961'
    if val >= mean:
        return '#87d277'

def display_funnel(df: DataFrame, panel_name: str | None = None):

    agg_df = df.groupby("billboard_name").agg({"people_passed": "mean", "interactions": "mean", "viewers": "mean"}).reset_index()


    means = [round(agg_df["people_passed"].mean(),2), round(agg_df["viewers"].mean(),2), round(agg_df["interactions"].mean(),2)]

    if panel_name:
        row = agg_df[agg_df["billboard_name"] == panel_name]
        curr_data = [round(row['people_passed'].iloc[0],2), round(row['viewers'].iloc[0],2), round(row['interactions'].iloc[0],2)]
        colors = [get_color(val, mean) for val, mean in zip(curr_data, means)]
    else:
        curr_data = means
        colors = ['#f9f871']*3

    fig = go.Figure(go.Funnel(
        y=[IMPRESSIONS, VIEWERS, SEARCHERS],
        x=curr_data,
        marker=dict(color=colors),
        connector=dict(fillcolor='#EDEDED'),
        showlegend=False,
    ))

    fig.update_layout(title=f"Mean data of {panel_name if panel_name else ALL_PANELS}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def display_data_over_time(df: DataFrame, panel_name: str | None = None):

    filtered_df = df[df['billboard_name'] == panel_name] if panel_name else df


    #df = px.data.gapminder().query("continent=='Oceania'")

    tab1, tab2, tab3 = st.tabs([IMPRESSIONS, VIEWERS, SEARCHERS])
    with tab1:
        column_name = "people_passed"
        if not panel_name:
            filtered_df_1 = filtered_df.groupby('date').agg({column_name: 'mean'}).reset_index()
        else:
            filtered_df_1 = filtered_df
        fig = px.line(filtered_df_1, x="date", y=column_name)
        fig.update_layout(title=f"Data of {panel_name if panel_name else ALL_PANELS}")
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Number of " + IMPRESSIONS)
        fig.update_traces(line=dict(color='#f9f871'))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        column_name = "minutes_observed"
        if not panel_name:
            filtered_df_2 = filtered_df.groupby('date').agg({column_name: 'mean'}).reset_index()
        else:
            filtered_df_2 = filtered_df
        fig = px.line(filtered_df_2, x="date", y=column_name)
        fig.update_layout(title=f"Data of {panel_name if panel_name else ALL_PANELS}")
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Number of " + VIEWERS)
        fig.update_traces(line=dict(color='#f9f871'))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab3:
        column_name = "interactions"
        if not panel_name:
            filtered_df_3 = filtered_df.groupby('date').agg({column_name: 'mean'}).reset_index()
        else:
            filtered_df_3 = filtered_df
        fig = px.line(filtered_df_3, x="date", y=column_name)
        fig.update_layout(title=f"Data of {panel_name if panel_name else ALL_PANELS}")
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Number of " + SEARCHERS)
        fig.update_traces(line=dict(color='#f9f871'))

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def main():
    st.set_page_config(APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    df = pd.read_csv("data/billboard_data.csv")
    map_width = 1400
    map_height = map_width / 3

    # Display Filters and Map
    col1, col2 = st.columns([4, 1])

    with col1:
        last_clicked_panel = display_map(map_width, map_height)
    with col2:
        display_funnel(df, last_clicked_panel)

    # last_clicked_panel = display_map()
    # display_funnel(last_clicked_panel)
    display_data_over_time(df, last_clicked_panel)


if __name__ == "__main__":
    main()