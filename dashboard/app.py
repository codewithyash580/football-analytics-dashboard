import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "football_cleaned.csv"
)

df = pd.read_csv(DATA_PATH)
goals = df["Total_Goals"].value_counts().sort_index().reset_index()
goals.columns = ["Total_Goals", "Matches"]

fig_line = px.line(
    goals,
    x="Total_Goals",
    y="Matches",
    markers=True,
    title="Total Goals Distribution"
)

st.plotly_chart(fig_line, use_container_width=True)
team_goals = (
    df.groupby("Home_Team")["Home_Goals"]
    .sum()
    .reset_index()
    .sort_values("Home_Goals", ascending=False)
)

fig_bar = px.bar(
    team_goals,
    x="Home_Team",
    y="Home_Goals",
    title="Goals Scored by Home Teams"
)

st.plotly_chart(fig_bar, use_container_width=True)
result_count = df["Match_Result"].value_counts().reset_index()
result_count.columns = ["Result", "Matches"]

fig_pie = px.pie(
    result_count,
    names="Result",
    values="Matches",
    title="Match Result Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)


if "Total_Goals" not in df.columns:
   df["Total_Goals"] = (
        df["Home_Goals"] +
     df["Away_Goals"]
    )

if "Goal_Difference" not in df.columns:
    df["Goal_Difference"] = (
        df["Home_Goals"] -
        df["Away_Goals"]
    ).abs()

if (
    "Total_Shots" not in df.columns
    and "Shots_Home" in df.columns
    and "Shots_Away" in df.columns
):
    df["Total_Shots"] = (
        df["Shots_Home"] +
        df["Shots_Away"]
    )


st.title("⚽ Football Analytics Dashboard")
st.write(
    "Interactive analysis of football match data"
)

st.divider()


st.sidebar.header("🔎 Filters")

filtered_df = df.copy()

if "Home_Team" in df.columns and "Away_Team" in df.columns:

    teams = sorted(
        set(df["Home_Team"].dropna()) |
        set(df["Away_Team"].dropna())
    )

    selected_team = st.sidebar.selectbox(
        "Select Team",
        ["All Teams"] + teams
    )

    if selected_team != "All Teams":

        filtered_df = df[
            (df["Home_Team"] == selected_team) |
            (df["Away_Team"] == selected_team)
        ]


st.subheader("📊 Overview")

total_matches = len(filtered_df)

total_goals = filtered_df["Total_Goals"].sum()

average_goals = (
    total_goals / total_matches
    if total_matches > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Matches",
    total_matches
)

col2.metric(
    "Total Goals",
    int(total_goals)
)

col3.metric(
    "Avg Goals / Match",
    round(average_goals, 2)
)

if "Total_Shots" in filtered_df.columns:

    total_shots = filtered_df["Total_Shots"].sum()

    col4.metric(
        "Total Shots",
        int(total_shots)
    )

else:

    col4.metric(
        "Total Shots",
        "N/A"
    )

st.divider()


st.subheader("🏆 Match Results")

home_wins = (
    filtered_df["Home_Goals"] >
    filtered_df["Away_Goals"]
).sum()

away_wins = (
    filtered_df["Away_Goals"] >
    filtered_df["Home_Goals"]
).sum()

draws = (
    filtered_df["Home_Goals"] ==
    filtered_df["Away_Goals"]
).sum()

result_data = pd.DataFrame({
    "Result": [
        "Home Wins",
        "Away Wins",
        "Draws"
    ],
    "Matches": [
        home_wins,
        away_wins,
        draws
    ]
})

fig1 = px.bar(
    result_data,
    x="Result",
    y="Matches",
    text="Matches",
    title="Home vs Away Results"
)

fig1.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


st.subheader("⚽ Goals Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Total_Goals",
    nbins=15,
    title="Distribution of Total Goals"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("🏠 Home vs Away Goals")

home_goals = filtered_df["Home_Goals"].sum()
away_goals = filtered_df["Away_Goals"].sum()

goal_data = pd.DataFrame({
    "Location": [
        "Home",
        "Away"
    ],
    "Goals": [
        home_goals,
        away_goals
    ]
})

fig3 = px.bar(
    goal_data,
    x="Location",
    y="Goals",
    text="Goals",
    title="Home vs Away Goals"
)

fig3.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


st.subheader("🥅 Top Teams by Goals")

home_goal_table = (
    filtered_df
    .groupby("Home_Team")["Home_Goals"]
    .sum()
    .reset_index()
)

home_goal_table.columns = [
    "Team",
    "Goals"
]

away_goal_table = (
    filtered_df
    .groupby("Away_Team")["Away_Goals"]
    .sum()
    .reset_index()
)

away_goal_table.columns = [
    "Team",
    "Goals"
]

team_goals = pd.concat([
    home_goal_table,
    away_goal_table
])

team_goals = (
    team_goals
    .groupby("Team")["Goals"]
    .sum()
    .reset_index()
    .sort_values(
        "Goals",
        ascending=False
    )
    .head(10)
)

fig4 = px.bar(
    team_goals,
    x="Goals",
    y="Team",
    orientation="h",
    text="Goals",
    title="Top 10 Teams by Goals"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader("📋 Data Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

st.caption(
    f"Showing {len(filtered_df)} matches"
)