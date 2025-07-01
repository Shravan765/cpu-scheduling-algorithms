import streamlit as st
import heapq
import pandas as pd
import matplotlib.pyplot as plt

INF = 1000000

#if the arrival time is the same, the order is 0-1-2...
class Schedule_Process():
    def __init__(self, process_id:list, process_entry_time:list, process_duration:list):
        #id is expected to be in range 0 to n-1, where n is number of processes
        self.id_list = process_id
        self.entry_time = process_entry_time
        self.time_needed = process_duration
    
    #returns waiting time, turnaorund time and gantt log list of First Come First Serve Algorithm
    def fcfs(self):
        n:int = len(self.id_list)
        waiting_time = [0 for i in range(n)]
        turnaround_time = [0 for i in range(n)]
        gantt_log = []

        processes_done = set()
        time_spent_till_now:int = 0 #in seconds
        while(len(processes_done) != n):
            earliest_arrival_time:int = INF
            earliest_process = -1
            for id in range(n):
                if(id not in processes_done):
                    if(self.entry_time[id] < earliest_arrival_time):
                        earliest_arrival_time = self.entry_time[id]
                        earliest_process = id
            start_time = time_spent_till_now
            time_spent_till_now = max(time_spent_till_now, earliest_arrival_time) 
            waiting_time[earliest_process] = time_spent_till_now - self.entry_time[earliest_process]
            time_spent_till_now += self.time_needed[earliest_process] #time spent in running the process
            end_time = time_spent_till_now
            gantt_log.append([earliest_process, start_time, end_time])
            turnaround_time[earliest_process] = time_spent_till_now - self.entry_time[earliest_process]
            processes_done.add(earliest_process)
        return waiting_time, turnaround_time, gantt_log
    
    #returns waiting time and turnaorund time list of Shortest Job First Algorithm
    def sjf(self):
        n:int = len(self.id_list)
        waiting_time = [0 for i in range(n)]
        turnaround_time = [0 for i in range(n)]
        gantt_log = []

        processes_done = set()
        time_spent_till_now:int = 0 #in seconds
        processes_arrived = set()
        while(len(processes_done) != n):
            for id in range(n):
                if((id not in processes_done) and (self.entry_time[id] <= time_spent_till_now)):
                    processes_arrived.add(id)
            if(len(processes_arrived) == 0):
                earliest_arrival_time:int = INF
                for id in range(n):
                    if(id not in processes_done):
                        if(self.entry_time[id] < earliest_arrival_time):
                            earliest_arrival_time = self.entry_time[id]
                        
                time_spent_till_now = earliest_arrival_time #this is because only now have processes arrived
                for id in range(n):
                    if(id not in processes_done and self.entry_time[id]<=time_spent_till_now):
                        processes_arrived.add(id)
            
            shortest_time:int = INF
            shortest_process = -1
            for id in processes_arrived:
                if(self.time_needed[id]< shortest_time):
                    shortest_time = self.time_needed[id]
                    shortest_process = id
            waiting_time[shortest_process] = time_spent_till_now - self.entry_time[shortest_process]
            start_time = time_spent_till_now
            time_spent_till_now += self.time_needed[shortest_process]
            turnaround_time[shortest_process] = time_spent_till_now - self.entry_time[shortest_process]
            end_time = time_spent_till_now
            gantt_log.append([shortest_process, start_time, end_time])
            processes_arrived.remove(shortest_process)
            processes_done.add(shortest_process)
            #print(time_spent_till_now, "  ,process ",shortest_process," done , ",processes_arrived)    
        return waiting_time, turnaround_time, gantt_log
    
    #returns waiting time and turnaorund time list of Shortest Remaining Time First Algorithm
    def srtf(self):
        n:int = len(self.id_list)
        waiting_time = [0 for i in range(n)]
        turnaround_time = [0 for i in range(n)]
        gantt_log = []

        processes_done = set()
        priority_queue = []
        processes_in_queue = set()
        #we will break ties with entry time, hence we will add (remaining_time, entry_time, id)
        time:int = 0
        while(len(processes_done) != n):
            for id in range(n):
                if((id not in processes_done) and (self.entry_time[id] <= time) and (id not in processes_in_queue)):
                    heapq.heappush(priority_queue, (self.time_needed[id] , self.entry_time[id], id) )
                    processes_in_queue.add(id)
            
            process_running = -1
            if len(priority_queue) != 0:
                entry = heapq.heappop(priority_queue)
                process_running = entry[2]
                if(entry[0] == 1):
                    #process done 
                    gantt_log.append([process_running, time, time+1])
                    processes_done.add(process_running)
                    time+=1
                    turnaround_time[process_running] = time - self.entry_time[process_running]
                    processes_in_queue.remove(process_running)
                else:
                    gantt_log.append([process_running, time, time+1])
                    modified_entry = list(entry)
                    modified_entry[0] -=1
                    heapq.heappush(priority_queue, tuple(modified_entry))
                    time+=1
                #modifying waiting time for all processes in processes_in_queue
                for id in processes_in_queue:
                    if id != process_running:
                        waiting_time[id] +=1
            else:
                time+=1

        return waiting_time, turnaround_time, gantt_log

