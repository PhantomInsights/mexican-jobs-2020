"""
Functions used to generate the EDA on the mexican job offers dataset.
"""

import json
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go


def days_stats(df):
    """Gets the daily counts by weekday and plots the daily counts.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    weekdays = df["isodate"].dt.weekday.value_counts()
    weekdays.sort_index(inplace=True)

    print(weekdays.to_markdown(floatfmt=",.0f"))

    # Create a Series with the counts of each day.
    days_counts = df["isodate"].value_counts()
    days_counts.sort_index(inplace=True)

    # Create a new DataFrame with only the data of Mondays.
    monday_df = days_counts[days_counts.index.weekday == 0]

    # Initialize our Figure.
    fig = go.Figure()

    fig.add_traces(go.Scatter(x=days_counts.index, y=days_counts.values, line_color="#ffa000",
                              mode="markers+lines", line_width=3, marker_size=12))

    # Highlight Mondays with a bigger marker.
    fig.add_traces(go.Scatter(x=monday_df.index, y=monday_df.values,
                              line_color="#c6ff00", mode="markers", marker_size=18))

    fig.update_xaxes(title="Date (2020)", ticks="outside", ticklen=10,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=12)

    fig.update_yaxes(title="Number of Job Offers", ticks="outside", ticklen=10,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=12)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Job Offers by Day",
        title_x=0.5,
        title_y=0.93,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("1.png")


def salaries_stats(df):
    """Plots the salaries distribution in an Histograms.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    print(df["salary"].describe().to_markdown(floatfmt=",.0f"))

    salaries = df[df["salary"] <= 35000]

    fig = go.Figure()

    fig.add_traces(go.Histogram(
        x=salaries["salary"], nbinsx=35, marker_color="#ffa000"))

    fig.update_xaxes(title="Monthly Salary", ticks="outside", ticklen=10, showgrid=False,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=35, title_standoff=20)

    fig.update_yaxes(title="Number of Job Offers", ticks="outside", ticklen=10,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=12, title_standoff=5)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Salaries Distribution",
        title_x=0.5,
        title_y=0.93,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("2.png")


def plot_states_offers(df):
    """Plots the job offers distribution in av horizontal Bar plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    states_series = df["state"].value_counts()

    fig = go.Figure()

    fig.add_traces(go.Bar(x=states_series.values, y=states_series.index, text=states_series.values,
                          orientation="h", marker={"color": states_series.values, "colorscale": "tropic"}))

    fig.update_xaxes(title="Number of Job Offers", ticks="outside", ticklen=10, tickcolor="#FFFFFF",
                     linewidth=2, showline=True, mirror=True, nticks=12, title_standoff=30, gridwidth=0.5, range=[0, states_series.values.max() * 1.1])

    fig.update_yaxes(title="", ticks="outside", ticklen=10, showgrid=False,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True)

    fig.update_traces(texttemplate=" %{text:,.0f}", textposition="outside")

    # Add final customizations.
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        showlegend=False,
        width=1200,
        height=1400,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Job Offers by State",
        title_x=0.5,
        title_y=0.96,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("3.png")


def plot_states_map(df):
    """Plots the job offers distribution in a Choropleth map.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    states_series = df["state"].value_counts()

    geojson = json.loads(open("mexico.json", "r", encoding="utf-8").read())

    fig = go.Figure()

    fig.add_traces(go.Choropleth(geojson=geojson,
                                 locations=states_series.index,
                                 z=states_series.values,
                                 featureidkey="properties.ADMIN_NAME",
                                 marker_line_color="#FFFFFF",
                                 marker_line_width=1,
                                 colorbar_outlinecolor="#FFFFFF",
                                 colorbar_outlinewidth=1.75,
                                 colorbar_ticks="outside",
                                 colorbar_ticklen=10,
                                 colorbar_tickcolor="#FFFFFF"))

    fig.update_geos(fitbounds="locations",
                    showocean=True, oceancolor="#263238",
                    showcountries=True, countrycolor="#FFFFFF", countrywidth=1.5,
                    framewidth=2, framecolor="#FFFFFF",
                    showlakes=False,
                    landcolor="#1B2327")

    # Add final customizations.
    fig.update_layout(
        title_text="Job Offers by State",
        title_x=0.5,
        title_y=0.96,
        title_font_size=30,
        font_color="#FFFFFF",
        margin={"r": 50, "t": 50, "l": 50, "b": 50},
        width=1200,
        height=650,
        paper_bgcolor="#37474f",
    )

    fig.write_image("4.png")


