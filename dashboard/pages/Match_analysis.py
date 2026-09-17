import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Match Analysis",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Match Analysis")
st.write("Detailed analysis of football matches.")


df = pd.read_csv("../data/processed/football_cleaned.csv")


df["Match_ID"] = range(1, len(df) + 1)


match_id = st.selectbox(
    "Select Match",
    df["Match_ID"]
)

match = df[df["Match_ID"] == match_id].iloc[0]

home_team = match["Home_Team"]
away_team = match["Away_Team"]

home_goals = match["Home_Goals"]
away_goals = match["Away_Goals"]


if home_goals > away_goals:
    result = f"{home_team} Won"

elif away_goals > home_goals:
    result = f"{away_team} Won"

else:
    result = "Draw"


st.subheader("🏟️ Match")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Home Team",
        home_team
    )

with col2:
    st.metric(
        "Score",
        f"{int(home_goals)} - {int(away_goals)}"
    )

with col3:
    st.metric(
        "Away Team",
        away_team
    )

st.info(f"🏆 Result: **{result}**")

st.divider()


st.subheader