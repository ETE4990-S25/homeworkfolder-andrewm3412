import time 
import os
import threading
import re
import matplotlib.pyplot as plt

Log_count = {
    'INFO': 0,
    'WARNING':0,
    'ERROR':0,
    'CRITICAL':0
}

def parse_log_line(line):
        pattern = r"^(.*?)\s\|\s(.*?)\|\s(INFO|WARNING|ERROR|CRITICAL)\|\s(.*)$"
        match = re.match(pattern, line)
        if match:
            return{
                "timestamp": match.group(1),
                "logger": match.group(2),
                "level": match.group(3),
                "message": match.group(4)
            }

def watch_log_file(filname):
    print(f"Waiting for {filname} to be created...")
    while not os.path.exists(filname):
        time.sleep(1)
    
    print(f"Now monitoring: {filname}")
    with open (filname, 'r') as file:
        file.seek(0)

        while True:
            line = file.readline()
            if line:
                log = parse_log_line(line)
                if log:
                    level = log["level"]
                    Log_count[level] += 1
                    print_summary()
                    if level == "CRITICAL":
                        print(f"[CRITCAL] {log['timestamp']} | {log['logger']}| {log['message']}")
                        print('-' *30)
            time.sleep(1)


def print_summary():
    print("\nLog Summary: ")
    for level,count in Log_count.items():
        print(f"{level}: {count}")
    print("-"*30)

def update_graph(log_summary):
    plt.clf()
    levels = list(log_summary.keys())
    count = list(log_summary.values())

    plt.bar(levels,count, color = ['blue', 'orange', 'red', 'green'])
    plt.title('Log Level Distribution')
    plt.xlabel('Log Level')
    plt.ylabel('Count')
    plt.pause(0.1)

def initialize_graph():
    plt.ion()
    plt.figure(figsize=(10,6))
    update_graph(Log_count)
    plt.show

def star_monitoring():
    log_filename = "app.log"
    watch_thread = threading.Thread(target=watch_log_file, args=(log_filename,))
    watch_thread.daemon = True
    watch_thread.start()

if __name__ == "__main__":
    initialize_graph()
    star_monitoring()
    while True:
        time.sleep(1)


