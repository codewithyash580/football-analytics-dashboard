import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Head to Head",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Head-to-Head Analysis")
st.write("Compare the historical performance of two football teams.")


df = pd.read_csv("../data/processed/football_cleaned.csv")

home_teams = df["Home_Team"].dropna().unique()
away_teams = df["Away_Team"].dropna().unique()

teams = sorted(set(home_teams) | set(away_teams))



col1, col2 = st.columns(2)

with col1:
    team_a = st.selectbox(
        "Select Team A",
        teams
    )

with col2:
    team_b = st.selectbox(
        "Select Team B",
        teams,
        index=1 if len(teams) > 1 else 0
    )


if team_a == team_b:

    st.warning("Please select two different teams.")

    st.stop()


h2h = df[
    (
        (df["Home_Team"] == team_a) &
        (df["Away_Team"] == team_b)
    )
    |
    (
        (df["Home_Team"] == team_b) &
        (df["Away_Team"] == team_a)
    )
].copy()



if h2h.empty:

    st.warning(
        f"No head-to-head matches found between "
        f"{team_a} and {team_b}."
    )

    st.stop()



team_a_wins = 0
team_b_wins = 0
draws = 0

team_a_goals = 0
team_b_goals = 0

for _, row in h2h.iterrows():

    home_goals = row["Home_Goals"]
    away_goals = row["Away_Goals"]

    # Team A is Home
    if row["Home_Team"] == team_a:

        team_a_goals += home_goals
        team_b_goals += away_goals

        if home_goals > away_goals:
            team_a_wins += 1

        elif away_goals > home_goals:
            team_b_wins += 1

        else:
            draws += 1

    
    else:

        team_a_goals += away_goals
        team_b_goals += home_goals

        if away_goals > home_goals:
            team_a_wins += 1

        elif home_goals > away_goals:
            team_b_wins += 1

        else:
            draws += 1



total_matches = len(h2h)



st.subheader(
    f"⚽ {team_a} vs {team_b}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches",
    total_matches
)

col2.metric(
    f"{team_a} Wins",
    team_a_wins
)

col3.metric(
    f"{team_b} Wins",
    team_b_wins
)

col4.metric(
    "Draws",
    draws
)



col5, col6 = st.columns(2)

col5.metric(
    f"{team_a} Goals",
    int(team_a_goals)
)

col6.metric(
    f"{team_b} Goals",
    int(team_b_goals)
)

st.divider()



st.subheader("🏆 Win Comparison")

win_data = pd.DataFrame({
    "Team": [
        team_a,
        team_b,
        "Draw"
    ],
    "Results": [
        team_a_wins,
        team_b_wins,
        draws
    ]
})

fig1 = px.bar(
    win_data,
    x="Team",
    y="Results",
    text="Results",
    title=f"{team_a} vs {team_b} - Results"
)

fig1.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


st.subheader("⚽ Goals Comparison")

goal_data = pd.DataFrame({
    "Team": [
        team_a,
        team_b
    ],
    "Goals": [
        team_a_goals,
        team_b_goals
    ]
})

fig2 = px.bar(
    goal_data,
    x="Team",
    y="Goals",
    text="Goals",
    title="Head-to-Head Goals"
)

fig2.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("📋 Match History")

display_columns = [
    "Home_Team",
    "Away_Team",
    "Home_Goals",
    "Away_Goals"
]

available_columns = [
    col for col in display_columns
    if col in h2h.columns
]

st.dataframe(
    h2h[available_columns],
    use_container_width=True
)