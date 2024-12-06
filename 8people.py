import streamlit as st
import pandas as pd

# 定义比赛规则和轮次对阵表
st.title("羽毛球比赛管理系统")
st.write("""
比赛规则：
1. **场地和时间限制**：两个场地，总计 16 场比赛，每场限时 13 分钟，包含 2 分钟计分和休息时间。
2. **积分规则**：
    - **完成的局**：
        - 胜方得 3 分（超过 21 分），负方得 1.5 分。
        - 胜方得 2 分（正好 21 分），负方得 1 分。
    - **未完成的局**：
        - 分数高者得 1.5 分（比分超过 11），低者得 0.5 分。
        - 分数均小于等于 11，胜方得 1 分，负方得 0 分。
3. **角色轮换**：确保每个球员每场比赛与不同的队友和对手配对。
""")

# 定义选手和对阵表
players = ["A", "B", "C", "D", "E", "F", "G", "H"]
match_schedule = [
    [("A", "B", "C", "D"), ("E", "F", "G", "H")],
    [("A", "C", "E", "G"), ("B", "F", "D", "H")],
    [("A", "E", "G", "H"), ("B", "C", "D", "F")],
    [("A", "G", "F", "H"), ("B", "E", "C", "D")],
    [("A", "H", "C", "F"), ("B", "G", "D", "E")],
    [("A", "D", "E", "H"), ("B", "F", "C", "G")],
    [("A", "F", "G", "E"), ("B", "H", "C", "D")],
    [("A", "H", "G", "C"), ("B", "E", "F", "D")]
]

# 显示对阵表
st.subheader("比赛对阵表")
schedule_df = pd.DataFrame(
    {
        "轮次": [f"第{i+1}轮" for i in range(len(match_schedule))],
        "场地1": [f"{match[0][0]}和{match[0][1]} 对阵 {match[0][2]}和{match[0][3]}" for match in match_schedule],
        "场地2": [f"{match[1][0]}和{match[1][1]} 对阵 {match[1][2]}和{match[1][3]}" for match in match_schedule],
    }
)
st.dataframe(schedule_df)

# 积分计算
st.subheader("模拟积分计算")
st.write("输入比赛结果，自动计算积分。")

# 动态表单输入比分
results = []
for i, match in enumerate(match_schedule):
    st.write(f"### 第 {i+1} 轮")
    col1, col2 = st.columns(2)
    with col1:
        score1 = st.text_input(f"场地1比分（例如 21-19）", key=f"score1_{i}")
    with col2:
        score2 = st.text_input(f"场地2比分（例如 15-18）", key=f"score2_{i}")
    results.append((score1, score2))

# 解析比分并计算积分
def calculate_points(score):
    if not score or "-" not in score:
        return (0, 0)
    try:
        p1, p2 = map(int, score.split("-"))
        if p1 > p2:
            if p1 > 21:
                return (3, 1.5)
            elif p1 == 21:
                return (2, 1)
            elif p1 > 11:
                return (1.5, 0.5)
            else:
                return (1, 0)
        else:
            if p2 > 21:
                return (1.5, 3)
            elif p2 == 21:
                return (1, 2)
            elif p2 > 11:
                return (0.5, 1.5)
            else:
                return (0, 1)
    except ValueError:
        return (0, 0)

# 显示积分结果
if st.button("计算积分"):
    total_points = {player: 0 for player in players}
    for i, (score1, score2) in enumerate(results):
        if score1:
            p1, p2 = calculate_points(score1)
            match = match_schedule[i][0]
            total_points[match[0]] += p1
            total_points[match[1]] += p1
            total_points[match[2]] += p2
            total_points[match[3]] += p2
        if score2:
            p1, p2 = calculate_points(score2)
            match = match_schedule[i][1]
            total_points[match[0]] += p1
            total_points[match[1]] += p1
            total_points[match[2]] += p2
            total_points[match[3]] += p2

    # 显示最终积分
    points_df = pd.DataFrame(
        [{"选手": player, "积分": total_points[player]} for player in players]
    ).sort_values(by="积分", ascending=False)
    st.subheader("总积分排名")
    st.dataframe(points_df)