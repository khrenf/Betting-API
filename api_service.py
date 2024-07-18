from fastapi import FastAPI
import db
import threading
import time
from analyze_props import main as analyze_props
import uvicorn

def update_database():
    """
    Pulls props every 10 minutes and updates database. Resets database every day.
    """
    count = 0
    while True:
        if count == 144:
            count = 0
            db.reset_table()
        props = analyze_props()
        for prop in props:
            try:
                db.add_prop_to_table(prop)
            except:
                print("error adding prop to table")
        count += 1
        time.sleep(600)

app = FastAPI()
@app.get("/props")
def get_props():
    """
    Fetches all props from database and returns
    """
    props = db.fetch_props()
    return props

if __name__ == '__main__':
    db.create_table()
    update_thread = threading.Thread(target=update_database)
    update_thread.daemon = True
    update_thread.start()
    uvicorn.run(app, host='127.0.0.1', port=8000)