#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../')
sys.path.append(utility_path)
from Method.Utility.Gpt_summary import gpt_summary_method
from Method.Utility.Detection_Driver import make_driver
from Method.Utility.Logins import logins
from Method.Utility.Log import Log
from Method.Commom_DB.DB import Common_DB
from Method.Custom_Selenium.WJ_Cafe_Method import Wj_Cafe_Method
from Method.Project_Exclusive_Method.Summary_Timestamp_Parse import Summary_Timestamp_Parse
from Method.Project_Exclusive_Method.Youtube_Timestamp_Screenshot import Youtube_Timestamp_Screenshot
from googleapiclient.discovery import build
import re
from time import sleep
import datetime
import json
from cachetools import cached, TTLCache

# 캐시 크기와 TTL(Time-To-Live)을 설정합니다. 여기서는 최대 100개의 항목을 10분 동안 저장합니다.
cache = TTLCache(maxsize=100, ttl=600)

class Integrated_code: #통합 작업

    def __init__(self,drive,ID,PW):  #init

       try:
            #업체별 카운트 변수
            self.count = 0

            #업체별 카운트 최대 등록 변수
            self.channel_max_count = 5

            #로그 init
            log = Log()
            self.log = log.activate()

            # 요약 파싱 클래스 활성화(프로젝트 전용)
            self.summary_timestamp_parse = Summary_Timestamp_Parse()

            # 요약 클래스 활성화
            self.summary = gpt_summary_method()

            #언디텍티드 드라이브 init
            self.driver = drive

            #로그인메서드 init
            self.logins = logins(self.driver)

            #로그인 전역 변수
            self.wj_ID = ID
            self.wj_PW = PW

            #DB video ID 전역변수
            self.registered_video_ids = None

            #초기 로그인
            self.logins.wj_login(self.wj_ID,self.wj_PW)
            sleep(2)


       except Exception as e:

            print(f'MainJob_Init_Error : {str(e)}')
            self.log.error(f'MainJob_Init_Error : {str(e)}')

       finally:
           
           sleep(1)
           print(f'MainJob_Init_Check')
           self.log.info(f'MainJob_Init_Check')
        
    def get_channel_id(self,url): #유튜브 채널 URL에서 ID부분만 추출하는 함수
        # 유튜브 채널 URL에서 'UC'로 시작하는 채널 ID를 추출하는 정규 표현식
        pattern = r'youtube\.com\/channel\/(UC[-_A-Za-z0-9]{21}[AQgw])'
        match = re.search(pattern, url)

        if match:
            # 정규 표현식에 해당하는 부분을 찾으면, 그 부분을 반환
            return match.group(1)
        else:
            # 채널 ID를 찾지 못하면 None 반환
            return None

    @cached(cache) # 이 데코레이터는 함수의 결과를 자동으로 캐시합니다.
    def get_video_links(self,api_key, channel_url): #채널 URL에 대한 영상 목록 가져오기
      try:
        #프로그램 배포시 build 매서드 안먹히는 버그 있음(static_discovery=False 옵션값으로 해결)
        youtube = build('youtube', 'v3', developerKey=api_key,static_discovery=False)
        channel_id = self.get_channel_id(channel_url)

        #유튜브 영상 (영상길이 videoDuration 4~20분사이,order 날짜기준 내림차순)
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=150, type='video',regionCode='KR',videoDuration='medium',order='date')
        response = request.execute()


        #뉴스 채널은 오늘 날짜만 뽑기(SBS뉴스채널).
        if channel_id == 'UCkinYTS9IHqOEwR1Sze2JTw':
            today_date = datetime.datetime.now().date()
            filtered_response_items = [
                item for item in response['items']
                if datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date() == today_date
            ]
            # Update the response variable with filtered data
            response = {'items': filtered_response_items}

        #로그 출력
        log_result = str(response['items'])
        self.log.info(f'get_video_links_list\n{log_result}')
        self.log.info(log_result)

        return response

      except Exception as e:
          
          self.log.error(f'get_video_links_Error : {str(e)}')
          return None

    def video_url_already_chek(self,video_id,registered_video_ids): #이미 등록되어 있는지 DB에서 확인
        
            # DB = Common_DB()
            # params = (author)
            # rows = DB.execute_read_query("select DISTINCT video_ID from youtube_video_reg_list where author = %s",params)
            # DB.close()

            for i in registered_video_ids:
                if i == video_id:
                    return  True
            
            return False

    def check_videos_already_registered(self, author):
        """
        데이터베이스에서 주어진 저자의 비디오 ID들 중 이미 등록된 것들을 조회합니다.
        
        :param author: 조회할 비디오의 저자
        :param video_ids: 조회할 비디오 ID들의 리스트
        :return: 이미 등록된 비디오 ID들의 리스트
        """
        # 데이터베이스 연결 생성
        DB = Common_DB()

        # 쿼리 실행
        query = f"SELECT DISTINCT video_ID FROM youtube_video_reg_list WHERE author = '{str(author)}'"
        rows = DB.execute_read_query(query)
        DB.close()

        # 조회된 결과에서 비디오 ID만 추출하여 리스트로 반환
        rows_list = [row[0] for row in rows]
        return rows_list




    def set_youtube_reg_cnt(self):#등록시 DB 총합 개수 누적
                #DB 지식인 답변 상태 카운트 하기
                DB = Common_DB()

                # 현재 날짜 및 시간 가져오기
                current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 기존 등록된 계정의 카운트 개수 확인
                row = DB.execute_read_query(f"SELECT * FROM youtube_answer_status WHERE WJ_ID = '{self.wj_ID}'")
                current_count = row[0][1]

                if current_count == '' or current_count == None:
                    DB.execute_query(f"UPDATE youtube_answer_status SET REG_CNT = 1, last_answer_regdate = '{current_date}' WHERE WJ_ID = '{self.wj_ID}'")
                    
                else:
                    current_count = int(current_count) + 1
                    DB.execute_query(f"UPDATE youtube_answer_status SET REG_CNT = {int(current_count)}, last_answer_regdate = '{current_date}' WHERE WJ_ID = '{self.wj_ID}'")
                    
            
                # 연결 종료
                DB.close()

    def video_total_cnt_ch(self):#통합DB 등록 개수 확인
    
            DB = Common_DB()

            row = DB.execute_read_query(f"SELECT * FROM youtube_maxcount_info")
            reg_count = int(row[0][0])#등록 가능한 카운트 개수 확인

            row = DB.execute_read_query(f"SELECT * FROM youtube_answer_status WHERE WJ_ID = '{self.wj_ID}'")
            current_count = row[0][1]

            # 연결 종료
            DB.close()

            #전체 개수를 넘는지 확인.
            if int(current_count) >= int(reg_count):
                return True
            else:
                return False

    def video_channel_cnt_ch(self,author):#현제 채널 금일 등록 개수 확인

        DB = Common_DB()
        row = DB.execute_read_query(f"select count(*) from youtube_video_reg_list where date(regdate) = curdate() and error is null and author = '{author}'")
        DB.close()

        today_channel_reg_count = int(row[0][0])#등록 가능한 카운트 개수 확인

        if today_channel_reg_count >= self.channel_max_count:
            return True
        else:
            return False
        

        

    def start(self): #통합 작업 동작

     try:
        # 키파일 열기
        with open('Youtube_key.txt', 'r') as file:
            # 파일에서 전체 내용 읽기
            youtube_key = file.read().strip()  # strip()을 사용하여 불필요한 공백이나 줄바꿈 문자 제거
        
        api_key = youtube_key #유튜브 API 키
        #channel_url = input("YouTube 채널 URL을 입력하세요: ")

        #txt파일 열어서 채널 url들 가공
        channel_urls = []
        with open('./Video_Url_list.txt', 'r', encoding='utf-8') as file:
               # JSON 데이터 로드
               data = json.load(file)
        for item in data:
            channel_urls.append(item['channel_url'])
        
        
        #채널 url 별로 요약하기
        for channel_url in channel_urls:

            #1.영상 목록 가져오기
            video_list = {}
            video_list = self.get_video_links(api_key, channel_url)

            #2.DB에 등록되어 있는 video_id 채널별 전체 리스트 가져오기(루프돌기전 한번만 DB실행)
            self.registered_video_ids =  self.check_videos_already_registered(video_list['items'][0]['snippet']['channelTitle'])
            print(str(self.registered_video_ids))

            #3.영상 요약하기
            self.count = 0
            for item in video_list['items']:
            
                # 영상 목록 변수화
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_link = f'https://www.youtube.com/watch?v={video_id}'
                description = item['snippet']['description']
                author = item['snippet']['channelTitle']
                thumbnail = item['snippet']['thumbnails']['high']

                #채널당 금일 등록수가 maxcount(5개) 이상이면 건너띄기
                video_channel_cnt_ch = self.video_channel_cnt_ch(str(author))
                if video_channel_cnt_ch == True:
                    self.log.info(f'Today_This_Channel_MaxCount_Over(skip) : {str(author)}')
                    break


                #이미 등록되어 있는지 가져온 리스트(self.registered_video_ids) 에서 확인
                data_checking = self.video_url_already_chek(video_id,self.registered_video_ids)
                if data_checking == True:
                    self.log.info(f'This_video_already : {str(video_title)}')    
                    continue
                
                
                #실행중 최대 개수 도달 했는지 체크 하기
                total_cntch = self.video_total_cnt_ch()
                if total_cntch == True:
                    self.log.info(f'등록중 허용치를 초과 하여 스킵 됩니다')    
                    return 'Max_reg_count'
                
                #요약 실행
                summary_result = '-'
                summary_result = self.summary.start(video_id, video_title, description, author)

                #요약 에러 발생시 넘기기
                if 'error' in str(summary_result['content']).lower():
                    self.log.info(f'This_video_summary_error : {str(video_title)}')    
                    continue    

                #요약본 우정 양식에 맞게 가공(제목 + 영상(임배디드,iframe) + 요약본(테이블) + 출처 GPT요약글 및 링크)(변경)
                chosen_title = video_title + '[이미지 포함]' if summary_result['caption_check'] else video_title #캡션 여부에 따라 추가 제목 '[이미지 포함]' 포함.
                wj_summary_content = f'''<h1><span style="font-size: 26px;">{str(chosen_title)}</span></h1> <br> <iframe width="912" height="514" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>''' +  summary_result['content'] + f'''<br> <span style="color: rgb(204, 204, 204);">▶ 위 내용은 GPT를 통해 요약되었습니다.</span> <br> <span style="color: rgb(204, 204, 204);">▶ 출처 URL : {str(video_link)}</span>'''            
                
                video_summary_result = {"title": chosen_title,"thumbnail_link": thumbnail,"link": video_link,"video_id" : video_id,"description" : description,"author" : author,"video_summary" : wj_summary_content, "caption_check" : summary_result['caption_check']}
                self.log.info(f'video_summary_result')
                self.log.info(video_summary_result)

                
                #캡션이 True 인경우만 실행
                if video_summary_result['caption_check'] == True:
                    
                    #타임스탬프 링크 video_summary_result 딕셔너리에 리스트로 추가됨
                    video_summary_result = self.summary_timestamp_parse.parse_text_info(video_summary_result)
                    if isinstance(video_summary_result, str):#에러 발생시 Json 남기고 넘기기
                        if 'error' in str(video_summary_result).lower(): 
                            continue    

                    #요약본 영상 스크린샷 저장(셀레니움 태그 스크린샷 사용 및 video_summary_result 딕셔너리에 경로 추가)
                    self.youtube_Timestamp_Screenshot = Youtube_Timestamp_Screenshot(self.driver)
                    video_summary_result = self.youtube_Timestamp_Screenshot.get_screenshot(video_summary_result)
                    if isinstance(video_summary_result, str):#에러 발생시 Json남기고 넘기기
                        if 'error' in str(video_summary_result).lower(): 
                            continue    


                #우정에 등록하기(셀레니움 이용,사진 추가 기능)
                wj_Cafe_Method = Wj_Cafe_Method(self.driver)
                wj_result = wj_Cafe_Method.wj_webpage_reg_method(video_summary_result)


                #DB등록
                wj_url = wj_result['wj_url']
                current_date_time = datetime.datetime.now()
                DB = Common_DB()
                #기존 쿼리식 사용시에 (특수문자 걸러내지 못함)
                #DB.execute_query(f"INSERT INTO youtube_video_reg_list (video_id, video_title, video_url,author,regdate,wj_url) VALUES ('{video_id}', '{video_title}','{video_link}','{str(author)}','{str(current_date_time)}','{wj_url}')")
                params = (video_id, video_title,video_link,author,str(current_date_time),wj_url)
                DB.execute_query("INSERT INTO youtube_video_reg_list (video_id, video_title, video_url,author,regdate,wj_url) VALUES (%s,%s,%s,%s,%s,%s)",params)
                DB.close()

                self.set_youtube_reg_cnt()#DB(전체) 카운트 누적
                self.count += 1 #for문(현제) 카운트 누적

                
        
            #통합 작업 완료 로그
            self.log.info(f'This_channel_video_reg_complete')

     except Exception as e:
          
        #통합 작업 에러 로그
        self.log.info(f'This_channel_video_reg_error : {str(e)}')




