#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
#print(sys.path)
from Method.Utility.Gpt_summary import gpt_summary_method
import requests

# API 키와 검색어 설정
API_KEY = "AIzaSyD3lgO2kgp0xk9bh1zOiZE9yYyRZ2Ybvs4"  # 여기에 실제 API 키를 입력하세요.
SEARCH_QUERY = "버리는법"

# YouTube Data API v3 검색 요청을 위한 파라미터 설정
params = {
    'part': 'snippet',
    'q': SEARCH_QUERY,
    'type': 'video',
    'maxResults': 3,
    'regionCode': 'KR',
    'videoDuration': 'short',
    'key': API_KEY
}

# YouTube Data API v3 검색 URL
url = "https://www.googleapis.com/youtube/v3/search"

# 요청 보내기
response = requests.get(url, params=params)

# 응답에서 데이터 추출
data = response.json().get('items', [])

# 요약 클래스 활성화
summary = gpt_summary_method()

# 결과 출력
with open("output.txt", "a") as file:
    for content in data:
        video_title = content['snippet']['title']
        video_id = content['id']['videoId']
        description = content['snippet']['description']
        author = content['snippet']['channelTitle']

        output_line = f"제목 : {video_title}, URL : https://www.youtube.com/watch?v={video_id}\n"
        
        file.write(output_line)
        print(output_line)

        summary_result = summary.start(video_id, video_title, description, author)
        summary_line = f'{str(summary_result)}\n'

        file.write(summary_line)
        print(summary_line)
