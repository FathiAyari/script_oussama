import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pymysql

# Directory path
connection_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'oussama',
    'port': 3306
}


def treat_data(file_path):
    flag = False
    valuesX = []
    valuesY = []
    flag2 = False
    valuesX1 = []
    valuesYu = []
    valuesYo = []
    flag_write = False
    done_getting_max = False
    with open(file_path, 'r') as fileToTreat:
        # Read all lines from the file
        lines = fileToTreat.readlines()

        x = ""
        y = ""
        line_index = 0

        for i, line in enumerate(lines, start=1):
            if i == 5:
                date = line.strip().split(":")[1]
            if i == 6:
                werkauftrag = line.strip().split(":")[1]

            if flag:
                if i % 2 == 0:
                    valuesX.extend([int(val) for val in line.strip().split()])
                else:
                    valuesY.extend([int(val) for val in line.strip().split()])

                    flag_write = True
            if i == 18:
                valuesX1.extend([str(val) for val in line.strip().split()])
            if i == 19:
                valuesYu.extend([str(val) for val in line.strip().split()])
            if i == 21:
                valuesYo.extend([str(val) for val in line.strip().split()])

            if line.strip() == "Messreihen (X,Y)":
                flag = True

            if flag_write:

                try:
                    connection = pymysql.connect(**connection_config)
                    print("Connected to MySQL database")
                    cursor = connection.cursor()

                    create_table_query = """
                        CREATE TABLE IF NOT EXISTS your_table (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            line_index int(10),
                            x int(10),
                            y int(10),
                            werkauftrag varchar(255),
                            datum varchar(255)
                        )
                    """
                    cursor.execute(create_table_query)
                    print("Table created successfully or already exists")

                    get_max_index_query = """select  max(line_index) from your_table"""
                    cursor.execute(get_max_index_query)
                    max_index = cursor.fetchone()[0]

                    if max_index is None:
                        line_index += 1
                    elif not done_getting_max:
                        line_index = max_index + 1
                        done_getting_max = True
                    else:
                        line_index += 1



                    data_to_insert = [(line_index, x, y, werkauftrag, date) for x, y in zip(valuesX, valuesY)]
                    # SQL query to insert data1.txt into the table
                    insert_query = """
                        INSERT INTO your_table (line_index,x, y,werkauftrag, datum)
                        VALUES (%s, %s, %s,%s,%s)
                    """
                    # Execute the SQL query for each data1.txt row
                    cursor.executemany(insert_query, data_to_insert)
                    connection.commit()
                    print("Data inserted successfully to your_table")

                    ###############################################################################

                    create_table2_query = """
                        CREATE TABLE IF NOT EXISTS your_table2 (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            x varchar(255),
                            yu varchar(255),
                            yo varchar(255),
                            werkauftrag varchar(255),
                            datum varchar(255)
                        )
                    """

                    # Execute the SQL query
                    cursor.execute(create_table2_query)
                    print("Table created successfully or already exists")

                    data_to_insert = [(x, yo, yu, werkauftrag, date) for x, yu, yo in zip(valuesX1, valuesYu, valuesYo)]
                    # SQL query to insert data1.txt into the table
                    insert_query = """
                        INSERT INTO your_table2 (x, yu,yo,werkauftrag, datum)
                        VALUES (%s, %s,%s, %s,%s)
                    """
                    # Execute the SQL query for each data1.txt row
                    cursor.executemany(insert_query, data_to_insert)
                    connection.commit()
                    print("Data inserted successfully to your_table2")
                except pymysql.Error as e:
                    print(f"Error connecting to MySQL database: {e}")
                finally:
                    # Close cursor and connection
                    if 'cursor' in locals():
                        cursor.close()
                    if 'connection' in locals() and connection.open:
                        connection.close()
                valuesX = []
                valuesY = []
                flag_write = False

    # Database connection details


class MyHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

    def log_event(self, event_type, file_path):
        with open(self.log_file, 'a') as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            username = os.getenv('USER') or os.getenv('USERNAME')  # Get current user
            f.write(f"{timestamp} - {username} - {event_type}: {file_path}\n")

    def on_any_event(self, event):
        if event.is_directory:
            return  # Ignore directory events

        if event.event_type == 'created':

            self.log_event('Created', event.src_path)
            treat_data(event.src_path)
        elif event.event_type == 'deleted':

            self.log_event('Deleted', event.src_path)


# Function to start the observer
def start_observer(directory, log_file):
    event_handler = MyHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"Watching directory: {directory}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Directory to monitor
directory_to_monitor = "my_folder"

# Log file
log_file = "log.txt"

# Start monitoring the directory
start_observer(directory_to_monitor, log_file)