def plot_states_median_salary(df):
    """Plots the median salary in each state using an horizontal Bar chart.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    median_salaries = df.pivot_table(
        index="state", values="salary", aggfunc="median").sort_values("salary", ascending=False)

    fig = go.Figure()

    fig.add_traces(go.Bar(x=median_salaries["salary"], y=median_salaries.index, text=median_salaries["salary"],
                          orientation="h", marker={"color": median_salaries["salary"], "colorscale": "peach"}))

    fig.update_xaxes(title="Monthly Median Salary in MXN", ticks="outside", ticklen=10, tickcolor="#FFFFFF", separatethousands=True,
                     linewidth=2, showline=True, mirror=True, nticks=12, title_standoff=30, gridwidth=0.5, range=[0, median_salaries["salary"].max() * 1.1])

    fig.update_yaxes(title="", ticks="outside", ticklen=10, showgrid=False,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True)

    fig.update_traces(texttemplate=" %{text:,.0f}", textposition="outside")

    # Add final customizations.
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        showlegend=False,
        width=1200,
        height=1400,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Median Salary by State",
        title_x=0.5,
        title_y=0.96,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("5.png")


def plot_median_salary_map(df):
    """Plots the median salary by state in a Choropleth map.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    median_salaries = df.pivot_table(
        index="state", values="salary", aggfunc="median").sort_values("salary", ascending=False)

    geojson = json.loads(open("mexico.json", "r", encoding="utf-8").read())

    fig = go.Figure()

    fig.add_traces(go.Choropleth(geojson=geojson,
                                 locations=median_salaries.index,
                                 z=median_salaries["salary"],
                                 featureidkey="properties.ADMIN_NAME",
                                 marker_line_color="#FFFFFF",
                                 marker_line_width=1,
                                 colorbar_outlinecolor="#FFFFFF",
                                 colorbar_outlinewidth=1.75,
                                 colorbar_separatethousands=True,
                                 colorbar_ticks="outside",
                                 colorbar_ticklen=10,
                                 colorbar_tickcolor="#FFFFFF"))

    fig.update_geos(fitbounds="locations",
                    showocean=True, oceancolor="#263238",
                    showcountries=True, countrycolor="#FFFFFF", countrywidth=1.5,
                    framewidth=2, framecolor="#FFFFFF",
                    showlakes=False,
                    landcolor="#1B2327")

    # Add final customizations.
    fig.update_layout(
        title_text="Median Salary by State",
        title_x=0.5,
        title_y=0.96,
        title_font_size=30,
        font_color="#FFFFFF",
        margin={"r": 50, "t": 50, "l": 50, "b": 50},
        width=1200,
        height=650,
        paper_bgcolor="#37474f",
    )

    fig.write_image("6.png")


def plot_hours(df):
    """Plots the hours required to work in an Histogram.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    fig = go.Figure()

    fig.add_traces(go.Histogram(x=df["hours_worked"],  marker_color="#ffa000"))

    fig.update_xaxes(title="Hours Required", ticks="outside", ticklen=10,  gridwidth=0.5,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=35, title_standoff=20)

    fig.update_yaxes(title="Number of Job Offers", ticks="outside", ticklen=10, separatethousands=True,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=18, gridwidth=0.5, title_standoff=5)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Labour Hours Distribution",
        title_x=0.5,
        title_y=0.93,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("7.png")


def plot_days(df):
    """Plots the days required to work in an Histogram.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    fig = go.Figure()

    fig.add_traces(go.Histogram(x=df["days_worked"], marker_color="#ffa000"))

    fig.update_xaxes(title="Days Required", ticks="outside", ticklen=10,  gridwidth=0.5,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=35, title_standoff=20)

    fig.update_yaxes(title="Number of Job Offers", ticks="outside", ticklen=10, separatethousands=True,
                     tickcolor="#FFFFFF", linewidth=2, showline=True, mirror=True, nticks=18, gridwidth=0.5, title_standoff=5)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Labour Days Distribution",
        title_x=0.5,
        title_y=0.93,
        margin_l=120,
        margin_b=120,
        title_font_size=30,
        plot_bgcolor="#37474f"
    )

    fig.write_image("8.png")


