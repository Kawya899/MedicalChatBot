import sqlite3

def print_all_tables_data():
    try:
        conn = sqlite3.connect('medical_chatbot.db')
        cur = conn.cursor()

        # Get the list of tables in the database
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        print("Database connection successful!\n")
        print("Tables and their data:\n")

        for (table_name,) in tables:
            print(f"--- Table: {table_name} ---")
            cur.execute(f"SELECT * FROM {table_name};")
            rows = cur.fetchall()

            # Fetch column names for better formatting
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = [info[1] for info in cur.fetchall()]

            # Print column headers
            print(" | ".join(columns))

            if rows:
                for row in rows:
                    print(" | ".join(str(item) if item is not None else "NULL" for item in row))
            else:
                print("[No data in this table]")
            print("\n")

        conn.close()

    except Exception as e:
        print("Database connection failed:", str(e))

if __name__ == '__main__':
    print_all_tables_data()
