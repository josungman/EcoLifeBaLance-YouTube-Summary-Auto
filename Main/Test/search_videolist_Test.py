#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Gpt_summary import gpt_summary_method
from googleapiclient.discovery import build
import json
import re


def get_channel_id(url):
    # 유튜브 채널 URL에서 'UC'로 시작하는 채널 ID를 추출하는 정규 표현식
    pattern = r'youtube\.com\/channel\/(UC[-_A-Za-z0-9]{21}[AQgw])'
    match = re.search(pattern, url)

    if match:
        # 정규 표현식에 해당하는 부분을 찾으면, 그 부분을 반환
        return match.group(1)
    else:
        # 채널 ID를 찾지 못하면 None 반환
        return None

def get_video_links(api_key, channel_url):
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = get_channel_id(channel_url)

    video_links = []
    #유튜브 영상 중간(4~20분사이)
    request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=150, type='video',regionCode='KR',videoDuration='medium')
    response = request.execute()

    for item in response['items']:
        
        # 요약 클래스 활성화
        summary = gpt_summary_method()

        # 결과 변수
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        description = item['snippet']['description']
        author = item['snippet']['channelTitle']
        thumbnail = item['snippet']['thumbnails']['high']

        summary_result = '-'
        summary_result = summary.start(video_id, video_title, description, author)
       
        with open('./Output_File/videolist_test.json', 'w', encoding='utf-8') as f:
            video_links.append({"title": item['snippet']['title'],"thumbnail_link": thumbnail,"link": video_link,"video_id" : video_id,"description" : item['snippet']['description'],"author" : item['snippet']['channelTitle'],"video_summary" : summary_result})
            json.dump(video_links, f, indent=4, ensure_ascii=False)
        print('check')

    # 결과를 JSON 파일로 저장
    #with open('video_links.json', 'w', encoding='utf-8') as f:
    #    json.dump(video_links, f, indent=4, ensure_ascii=False)

    print("동영상 목록이 'videolist_test.json' 파일에 저장되었습니다.")

#우정
#https://www.youtube.com/channel/UCx3R_KdwgaqCaEmaRAe_NOg

#클린 어밴져스
#https://www.youtube.com/channel/UCBcm-pxUmI5CUnhZSMGbvWQ


#if __name__ == '__main__': Test시 활성화하기(구어체 안먹힘 추후 다시 셋팅 해보기)
    api_key = 'AIzaSyD3lgO2kgp0xk9bh1zOiZE9yYyRZ2Ybvs4' 
    channel_url = input("YouTube 채널 URL을 입력하세요: ")
    get_video_links(api_key, channel_url)