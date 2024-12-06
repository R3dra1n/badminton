import random
import pandas as pd

# 选手列表
players = ["A", "B", "C", "D", "E", "F", "G", "H"]

def generate_match_schedule(players):
    num_players = len(players)
    num_rounds = 7  # 每人打满 7 场
    matches = []  # 存储每一轮的比赛

    # 初始化跟踪器：记录每人的搭档和对手
    used_partners = {player: set() for player in players}

    for round_num in range(num_rounds):
        round_matches = []
        available_players = players[:]
        random.shuffle(available_players)  # 随机打乱选手顺序

        while len(available_players) >= 4:
            # 从剩余选手中选 4 个
            group = available_players[:4]
            del available_players[:4]

            # 动态匹配搭档
            p1, p2 = group[0], group[1]
            p3, p4 = group[2], group[3]

            # 如果搭档重复，重新打乱本轮
            if p2 in used_partners[p1] or p1 in used_partners[p2] or \
               p4 in used_partners[p3] or p3 in used_partners[p4]:
                available_players.extend(group)
                random.shuffle(available_players)
                continue

            # 记录本轮搭档
            used_partners[p1].add(p2)
            used_partners[p2].add(p1)
            used_partners[p3].add(p4)
            used_partners[p4].add(p3)

            # 添加本轮比赛
            round_matches.append(((p1, p2), (p3, p4)))

        # 如果本轮无法完成分组，重新生成比赛表
        if len(round_matches) < num_players // 4:
            return None

        matches.append(round_matches)

    return matches


# 高效生成对阵表
def generate_schedule_until_success(players):
    for _ in range(100):  # 限制尝试次数，避免无限循环
        matches = generate_match_schedule(players)
        if matches:
            return matches
    raise RuntimeError("无法在合理时间内生成符合条件的对阵表，请稍后再试")


# 尝试生成对阵表
matches = generate_schedule_until_success(players)

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
