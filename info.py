import streamlit as st

st.write("### FCFS")
st.write("#### First Come, First Serve \n\n\n\n")

st.write("Probably the simplest of algorithms, it allocates the CPU to the process " \
            "that requested for it first \n\n\n\n")

st.write("### SJF")
st.write("#### Shortest Job First \n\n\n\n")

st.write("Allocates the CPU to the the process " \
            "that takes the least amount of time to complete"\
                " at the time of initial allocation. \n\n\n\n")

st.write("##### Note : Both FCFS and SJF do not swap out an allocated process while the process is running")

st.write("### SRTF")
st.write("#### Shortest Remaining Time First \n\n\n\n")

st.write("Allocates the CPU to the the process " \
            "that takes the least amount of time to complete at any instant."\
            "n\n  Hence, it can swap out processes previously allocated"\
            "to the CPU if a new process with lower time required comes \n\n\n\n")

st.write("### 📊 Key Metrics")

st.write("#### Waiting Time")
st.write("Time spent waiting for the chance to be executed \n\n\n\n")

st.write("#### Turnaround Time")
st.write("Time difference between the arrival of process and when it is done executing \n\n\n\n")

st.write("##### We try to minimise the waiting and turnaround time")