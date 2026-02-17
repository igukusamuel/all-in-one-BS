def shift_open_screen():
    st.subheader("Open Shift")

    beginning_cash = st.number_input(
        "Beginning Cash Float",
        min_value=0.0,
        step=10.0
    )

    if st.button("Start Shift"):
        st.session_state.shift_open = True
        st.session_state.beginning_cash = beginning_cash
        st.session_state.cash_sales = 0
        st.success("Shift opened.")
        st.rerun()
