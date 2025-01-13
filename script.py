import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'weather_info': 'hello!'}


if __name__ == '__main__':
    uvicorn.run('script:app', reload=True)
