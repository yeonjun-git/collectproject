from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/") # @는 데코레이터 문법. 함수에 응답하는 것.
# 각각의 @app.get은 각각의 라우터에 해당한다.
# 웹 브라우저에서 url을 입력하면, 그에 해당하는 라우터를 찾아 함수를 실행해준다.
def read_root():
    return {"Hellos": "World"}

@app.get("/hello")
def read_fastapi():
    return {"Hellos": "FastAPI"}

@app.get("/items/{item_id}/{xyz}")
# 위 url을 동적 라우팅 이라고 한다.
# get이 받는 파라미터는 url의 정해진 포맷
# 이 포맷으로 요청 받은 app 인스턴스가 다음 라인의 함수를 실행하고 값을 응답한다.
def read_item(item_id: int, xyz: str, q: Union[str, None] = None):
    # code..
    return {"item_id": item_id, "xyz": xyz, "q": q}
# item_id, xyz는 필수 입력 url // q는 query를 뜻하며, Union을 사용하므로 필수 입력은 아님.
