import pymysql

# Open the file in read mode
flag = False
valuesX = []
valuesY = []
with open('data.txt', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

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

        if line.strip() == "Messreihen (X,Y)":
            flag = True



# Database connection details
connection_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'oussama',
    'port': 3306
}


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

    data_to_insert = [(x, y,werkauftrag, date) for x, y in zip(valuesX, valuesY)]
  # SQL query to insert data.txt into the table
    insert_query = """
        INSERT INTO your_table (x, y,werkauftrag, datum)
        VALUES (%s, %s, %s,%s)
    """
    # Execute the SQL query for each data.txt row
    cursor.executemany(insert_query, data_to_insert)
    connection.commit()
    print("Data inserted successfully")

except pymysql.Error as e:
    print(f"Error connecting to MySQL database: {e}")

finally:
    # Close cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals() and connection.open:
        connection.close()