def plot_education_level(df):
    """Plots the education level distribution in a Donut plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    # Define our custom culors.
    colors = ["#0091ea", "#ff5722", "#43a047", "#7e57c2", "#1565c0",
              "#2e7d32", "#c62828", "#ef6c00", "#ffc400", "#64dd17"]

    education_level = df["education_level"].value_counts()

    fig = go.Figure()

    fig.add_traces(go.Pie(labels=education_level.index,
                          values=education_level.values,
                          marker_colors=colors,
                          hole=0.5,
                          insidetextfont_color="#FFFFFF"))

    # Add final customizations.
    fig.update_layout(
        legend_bordercolor="#FFFFFF",
        legend_borderwidth=1.5,
        legend_x=0.88,
        legend_y=0.5,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Education Level Distribution",
        title_x=0.5,
        title_y=0.93,
        margin={"r": 0, "t": 150, "l": 0, "b": 50},
        width=1200,
        height=800,
        title_font_size=30,
        paper_bgcolor="#37474f"
    )

    fig.write_image("9.png")


def plot_experience(df):
    """Plots the experience distribution in a Donut plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    # Define our custom culors.
    colors = ["#0091ea", "#ff5722", "#43a047", "#7e57c2", "#1565c0",
              "#2e7d32", "#c62828", "#ef6c00", "#ffc400", "#64dd17"]

    experience = df["experience"].value_counts()

    fig = go.Figure()

    fig.add_traces(go.Pie(labels=experience.index,
                          values=experience.values,
                          marker_colors=colors,
                          hole=0.5,
                          insidetextfont_color="#FFFFFF"))

    # Add final customizations.
    fig.update_layout(
        legend_bordercolor="#FFFFFF",
        legend_borderwidth=1.5,
        legend_x=0.88,
        legend_y=0.5,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Required Experience Distribution",
        title_x=0.5,
        title_y=0.93,
        margin={"r": 0, "t": 150, "l": 0, "b": 50},
        width=1200,
        height=800,
        title_font_size=30,
        paper_bgcolor="#37474f"
    )

    fig.write_image("10.png")


def hours_worked_salary(df):
    """Plots the correlation between salary and daily hours worked in a Scatter plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    # Remove outliers.
    df = df[df["salary"] <= 35000]

    # Initialize our Figure.
    fig = go.Figure()

    fig.add_traces(go.Scatter(x=df["hours_worked"], y=df["salary"], line_color="#ffa000",
                              mode="markers", line_width=3, marker_size=8))

    fig.update_xaxes(title="Number of Daily Hours", ticks="outside", ticklen=10,
                     tickcolor="#FFFFFF", title_standoff=30, linewidth=2, showline=True, mirror=True, nticks=25, gridwidth=0.5)

    fig.update_yaxes(title="Monthly Salary in MXN", ticks="outside", ticklen=10, separatethousands=True,
                     tickcolor="#FFFFFF", title_standoff=20, linewidth=2, showline=True, mirror=True, nticks=12, gridwidth=0.5)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Comparison of Hours Worked and Monthly Salary",
        title_x=0.5,
        title_y=0.93,
        margin_l=140,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("11.png")


def education_level_salary(df):
    """Plots the correlation between salary and education level in a Scatter plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame containing job offers data.

    """

    # Remove outliers.
    df = df[df["salary"] <= 35000].copy()

    # We are going to map the education levels with a number.
    # The greater th enumber is the greater the education level.
    education_map = {
        "Primaria": 1,
        "Secundaria/sec. técnica": 2,
        "Prepa o vocacional": 3,
        "Carrera técnica": 4,
        "Carrera comercial": 4,
        "Profesional técnico": 4,
        "T. superior universitario": 4,
        "Licenciatura": 5,
        "Maestría": 6,
        "Doctorado": 7
    }

    # We convert the categorical data to numerical.
    df["education_level"] = df["education_level"].apply(
        lambda x: education_map[x])

   # Initialize our Figure.
    fig = go.Figure()

    fig.add_traces(go.Scatter(x=df["education_level"], y=df["salary"], line_color="#ffa000",
                              mode="markers", line_width=3, marker_size=8))

    fig.update_xaxes(title="Education Level", ticks="outside", ticklen=10,
                     tickcolor="#FFFFFF", title_standoff=30, linewidth=2, showline=True, mirror=True, nticks=7, gridwidth=0.5)

    fig.update_yaxes(title="Monthly Salary in MXN", ticks="outside", ticklen=10, separatethousands=True,
                     tickcolor="#FFFFFF", title_standoff=20, linewidth=2, showline=True, mirror=True, nticks=12, gridwidth=0.5)

    # Add final customizations.
    fig.update_layout(
        showlegend=False,
        width=1200,
        height=800,
        font_color="#FFFFFF",
        font_size=18,
        title_text="Comparison of Education Level and Monthly Salary",
        title_x=0.5,
        title_y=0.93,
        margin_l=140,
        margin_b=120,
        title_font_size=30,
        paper_bgcolor="#37474f",
        plot_bgcolor="#263238"
    )

    fig.write_image("12.png")


if __name__ == "__main__":

    df = pd.read_csv("data.csv", parse_dates=["isodate"])

    # days_stats(df)
    # salaries_stats(df)
    # plot_states_offers(df)
    # plot_states_map(df)
    # plot_states_median_salary(df)
    # plot_median_salary_map(df)
    # plot_hours(df)
    # plot_days(df)
    # plot_education_level(df)
    # plot_experience(df)
    # hours_worked_salary(df)
    # education_level_salary(df)
