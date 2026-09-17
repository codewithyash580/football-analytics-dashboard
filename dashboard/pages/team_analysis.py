import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Team Analysis",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Team Analysis")
st.write("Analyze the performance of an individual football team.")


df = pd.read_csv("../data/processed/football_cleaned.csv")


home_teams = df["Home_Team"].dropna().unique()
away_teams = df["Away_Team"].dropna().unique()

teams = sorted(set(home_teams) | set(away_teams))


team = st.selectbox(
    "Select Team",
    teams
)


home = df[df["Home_Team"] == team]
away = df[df["Away_Team"] == team]


matches_played = len(home) + len(away)

goals_scored = (
    home["Home_Goals"].sum()
    + away["Away_Goals"].sum()
)

goals_conceded = (
    home["Away_Goals"].sum()
    + away["Home_Goals"].sum()
)

# Wins
home_wins = (home["Home_Goals"] > home["Away_Goals"]).sum()
away_wins = (away["Away_Goals"] > away["Home_Goals"]).sum()

wins = home_wins + away_wins

# Draws
home_draws = (home["Home_Goals"] == home["Away_Goals"]).sum()
away_draws = (away["Away_Goals"] == away["Home_Goals"]).sum()

draws = home_draws + away_draws

# Losses
losses = matches_played - wins - draws



col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches Played",
    matches_played
)

col2.metric(
    "Wins",
    wins
)

col3.metric(
    "Draws",
    draws
)

col4.metric(
    "Losses",
    losses
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "Goals Scored",
    int(goals_scored)
)

col6.metric(
    "Goals Conceded",
    int(goals_conceded)
)

goal_difference = goals_scored - goals_conceded

col7.metric(
    "Goal Difference",
    int(goal_difference)
)

st.divider()



st.subheader("📊 Match Results")

result_data = pd.DataFrame({
    "Result": ["Wins", "Draws", "Losses"],
    "Matches": [wins, draws, losses]
})

fig = px.bar(
    result_data,
    x="Result",
    y="Matches",
    title=f"{team} - Match Results",
    text="Matches"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)



st.subheader("⚽ Goals Analysis")

goal_data = pd.DataFrame({
    "Category": [
        "Goals Scored",
        "Goals Conceded"
    ],
    "Goals": [
        goals_scored,
        goals_conceded
    ]
})

fig2 = px.bar(
    goal_data,
    x="Category",
    y="Goals",
    title=f"{team} - Goals Comparison",
    text="Goals"
)

fig2.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)



st.subheader("🏠 Home vs Away Performance")

home_goals = home["Home_Goals"].sum()
away_goals = away["Away_Goals"].sum()

home_conceded = home["Away_Goals"].sum()
away_conceded = away["Home_Goals"].sum()

performance_data = pd.DataFrame({
    "Location": ["Home", "Away"],
    "Goals Scored": [
        home_goals,
        away_goals
    ],
    "Goals Conceded": [
        home_conceded,
        away_conceded
    ]
})

fig3 = px.bar(
    performance_data,
    x="Location",
    y=["Goals Scored", "Goals Conceded"],
    barmode="group",
    title=f"{team} - Home vs Away"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)



if "Shots_Home" in df.columns and "Shots_Away" in df.columns:

    home_shots = home["Shots_Home"].sum()
    away_shots = away["Shots_Away"].sum()

    total_shots = home_shots + away_shots

    st.subheader("🎯 Shots Analysis")

    st.metric(
        "Total Shots",
        int(total_shots)
    )

    shots_data = pd.DataFrame({
        "Location": ["Home", "Away"],
        "Shots": [
            home_shots,
            away_shots
        ]
    })

    fig4 = px.bar(
        shots_data,
        x="Location",
        y="Shots",
        title=f"{team} - Shots"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )



st.subheader("📋 Team Summary")

st.write(
    f"""
    **{team}** played **{matches_played} matches**.

    - 🏆 Wins: **{wins}**
    - 🤝 Draws: **{draws}**
    - ❌ Losses: **{losses}**
    - ⚽ Goals Scored: **{int(goals_scored)}**
    - 🥅 Goals Conceded: **{int(goals_conceded)}**
    - 📈 Goal Difference: **{int(goal_difference)}**
    """
)