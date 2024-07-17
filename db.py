import sqlite3
connection = sqlite3.connect("props_db.db")
cursor = connection.cursor()
from datetime import datetime
import json

def create_table():
    connection = sqlite3.connect("props_db.db")
    cursor = connection.cursor()    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS PropsTable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT,
        stat TEXT,
        prizepicks_line TEXT,
        underdog_line TEXT,
        draftkings_line TEXT,
        draftkings_over TEXT,
        draftkings_under TEXT,
        fanduel_line TEXT,
        fanduel_over TEXT,
        fanduel_under TEXT,
        time TEXT
    );
    """
    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()

def add_prop_to_table(prop):
    connection = sqlite3.connect("props_db.db")
    cursor = connection.cursor()  
    insert_row = """
    INSERT INTO PropsTable (
        player,
        stat,
        prizepicks_line,
        underdog_line,
        draftkings_line,
        draftkings_over,
        draftkings_under,
        fanduel_line,
        fanduel_over,
        fanduel_under,
        time
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cursor.execute(insert_row, (
        prop["player"],
        prop["stat"],
        prop["prizepicks_line"],
        prop["underdog_line"],
        prop["draftkings_line"],
        prop["draftkings_over"],
        prop["draftkings_under"],
        prop["fanduel_line"],
        prop["fanduel_over"],
        prop["fanduel_under"],
        datetime.now().replace(microsecond=0)
    ))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting {prop}: {e}")
    finally:
        connection.close()

def fetch_props():
    connection = sqlite3.connect("props_db.db")
    cursor = connection.cursor()
    get_all = """
    SELECT * FROM PropsTable;
    """
    rows = []
    try:
        cursor.execute(get_all)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching props: {e}")
    finally:
        connection.close()
    props = []
    for row in rows:
        old_time = datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S")
        time_since = str(datetime.now().replace(microsecond=0) - old_time)
        time_since = time_since.split(":")
        time_message = f"{time_since[0]} hours, {time_since[1]} minutes, {time_since[2]} seconds"
        prop_item = {
                "player": row[1],
                "stat": row[2],
                "prizepicks_line": row[3],
                "underdog_line": row[4],
                "draftkings_line": row[5],
                "draftkings_over": row[6],
                "draftkings_under": row[7],
                "fanduel_line": row[8],
                "fanduel_over": row[9],
                "fanduel_under": row[10],
                "time_elapsed": time_message
            }
        props.append(prop_item)
    return props
    

if __name__ == '__main__':
    create_table()
    # add_prop_to_table(
    #     {"player": "Jose Siri", "stat": "Total Bases", "prizepicks_line": "0.5", "underdog_line": "0.5", "draftkings_line": "-1", "draftkings_over": "-1", "draftkings_under": "-1", "fanduel_line": "-1", "fanduel_over": "-1", "fanduel_under": "-1"}
    # )
    print(fetch_props())


