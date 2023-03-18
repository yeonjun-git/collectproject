# 연결할 DB의 client와 engine을 project 파일 안에서 전역 변수로 사용하기 위해
# 별도로 __init__.py 파일을 생성하고 client, engine을 저장한다.
# project 파일에서 __init__.py을 import 한 후 사용하면 된다.

#-----------------------------------------------------
# mongodb(NoSQL) connect library
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import Mongo_DB_Name, Mongo_Url
#-----------------------------------------------------

#-----------------------------------------------------
# pymongo.errors.ServerSelectionTimeoutError
## window 환경에서 R3 Certificate이 만료되어 발생하는 이슈
# Trouble Shooting
import certifi
# client 지정하는 부분에서 tlsCAFile = certifi.where() 설정
#-----------------------------------------------------
class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(Mongo_Url, tlsCAFile = certifi.where())
        self.engine = AIOEngine(client=self.client, database=Mongo_DB_Name)
        print("MongoDB connect Succeess.")
        print("MongoDB Name:", Mongo_DB_Name)

    def close(self):
        self.client.close()
        print("MongoDB disconnect Succeess.")


mongodb = MongoDB()