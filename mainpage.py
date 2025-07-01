import streamlit as st

simulator_pg = st.Page("simulator.py", title="Simulate scheduling!", icon="⚙️")
info_pg = st.Page("info.py", title="Learn about the scheduling algorithms!", icon="📖")

pg = st.navigation(pages=[simulator_pg, info_pg])
pg.run()