def avg(lis:list):
    return sum(lis)/len(lis)

def show_individual_data(waiting:list, turnaround:list):
    n = len(waiting)
    df = pd.DataFrame( [ [id+1, waiting[id], turnaround[id]] for id in range (n)], 
                      columns=["Process Id" , "Waiting Time" ,"Turnaround Time"] )
    df.set_index("Process Id", inplace=True)
    styled_df = df.style.background_gradient(subset=["Waiting Time", "Turnaround Time"],cmap="oranges")
    st.dataframe(df)

def plot_gantt(gantt_log):
    fig, ax = plt.subplots()
    for pid , start, end in gantt_log:
        ax.barh(y=0.5, width=end-start, left=start, height=0.3, label=f'P{pid}')
        ax.text(x=(start + end) / 2, y=0.5, s=f'P{pid}', va='center', ha='center')
    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    st.pyplot(fig)
    

number_of_processes = st.slider(label = "Number of processes", min_value=1, max_value=10)

st.write("#### Choose the entry time of every process and the time it will take from the slider")

id_list = [i for i in range(number_of_processes)]
process_entry_time = [0 for i in range(number_of_processes)]
process_duration = [0 for i in range(number_of_processes)]

for i in range(number_of_processes):
    process_entry_time[i] = st.slider(label = f"Entry time of Process {i+1}", min_value=0, max_value=100, key=f"e{i}")
    process_duration[i] = st.slider(label = f"Time required by Process {i+1}", min_value=1, max_value=100, key=f"t{i}")

scheduler = Schedule_Process(id_list, process_entry_time, process_duration)

st.write("##### (You can read about these scheduling algorithms on the other page!)")

if(st.checkbox(label="Run First Come First Serve 🖥" , key="fcfs")):
    fcfs_waiting_time, fcfs_turnaround_time, fcfs_gantt_chart = scheduler.fcfs()
    st.write(f"##### Average Waiting time = {round(avg(fcfs_waiting_time) , 3)}")
    st.write(f"##### Average Turnaround time = {round(avg(fcfs_turnaround_time) , 3)}")
    st.write("\n\n")
    if(st.checkbox("See Waiting and Turnaround Time of Individual Process In First Come First Serve" , key="fcfsshow")):
        show_individual_data(fcfs_waiting_time, fcfs_turnaround_time)
    st.write("\n\n")
    if(st.checkbox("See Visual representation of process execution In First Come First Serve " , key="fcfsgantt")):
        plot_gantt(fcfs_gantt_chart)

st.write("\n\n\n\n")
if(st.checkbox(label="Run Shortest Job First 🖥",key="sjf")):
    sjf_waiting_time, sjf_turnaround_time, sjf_gantt_chart = scheduler.sjf()
    st.write(f"##### Average Waiting time = {round(avg(sjf_waiting_time) , 3)}")
    st.write(f"##### Average Turnaround time = {round(avg(sjf_turnaround_time) , 3)}")
    st.write("\n\n")
    if(st.checkbox("See Waiting and Turnaround Time of Individual Process In Shortest Job First", key = "sjfshow")):
        show_individual_data(sjf_waiting_time, sjf_turnaround_time)
    st.write("\n\n")
    if(st.checkbox("See Visual representation of process execution In Shortest Job First" , key="sjfgantt")):
        plot_gantt(sjf_gantt_chart)

if(st.checkbox(label="Run Shortest Remaining Time First 🖥", key="srtf")):
    srtf_waiting_time, srtf_turnaround_time, srtf_gantt_chart = scheduler.srtf()
    st.write(f"##### Average Waiting time = {round(avg(srtf_waiting_time) , 3)}")
    st.write(f"##### Average Turnaround time = {round(avg(srtf_turnaround_time) , 3)}")
    st.write("\n\n")
    if(st.checkbox("See Waiting and Turnaround Time of Individual Process In Shortest Remaining Time First", key="srtfshow")):
        show_individual_data(srtf_waiting_time, srtf_turnaround_time)
    st.write("\n\n")
    if(st.checkbox("See Visual representation of process execution In Shortest Remaining Time First" , key="srtfgantt")):
        #processing gantt chart of srtf
        processed_srtf_gantt_chart = []
        current_id, start, end = srtf_gantt_chart[0]
        for pid, s, e in srtf_gantt_chart[1::]:
            if(pid == current_id):
                end = e
            else:
                processed_srtf_gantt_chart.append((current_id, start, end))
                current_id = pid
                start = s
                end = e
        processed_srtf_gantt_chart.append((current_id, start, end))
        plot_gantt(processed_srtf_gantt_chart)

