# mongoDB에 컬렉션 데이터를 저장하는 모듈
# db fastapi-pj -> collection books -> document

from odmantic import Model

class BookModel(Model):
    keyword: str
    title: str 
    publisher: str
    price: int
    image: str

    class Config:
        collection = "books"