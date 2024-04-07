#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Detection_Driver import make_driver
from Method.Utility.Logins import logins
from Method.Custom_Selenium.WJ_Cafe_Method import Wj_Cafe_Method

class Test:

    def __init__(self):  #init

          #언디텍티드 드라이브 init
            self.driver = make_driver()

            #로그인메서드 init
            self.logins = logins(self.driver)

            # 계정 파일 열기
            with open('WJ_Account.txt', 'r') as file:
                # 파일에서 첫 번째 줄 읽기
                line = file.readline().strip()  # strip()을 사용하여 줄바꿈 문자 제거    
                # 쉼표로 구분하여 ID와 PW 추출
                ID, PW = line.split(',')

            #로그인 전역 변수
            self.wj_ID = ID
            self.wj_PW = PW

            #초기 로그인
            self.logins.wj_login(self.wj_ID,self.wj_PW)

    def wj_Cafe_Method_test(self):

          #Test_data(매직tv : 0초 사진 엉뚱한데에 입력됨.)
          video_summary_result = {
    "title": "냉장고 청소방법 /손얼룩 제거 방법 /대박 쉬운 냉장고 청소방법 공개 /매직청소TV[이미지 포함]",
    "thumbnail_link": {
        "url": "https://i.ytimg.com/vi/jav7gelVWYg/hqdefault.jpg",
        "width": 480,
        "height": 360
    },
    "link": "https://www.youtube.com/watch?v=jav7gelVWYg",
    "video_id": "jav7gelVWYg",
    "description": "매직청소TV 공식 청소용품 쇼핑몰 OPEN https://smartstore.naver.com/magiccleantv 생활에 꼭 필요한 청소 방법을 알려드리고 있는 ...",
    "author": "매직청소TV",
    "video_summary": "<h1><span style=\"font-size: 26px;\">냉장고 청소방법 /손얼룩 제거 방법 /대박 쉬운 냉장고 청소방법 공개 /매직청소TV[이미지 포함]</span></h1> <br> <iframe width=\"912\" height=\"514\" src=\"https://www.youtube.com/embed/jav7gelVWYg\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen=\"\"></iframe><br><h2><span style=\"font-size: 22px;\">한 문장 요약</span></h2><span style='margin: 20px 0px;'>매직청소TV에서는 냉장고 청소와 손 얼룩 제거 방법을 쉽고 빠르게 알려주며, 린스나 컨디셔너를 활용한 친환경적인 청소 방법을 제시합니다.🧹🍃</span><br><h2><span style=\"font-size: 22px;\">동영상 하이라이트</span></h2><details open>    <summary><strong>접기 또는 펼치기👆</strong></summary><table class=\"m-table-style noBorder\" style=\"width: 100%;\">\t<tbody>\t\t<tr>\t\t\t<td style=\"width: 50%; text-align: center;\">\t\t\t\t<div style=\"text-align: left;\"><strong>00:00</strong><sub>(0초)</sub> 매직청소TV가 냉장고 청소와 손 얼룩 제거 방법을 소개합니다.🎬</div>\t\t\t</td>\t\t\t<td style=\"width: 50%; text-align: center;\">\t\t\t\t<p style=\"text-align: left;\"><strong>00:24</strong><sub>(24초)</sub> 준비물로 간단한 물과 린스 또는 컨디셔너가 필요하며, 이를 활용한 친환경적인 청소 방법을 알려줍니다.🍃</p>\t\t\t</td>\t\t</tr>\t\t<tr>\t\t\t<td style=\"width: 50%; text-align: center;\">24초-캡쳐이미지</td>\t\t\t<td style=\"width: 50%; text-align: center;\">0초-캡쳐이미지</td>\t\t</tr>\t\t<tr>\t\t\t<td style=\"width: 50%; text-align: center;\">\t\t\t\t<div style=\"text-align: left;\"><strong>01:45</strong><sub>(105초)</sub> 물과 린스를 섞은 후, 이를 청소용 걸레에 적셔 냉장고를 닦는 과정을 보여줍니다.💦</div>\t\t\t</td>\t\t\t<td style=\"width: 50%; text-align: center;\">\t\t\t\t<p style=\"text-align: left;\"><strong>03:31</strong><sub>(211초)</sub> 냉장고의 손잡이 부분을 청소하는 방법을 알려주며, 얼룩이 하나도 없어진 깨끗한 결과를 보여줍니다.✨</p>\t\t\t</td>\t\t</tr>\t\t<tr>\t\t\t<td style=\"width: 50%; text-align: center;\">105초-캡쳐이미지</td>\t\t\t<td style=\"width: 50%; text-align: center;\">211초-캡쳐이미지</td>\t\t</tr>\t</tbody></table></details><br> <span style=\"color: rgb(204, 204, 204);\">▶ 위 내용은 GPT를 통해 요약되었습니다.</span> <br> <span style=\"color: rgb(204, 204, 204);\">▶ 출처 URL : https://www.youtube.com/watch?v=jav7gelVWYg</span>",
    "caption_check": True,
    "summary_timestamp_links": [
        {
            "timestamp_link": "https://www.youtube.com/watch?v=jav7gelVWYg&t=0"
        },
        {
            "timestamp_link": "https://www.youtube.com/watch?v=jav7gelVWYg&t=24"
        },
        {
            "timestamp_link": "https://www.youtube.com/watch?v=jav7gelVWYg&t=105"
        },
        {
            "timestamp_link": "https://www.youtube.com/watch?v=jav7gelVWYg&t=211"
        }
    ],
    "video_screenshot_paths": [
        {
            "video_screenshot_path": "file://C:/Python_Project/youtube_summary_project_V1/dist/Youtube_screenshots/jav7gelVWYg/0.png"
        },
        {
            "video_screenshot_path": "file://C:/Python_Project/youtube_summary_project_V1/dist/Youtube_screenshots/jav7gelVWYg/24.png"
        },
        {
            "video_screenshot_path": "file://C:/Python_Project/youtube_summary_project_V1/dist/Youtube_screenshots/jav7gelVWYg/105.png"
        },
        {
            "video_screenshot_path": "file://C:/Python_Project/youtube_summary_project_V1/dist/Youtube_screenshots/jav7gelVWYg/211.png"
        }
    ]
}
          
          wj_Cafe_Method = Wj_Cafe_Method(self.driver)
          wj_Cafe_Method.wj_webpage_reg_method(video_summary_result)


#test하기
test = Test()
test.wj_Cafe_Method_test()