from fastapi import FastAPI
from analyze_props import main as analyze_props
import db

app = FastAPI()

@app.get("/props")
def get_props():
    props = db.fetch_props()
    return props

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
