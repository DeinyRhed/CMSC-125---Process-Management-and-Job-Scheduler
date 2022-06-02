   
"""
CMSC 125 - Machine Problem 2: Processor Management and Job Scheduling
Programmed by: Dianne M. Mondido
Reference:  Guru99 (7 May, 2022). Shortest Job First (SJF): Preemptive, Non-Preemptive Example. Retrieved from https://www.guru99.com/shortest-job-first-sjf-scheduling.html
            StudyTonight. Round Robin Scheduling. Retrieved From https://www.studytonight.com/operating-system/round-robin-scheduling


"""

class Process:
    def __init__(self, index:int, arrivalTime:int, burstTime:int, priority:int):
        self.__index = index
        self.__arrival = arrivalTime
        self.__burst = burstTime
        self.__priority = priority

    def arrivalTime(self):
        return self.__arrival

    def burstTime(self):
        return self.__burst

    def priorityNum(self):
        return self.__priority

    def __str__(self):
        return f'Process {str(self.__index)}'


# Scheduling Algorithms 

# First Come First Serve Scheduling 
def fcfs(processList:'list[Process]'):
    tableFormat = ''
    currentWaitingTime = 0
    currentTurnaroundTime = 0
    averageWaitingTime = 0
    averageTurnaroundTime = 0

    # Loop through the process.
    for process in processList:
        currentTurnaroundTime += process.burstTime()
        averageTurnaroundTime += currentTurnaroundTime
        tableFormat += f'\t{process}\t\t{currentWaitingTime}\t\t\t{currentTurnaroundTime}\n'
        averageWaitingTime += currentWaitingTime
        currentWaitingTime += process.burstTime()
    
    return {'str': tableFormat, 'averageWaitingTime': averageWaitingTime/len(processList), 'averageTurnaroundTime': averageTurnaroundTime/len(processList)}

# Shortest Job First Scheduling
def sjf(processList:'list[Process]'):
    tableFormat = ''
    currentWaitingTime = 0
    currentTurnaroundTime = 0
    averageWaitingTime = 0
    averageTurnaroundTime = 0

    # Loop through the process list arranged in ascending order in terms of burst time 
    for process in sorted(processList, key = lambda process:process.burstTime()):
        currentTurnaroundTime += process.burstTime()
        averageTurnaroundTime += currentTurnaroundTime
        tableFormat += f'\t{process}\t\t{currentWaitingTime}\t\t\t{currentTurnaroundTime}\n'
        averageWaitingTime += currentWaitingTime
        currentWaitingTime += process.burstTime()
        
    return {'str': tableFormat, 'averageWaitingTime': averageWaitingTime/len(processList), 'averageTurnaroundTime': averageTurnaroundTime/len(processList)}

# Priority Scheduling
def priority(processList:'list[Process]'):
    tableFormat = ''
    currentWaitingTime = 0
    currentTurnaroundTime = 0
    averageWaitingTime = 0
    averageTurnaroundTime = 0

    # Loop through the process list arranged in ascending order in terms of priority
    for process in sorted(processList, key = lambda process:process.priorityNum()):
        currentTurnaroundTime += process.burstTime()
        averageTurnaroundTime += currentTurnaroundTime
        tableFormat += f'\t{process}\t\t{currentWaitingTime}\t\t\t{currentTurnaroundTime}\n'
        averageWaitingTime += currentWaitingTime
        currentWaitingTime += process.burstTime()
        
    return {'str': tableFormat, 'averageWaitingTime': averageWaitingTime/len(processList), 'averageTurnaroundTime': averageTurnaroundTime/len(processList)}

# Shortest Remaining Processing Time Scheduling
def srpt(processList:'list[Process]'):
    srptList = [{'process': process, 'waitingTime': 0, 'turnaroundTime': 0, 'remainingBurstTime': process.burstTime()} for process in processList]

    min = 99999
    tableFormat = ''
    completedProcesses = 0          
    currentTime = 0                                  
    shortestProcess = None                   
    shortestProcess_check = False      
    averageWaitingTime = 0
    averageTurnaroundTime = 0      

    while completedProcesses != len(srptList):
        # Finds lowest burst time
        for process in srptList:
            if ((process['process'].arrivalTime() <= currentTime) and (process['remainingBurstTime'] < min) and (process['remainingBurstTime'] > 0)):
                min = process['remainingBurstTime']
                shortestProcess = process
                shortestProcess_check = True
        
        # If shortest process still the same, just increment the time and continue
        if (not shortestProcess_check):
            currentTime += 1
            continue
        
        # Reduce remaining burst time of shortest process by one
        shortestProcess['remainingBurstTime'] -= 1

        # Update min value
        min = shortestProcess['remainingBurstTime']
        if (min == 0):
            min = 99999

        # If shortest process reaches zero, add one to completedProcesses
        if (shortestProcess['remainingBurstTime'] == 0):
            completedProcesses += 1
            shortestProcess_check = False

            # since this process is considered done when it reaches here, we can set final waitingTime and turnaroundTime values here
            shortestProcess['waitingTime'] = ((currentTime + 1) - shortestProcess['process'].burstTime() - shortestProcess['process'].arrivalTime())
            shortestProcess['turnaroundTime'] = shortestProcess['process'].burstTime() + shortestProcess['waitingTime']

            if (shortestProcess['waitingTime'] < 0):
                shortestProcess['waitingTime'] = 0
        
        currentTime += 1


    for process in srptList:
        averageWaitingTime += process['waitingTime']
        averageTurnaroundTime += process['turnaroundTime']
        tableFormat += f"\t{process['process']}\t\t{process['waitingTime']}\t\t\t{process['turnaroundTime']}\n"

    return {'str': tableFormat, 'averageWaitingTime': averageWaitingTime/len(processList), 'averageTurnaroundTime': averageTurnaroundTime/len(processList)}

