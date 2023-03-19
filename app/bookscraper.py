# 동시성 프로그래밍으로 각각의 api로 요청해서 페이지 데이터를 스크래핑하는 모듈

import aiohttp
import asyncio
from app.config import get_secret

class NaverBookScraper:

    Naver_Api_Book = "https://openapi.naver.com/v1/search/book"
    Naver_Api_Id = get_secret("Naver_Api_Id")
    Naver_Api_Secret = get_secret("Naver_Api_Secret")


    @staticmethod # 정적메서드: 인스턴스를 만들지 않고 클래스 이름으로 직접 호출.
    async def fetch(session, url, headers):
        async with session.get(url, headers = headers) as response:
            if response.status == 200:
                result = await response.json()
                return result['items']


    # 1. keword와 start를 입력받아 url, header를 리턴하는 인스턴스 메서드
    def unit_url(self, keyword, start):
        return {
            "url": f"{self.Naver_Api_Book}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.Naver_Api_Id,
                "X-Naver-Client-Secret": self.Naver_Api_Secret,
            }
        }

    # 2. keword와 total page를 입력받아 unit_url 메서드를 이용해 url과 header를 저장
    #    저장한 url, header을 이용해 fetch 메서드를 통해 데이터 접근
    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1+i*10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result
            

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))
    

# Book Scraper 테스트해보기싶으면 이 파일을 실행해본다.    
if __name__ == "__main__":
    scraper = NaverBookScraper()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(scraper.run("파이썬", 1))

    