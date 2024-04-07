import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../')
sys.path.append(utility_path)
from Method.Utility.Auto_job_Log import Auto_job_Log
import datetime
import random
import pymysql
from time import sleep
from Method.Commom_DB.DB import Common_DB
from Method.Utility.Detection_Driver import make_driver
from Method.Integrated_code.Integrated_code import Integrated_code

class Auto_Main_job:
        
        def __init__(self,WJ_ID,WJ_PW):  #init
            
            #로그 init
            log = Auto_job_Log()
            self.log = log.activate()

            #언디텍티드 드라이브 init
            self.driver = make_driver()

            #계정 정보
            self.WJ_ID = WJ_ID
            self.WJ_PW = WJ_PW

            #통합코드 클래스 활성화
            self.integrated_code = Integrated_code(self.driver,self.WJ_ID,self.WJ_PW)

            #DB시간 테이블 정보 가져오기
            DB = Common_DB()
            row = DB.execute_read_query(f"SELECT * FROM youtube_time_seting_info")
            DB.close()

            self.start_time_1 = int(row[0][0])
            self.start_time_2 = int(row[0][1])
            self.end_time_1 = int(row[0][2])
            self.end_time_2 = int(row[0][3])

            #자동화 기본 변수 셋팅
            self.start_autojob_time =  datetime.time(random.randint(self.start_time_1,self.start_time_2), 0)  # 매일 오전 8시
            self.end_autojob_time = datetime.time(random.randint(self.end_time_1,self.end_time_2), 0)  # 매일 오전 9시
            self.random_target_weekday = random.randint(0, 5) #월~토 랜덤하게
            self.autojob_check = True #오토잡 체크(기본True)
            self.midnight_check = True #자정 체크(기본True)
            self.chalarm = False #스킵일 알람체크(기본False)
            self.today = datetime.date.today()#금일날짜
            self.next_week_start = self.today + datetime.timedelta(days=(6 - self.today.weekday()) + 1) # 다음 주의 시작 날짜 구하기 (월요일을 기준으로 함)


        def get_account_check(self,id):#계정 체크 및 DB 등록

                # 현재 날짜 및 시간 가져오기
                current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                #기존 등록된 ID가 있는지 확인후 있으면 등급 업데이트
                DB = Common_DB()

                # 기존 등록된 ID 확인
                rows = DB.execute_read_query(f"SELECT * FROM youtube_answer_status WHERE WJ_ID = '{self.WJ_ID}'")
                
                if len(rows) != 0:
                    DB.execute_query(f"UPDATE youtube_answer_status SET last_connect_regdate = '{current_date}' WHERE WJ_ID = '{self.WJ_ID}'")
                    self.log.info(f"우정계정 {self.WJ_ID} 계정이 이미 DB에 있습니다. 접속일 업데이트 합니다. : {str(current_date)}")
                else:
                    # 기존 등록된 ID가 없으면 새로운 ID와 등급 삽입
                    DB.execute_query(f"INSERT INTO youtube_answer_status (WJ_ID, REG_CNT, last_connect_regdate) VALUES ('{self.WJ_ID}', '0','{current_date}')")
                    self.log.info(f"우정계정 {self.WJ_ID}가 신규로 등록되었습니다.")

                # 연결 종료
                DB.close()

        def get_weekday_name(self,weekday): #요일 이름 반환 함수
            weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            return weekday_names[weekday]

        def set_youtube_answer_cnt_ch(self):#등록시 등록 카운트 체크 함수
            #DB 지식인 답변 상태 카운트 하기
            DB = Common_DB()

            # 현재 날짜 및 시간 가져오기
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            

            # 기존 등록된 계정의 카운트 개수 확인
            row = DB.execute_read_query(f"SELECT * FROM youtube_answer_status WHERE WJ_ID = '{self.WJ_ID}'")
            self.current_count = row[0][1]

            #현제(일)이 해당 계정 마지막 답변 등록(일)보다 크면 카운트 초기화 및 마지막답변날짜 업데이트
            set_last_answer_regdate = row[0][2]
            if set_last_answer_regdate != None: #첫등록된 계정은 None상태이므로 None이 아닌경우에만 실행..
                last_answer_regdate = set_last_answer_regdate.strftime('%Y-%m-%d')
                if current_date > last_answer_regdate :
                    
                    self.current_count = '0' #변수 초기화
                    DB.execute_query(f"UPDATE youtube_answer_status SET REG_CNT = '0', last_answer_regdate = '{current_date}' WHERE WJ_ID = '{self.WJ_ID}'")
                    
                    
            #등록 가능한 카운트 개수 확인
            row = DB.execute_read_query(f"SELECT * FROM youtube_maxcount_info")
            
            #(등록 가능 개수)
            self.reg_count = int(row[0][0])

            # 연결 종료
            DB.close()

            #등급 개수를 넘는지 확인.
            if int(self.current_count) >= int(self.reg_count):
                return False #현제 계정 개수가 등급개수를 넘는경우
            else:
                return True    



        def start(self):
           
          while True: #무한루프  
            
            sleep(30)
            
            try:
                #계정 체크 및 등록
                self.get_account_check(self.WJ_ID)

                now = datetime.datetime.now() # 현재 시간을 가져옵니다.
                self.current_weekday = now.weekday()  # 월요일부터 일요일까지 0부터 6까지의 값을 가집니다.                         
                self.today = datetime.date.today() # 현제 날짜

                # 1.매일 자정 걸릴때(한번만) 시작 시간과 종료 시간을 재정의합니다.
                if now.hour == 0 and self.midnight_check == True:                

                    self.log.info(f'[자정체크] - 자정이 되어 등록개수 초기화 합니다.')    

                    #DB시간 테이블 정보 가져오기
                    DB = Common_DB()
                    row = DB.execute_read_query(f"SELECT * FROM youtube_time_seting_info")
                    DB.close()

                    self.start_time_1 = int(row[0][0])
                    self.start_time_2 = int(row[0][1])
                    self.end_time_1 = int(row[0][2])
                    self.end_time_2 = int(row[0][3])

                    #시간 범위 다시 랜덤으로 조정
                    self.start_autojob_time = datetime.time(random.randint(self.start_time_1,self.start_time_2), 0)  # 매일 오전 8시
                    self.end_autojob_time = datetime.time(random.randint(self.end_time_1,self.end_time_2), 0)  # 매일 오전 9시

                    self.midnight_check = False


                # 2.요일에 대해 동작 및 스킵 여부 셋팅 합니다.
                if self.current_weekday in [6]:#주말은(일) 자동화 스킵    
                    self.log.info(f'주말({self.get_weekday_name(self.current_weekday)})이므로 자동화 스킵 됩니다.\n(*스킵되는 세션 종료 됩니다.)')    
                    
                    try:
                        
                        if self.autojob_check == True:
                            self.driver.quit()
                            self.autojob_check = False 
                    except Exception as e:
                        self.log.error(f'주말 스킵진행시 에러발생 :  {str(e)}')    
                    continue 
                    

                if self.today >= self.next_week_start: #다음주(월요일)마다 실행될 코드,self.today변수는 init시에 실행후 고정.
                        
                        self.next_week_start = self.today + datetime.timedelta(days=(6 - self.today.weekday()) + 1) # 다음 주의 시작 날짜 구하기 (월요일을 기준으로 함) 
                        self.random_target_weekday = random.randint(0, 5)#월~토 랜덤하게
                        self.log.info(f'프로그램 실행후 한주가 지나 스킵요일을 재설정 합니다. {self.get_weekday_name(self.random_target_weekday)}') 

                if self.current_weekday == self.random_target_weekday: # 0부터 4까지의 값으로 월요일부터 토요일까지 선택
                   self.log.info(f'이번주 해당 요일({self.get_weekday_name(self.random_target_weekday)})은 자동화 스킵 됩니다.\n(*스킵되는 동안 계정 로그아웃 및 세션 종료 됩니다.)') 
                   try:
                        
                        if self.autojob_check == True:          
                            self.driver.quit()
                            self.autojob_check = False 
                   except Exception as e:
                     self.log.error(f'해당요일 스킵진행시 에러발생 :  {str(e)}')    
                   continue 

                #3.답변 등록시 해당 계정 등급 개수와 답변 개수 카운트 체크
                answer_gradecnt_ch = self.set_youtube_answer_cnt_ch()
                if answer_gradecnt_ch == False:
                    self.log.info(f'현제 등록 허용치를 초과 하여 스킵됩니다, 하루 지난후 초기화 됩니다.\n 현제등록개수 : {self.current_count}, 가능개수 : {int(self.reg_count)}\n(*스킵되는 동안 세션 종료 됩니다.)')

                    try:
                        if self.autojob_check == True:
                            self.driver.quit()
                            self.autojob_check = False 
                    except Exception as e:
                        self.log.error(f'스킵진행시 에러발생 :  {str(e)}')
                    continue

                
                # 4.현재 시간이 [시작 시간과 종료 시간 사이]에 있는지 확인합니다. 순서상 마지막 체크!!
                if self.start_autojob_time <= now.time() <= self.end_autojob_time:

                    self.log.info(str(f'자동화 시간({str(self.start_autojob_time)}~{str(self.end_autojob_time)})입니다.'))    

                    #스킵일 알림체크 False로 초기화
                    self.chalarm = False 

                    #self.autojob_check(플래그) False이면 드라이버 실행 및 통합코드 재활성화 하기
                    if self.autojob_check == False:
                        self.driver = make_driver()    
                        
                        #통합코드 재활성화
                        self.integrated_code = Integrated_code(self.driver,self.WJ_ID,self.WJ_PW)
                        self.autojob_check = True  

                    
                    #통합코드 실행
                    self.integrated_code.start()
                    
            
                else:

                    self.log.info(f'자동화 시간({str(self.start_autojob_time)}~{str(self.end_autojob_time)})이 아니라 작업 스킵 됩니다.\n(*스킵되는 동안 세션 종료 됩니다.)')
                    
                    #셀레니움 종료
                    if self.autojob_check == True:
            
                        self.driver.quit()
                        self.autojob_check = False #오토잡 체크(플래그)
                        self.midnight_check = True #자정체크


            except Exception as e:

                 self.log.info(f'자동화 진행시 에러 발생 : {str(e)}')


if __name__ == "__main__":

    # 계정 파일 열기
    with open('WJ_Account.txt', 'r') as file:
        # 파일에서 첫 번째 줄 읽기
        line = file.readline().strip()  # strip()을 사용하여 줄바꿈 문자 제거    
        # 쉼표로 구분하여 ID와 PW 추출
        ID, PW = line.split(',')
   
    auto_Main_job = Auto_Main_job(ID,PW)
    auto_Main_job.start()



