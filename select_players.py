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
                st.session_state.current_user = st.session_state.queue[0]
                st.session_state.selected_users = []
                st.rerun()
        st.stop()

    # 当前状态
    queue = st.session_state.queue
    current_user = st.session_state.current_user
    selected_users = st.session_state.selected_users

    # 显示当前队列
    st.write(f"当前队列: {queue}")

    # 当前用户操作
    st.subheader(f"当前用户：{current_user}")
    st.write("请选择上场的3名用户（不能选择自己）")

    # 可选用户列表
    available_users = [user for user in queue if user != current_user]
    selected = st.multiselect("请选择3名用户：", available_users, default=selected_users)

    # 确认选择按钮
    if st.button("确认选择"):
        if len(selected) != 3:
            st.error("必须选择3名用户！")
        elif any(user not in available_users for user in selected):
            st.error("选择的用户无效，请重新选择！")
        else:
            # 更新队列
            st.success(f"用户 {current_user} 选择了用户 {selected} 上场")
            queue = [user for user in queue if user not in selected and user != current_user]
            queue.extend(selected)
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
        st.write("游戏结束！最终队列:", queue)
        st.stop()

if __name__ == "__main__":
    select_double_players()