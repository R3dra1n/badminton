# Streamlit 应用部分
import math
import random
import streamlit as st
from collections import defaultdict

def generate_doubles_schedule(players, n_matches, max_retries=200):
    n = len(players)
    pairs = [(players[i], players[j]) for i in range(n) for j in range(i + 1, n)]
    games = []
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if not set(pairs[i]).intersection(set(pairs[j])):
                games.append((pairs[i], pairs[j]))
    for retry in range(max_retries):
        random.shuffle(games)
        player_count = defaultdict(int)
        schedule = []

        def can_add_game(game):
            team1, team2 = game
            team_players = set(team1 + team2)
            return all(player_count[player] < n_matches for player in team_players)

        try:
            for game in games:
                if len(schedule) >= n * n_matches // 2:
                    break
                if can_add_game(game):
                    schedule.append(game)
                    for player in game[0] + game[1]:
                        player_count[player] += 1
            if any(count != n_matches for count in player_count.values()):
                raise ValueError("无法均衡分配每位选手的出场次数")
            return schedule
        except ValueError:
            pass
    raise ValueError("超过最大重试次数，无法生成均衡比赛表")

players = []
numbers = st.selectbox("选择您的人数:", [5, 6, 7, 8])
for i in range(numbers):
    player = st.text_input(f"输入第 {i + 1} 号选手")
    players.append(player)

n_matches = st.selectbox("每位选手需要出场的总次数", list(range(1, numbers*2)))

try:
    schedule = generate_doubles_schedule(players, n_matches)
    for idx, game in enumerate(schedule):
        team1, team2 = game
        st.write(f"场次 {idx + 1}: 队1({team1[0]} & {team1[1]}) vs 队2({team2[0]} & {team2[1]})")
except ValueError as e:
    st.write(e)

# 持久化刷新逻辑
if "n" not in st.session_state:
    st.session_state.n = 1

if st.button("refresh"):
    st.session_state.n += 1

st.write(f"刷新次数: {st.session_state.n}")
