import os
import pymysql

# Directory path
directory = 'my_folder'
connection_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'oussama',
    'port': 3306
}

# Create a new file to store the imported files
importedData = 'imported_files.txt'
file_path = os.path.join("", importedData)
# Create a new file
if not os.path.exists(importedData):

    file_path = os.path.join("", importedData)
    # Create a new file
    with open(file_path, 'w') as file:
        print(f"File '{importedData}' created in main project'.")

#get the treated files from the file importedData
treatedDataFile=[]
with open(importedData, 'r') as fileToTreat:
    lines = fileToTreat.readlines()
    for i, line in enumerate(lines, start=1):
        if line.strip():
            treatedDataFile.append(line.rstrip('\n'))

print("the treated data are : ",treatedDataFile)

# List all files in the directory
files = os.listdir(directory)

# Filter out only the .txt files
txt_files = [file for file in files if file.endswith('.txt')]

# Display the names of the .txt files
files=[]
for file in txt_files:

    files.append(file)


for file in files:
    if not file in treatedDataFile:
        # Open the file in append mode and write the new line
        with open(file_path, 'a') as tr:
            if not os.path.getsize(file_path) ==0:
                tr.write('\n')  # Add a newline character before appending the new line
            new_line = file
            tr.write(new_line)

        print("New line written to the file.")

        # Open the file in read mode
        flag = False
        valuesX = []
        valuesY = []
        flag2 = False
        valuesX1 = []
        valuesYu = []
        valuesYo = []
        with open('my_folder/' + file, 'r') as fileToTreat:
            # Read all lines from the file
            lines = fileToTreat.readlines()

            x = ""
            y = ""
            # Display each line with its line number
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

                if i ==18:
                    valuesX1.extend([str(val) for val in line.strip().split()])
                if i ==19:
                    valuesYu.extend([str(val) for val in line.strip().split()])
                if i ==21:
                    valuesYo.extend([str(val) for val in line.strip().split()])


                if line.strip() == "Messreihen (X,Y)":
                    flag = True


        # Database connection details

        try:
            connection = pymysql.connect(**connection_config)
            print("Connected to MySQL database")
            cursor = connection.cursor()

            create_table_query = """
                    CREATE TABLE IF NOT EXISTS your_table (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        x int(10),
                        y int(10),
                        werkauftrag varchar(255),
                        datum varchar(255)
                    )
                """

            # Execute the SQL query
            cursor.execute(create_table_query)
            print("Table created successfully or already exists")

            data_to_insert = [(x, y, werkauftrag, date) for x, y in zip(valuesX, valuesY)]
            # SQL query to insert data1.txt into the table
            insert_query = """
                    INSERT INTO your_table (x, y,werkauftrag, datum)
                    VALUES (%s, %s, %s,%s)
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

            data_to_insert = [(x, yo,yu, werkauftrag, date) for x, yu,yo in zip(valuesX1, valuesYu,valuesYo)]
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





