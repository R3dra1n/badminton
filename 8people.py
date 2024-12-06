import random
import pandas as pd

# 选手列表
players = ["A", "B", "C", "D", "E", "F", "G", "H"]

def generate_match_schedule(players):
    num_rounds = 7  # 每人打满 7 场
    matches = []  # 存储每一轮的比赛
    used_partners = {player: set() for player in players}  # 记录每人的搭档

    for round_num in range(num_rounds):
        round_matches = []
        available_players = players[:]
        random.shuffle(available_players)  # 随机打乱选手顺序

        while len(available_players) >= 4:
            # 从剩余选手中随机选择4个
            group = available_players[:4]
            del available_players[:4]  # 移除已选择的选手

            # 确保搭档不重复
            p1, p2 = group[0], group[1]
            p3, p4 = group[2], group[3]

            # 如果搭档已经存在，重新洗牌
            if p2 in used_partners[p1] or p1 in used_partners[p2]:
                available_players.extend(group)  # 把组加回去
                random.shuffle(available_players)  # 洗牌重新选择
                continue

            if p4 in used_partners[p3] or p3 in used_partners[p4]:
                available_players.extend(group)
                random.shuffle(available_players)
                continue

            # 添加搭档关系
            used_partners[p1].add(p2)
            used_partners[p2].add(p1)
            used_partners[p3].add(p4)
            used_partners[p4].add(p3)

            # 记录本轮比赛
            round_matches.append(((p1, p2), (p3, p4)))

        # 如果无法满足条件，重新生成本轮
        if len(round_matches) < len(players) // 4:
            return None

        matches.append(round_matches)

    return matches

# 尝试生成对阵表，直到成功为止
while True:
    matches = generate_match_schedule(players)
    if matches:
        break

# 转换为 DataFrame 便于展示
schedule = []
for round_num, round_matches in enumerate(matches, 1):
    for match_num, ((p1, p2), (p3, p4)) in enumerate(round_matches, 1):
        schedule.append({
            "轮次": round_num,
            "场次": match_num,
            "场地": f"场地 {match_num}",
            "队伍1": f"{p1} 和 {p2}",
            "队伍2": f"{p3} 和 {p4}"
        })

schedule_df = pd.DataFrame(schedule)

# 使用 Streamlit 展示对阵表
import streamlit as st

st.title("羽毛球随机对阵生成器")
st.subheader("生成的对阵表如下：")
st.dataframe(schedule_df)