# Round Robin Scheduling
def roundrobin(processList:'list[Process]', quantum = 4):
    rrList = [{'process': process, 'waitingTime': 0, 'turnaroundTime': 0, 'remainingBurstTime': process.burstTime()} for process in processList]
    tableFormat = ''
    turnaroundTime = 0 
    averageWaitingTime = 0
    averageTurnaroundTime = 0

    while True:
        ifDone = True

        for process in rrList:
            # Check if a process has remaining burst time. If true, then there are pending time
            if process['remainingBurstTime'] > 0:
                ifDone = False

                # Check if remaining burst time is greater than quantum.
                if process['remainingBurstTime'] > quantum:
                    turnaroundTime += quantum
                    process['remainingBurstTime'] -= quantum
                else:
                    turnaroundTime = turnaroundTime + process['remainingBurstTime']
                    process['remainingBurstTime'] = 0
                    # Since this process is considered done when it reaches here, set the final waitingTime and turnaroundTime values here
                    process['waitingTime'] = turnaroundTime - process['process'].burstTime()
                    process['turnaroundTime'] = process['process'].burstTime() + process['waitingTime']
        
        if ifDone:
            break

    for process in rrList:
        averageWaitingTime += process['waitingTime']
        averageTurnaroundTime += process['turnaroundTime']
        tableFormat += f"\t{process['process']}\t\t{process['waitingTime']}\t\t\t{process['turnaroundTime']}\n"

    return {'str': tableFormat, 'averageWaitingTime': averageWaitingTime/len(processList), 'averageTurnaroundTime': averageTurnaroundTime/len(processList)}


# Print Result
def print_results(processInfo):
    print(f'\t ----------------- {processInfo[0]} -----------------')
    print('\tPROCESSES\tWaiting Time (ms)\tTurnaround Time (ms)\n')
    print(processInfo[1]["str"])
    print(f'\tAverage Waiting Time: {"%.2f" % processInfo[1]["averageWaitingTime"]} ms')
    print(f'\tAverage Turnaround Time: {"%.2f" % processInfo[1]["averageTurnaroundTime"]} ms')
    print()

def main():
    processList = []

    with open('./sample data/process1.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            row = line.split()
            processList.append(Process(int(row[0]), int(row[1]), int(row[2]), int(row[3])))

    FCFS = ('First Come First Serve Scheduling ', fcfs(processList))
    SJF = ('Shortest Job First Scheduling', sjf(processList))
    SRPT = ('Shortest Remaining Processing Time Scheduling', srpt(processList))
    PS = ('Priority Scheduling', priority(processList))
    RRS = ('Round Robin Scheduling', roundrobin(processList))

    print_results(FCFS)
    print_results(SJF)
    print_results(SRPT)
    print_results(PS)
    print_results(RRS)

    # Scheduling Algorithms evaluation
    scheduleAlgorithm = [FCFS, SJF, SRPT, PS, RRS]

    print('\t----- ALGORITHM EVALUATION -----\n')

    rank = 0
    print("\tLowest to Highest algorithm average waiting time:")
    for scheduler in sorted(scheduleAlgorithm, key = lambda scheduler: scheduler[1]["averageWaitingTime"]):
        print(f'\t\t[{rank+1}] {scheduler[0]} ({"%.2f" % scheduler[1]["averageWaitingTime"]} ms)')
        rank += 1
    print()

    rank = 0
    print("\tLowest to Highest algorithm average turnaround time:")
    for scheduler in sorted(scheduleAlgorithm, key = lambda scheduler: scheduler[1]["averageTurnaroundTime"]):
        print(f'\t\t[{rank+1}] {scheduler[0]} ({"%.2f" % scheduler[1]["averageTurnaroundTime"]} ms)')
        rank += 1
    print()

main()

