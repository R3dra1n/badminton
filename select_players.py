import streamlit as st

def select_double_players():
    st.title("双打用户选择程序")

    # 初始化状态
    if "queue" not in st.session_state:
        total_users = st.number_input("请输入有几个人：", min_value=4, step=1, format="%d")
        if st.button("确认人数"):
            if total_users < 4:
                st.error("人数必须大于等于4人！")
            else:
                # 初始化队列和状态
                st.session_state.queue = list(range(1, total_users + 1))
                st.session_state.user_names = [""] * total_users  # 初始化用户名字列表
                st.session_state.current_user = st.session_state.queue[0]
                st.session_state.selected_users = []
                st.session_state.names_completed = False
                st.rerun()
        st.stop()

    # 输入用户名字
    if not st.session_state.names_completed:
        st.subheader("请为每位用户输入名字：")
        for i in range(len(st.session_state.queue)):
            st.session_state.user_names[i] = st.text_input(
                f"请输入用户 {i + 1} 的名字：",
                value=st.session_state.user_names[i]
            )

        if "" not in st.session_state.user_names:
            if st.button("完成名字输入"):
                st.session_state.names_completed = True
                st.success("所有用户名字已输入完毕！")
                st.rerun()
        st.stop()

    # 当前状态
    queue = st.session_state.queue
    user_names = st.session_state.user_names
    current_user = st.session_state.current_user
    selected_users = st.session_state.selected_users

    # 显示当前队列及用户名字
    st.write("当前队列:")
    for user_id in queue:
        st.write(f"用户 {user_id}: {user_names[user_id - 1]}")

    # 当前用户操作
    st.subheader(f"当前用户：{user_names[current_user - 1]}（编号 {current_user}）")
    st.write("请选择上场的3名用户（不能选择自己）")

    # 可选用户列表
    available_users = [
        user for user in queue if user != current_user
    ]
    selected = st.multiselect(
        "请选择3名用户：",
        [f"用户 {user}: {user_names[user - 1]}" for user in available_users],
        default=[
            f"用户 {user}: {user_names[user - 1]}" for user in selected_users
        ]
    )

    # 确认选择按钮
    if st.button("确认选择"):
        selected_ids = [
            user for user in available_users
            if f"用户 {user}: {user_names[user - 1]}" in selected
        ]
        if len(selected_ids) != 3:
            st.error("必须选择3名用户！")
        elif any(user not in available_users for user in selected_ids):
            st.error("选择的用户无效，请重新选择！")
        else:
            # 更新队列
            st.success(
                f"用户 {user_names[current_user - 1]} 选择了用户 {', '.join(user_names[user - 1] for user in selected_ids)} 上场"
            )
            queue = [
                user for user in queue
                if user not in selected_ids and user != current_user
            ]
            queue.extend(selected_ids)
            queue.append(current_user)

            # 更新状态
            st.session_state.queue = queue
            if len(queue) > 4:
                st.session_state.current_user = queue[0]
            else:
                st.session_state.current_user = None  # 游戏结束

            st.session_state.selected_users = []
            st.rerun()

    # 游戏结束条件
    if len(queue) <= 4:
        st.write("游戏结束！最终队列:")
        for user_id in queue:
            st.write(f"用户 {user_id}: {user_names[user_id - 1]}")
        st.stop()

if __name__ == "__main__":
    select_double_players()
