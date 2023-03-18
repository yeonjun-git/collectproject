# terminal에서 uvicorn 명령어 실행하지 말고
# Python script로 uvicorn 실행하는 방법

import uvicorn

if __name__ == "__main__":
    uvicorn.run('app.project:app_project', host='localhost', port=8000, reload = True)

    