import re
import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log
from Method.Commom_DB.DB import Common_DB
import datetime
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Youtube_Timestamp_Screenshot:
        
        def __init__(self,driver):  #init
            
           #로그 init
           log = Log()
           self.log = log.activate() 

           try:
                self.driver = driver
           except Exception as e:
                
                self.log.info(f'Youtube_Timestamp_Screenshot_init_error : {str(e)}')
                #print(f'logins_init_error : {str(e)}')
            

        def error_db_reg(self,video_id,video_title,author,error): #에러시 DB 기록
            DB = Common_DB()
            
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            current_date_time = datetime.datetime.now()

            params = (video_id, video_title,video_url,author,str(current_date_time),'-',error)
            DB.execute_query("INSERT INTO youtube_video_reg_list (video_id, video_title, video_url,author,regdate,wj_url,error) VALUES (%s,%s,%s,%s,%s,%s,%s)",params)
            DB.close()


        
        def get_screenshot(self, video_summary_result):
            
            try:

                #기존 크롬 사이즈 추출(뷰포트)
                before_width = self.driver.execute_script("return window.innerWidth;")
                before_height = self.driver.execute_script("return window.innerHeight;")
                print(f"Viewport size: {before_width}x{before_height}")    

                #유튜브 사이즈로 인하여 잠시 조절
                self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                    "width":360,
                    "height":640,
                    "deviceScaleFactor" : 1,
                    "mobile": True
                })


                # 현재 프로젝트의 절대 경로를 기준으로 디렉터리 경로 생성
                current_project_path = os.getcwd()
                summary_timestamp_link = video_summary_result['summary_timestamp_links']
                video_id = video_summary_result['video_id']
                

                video_screenshot_path = []
                for link in summary_timestamp_link:

                    url = link['timestamp_link']
                    self.driver.get(url)

                    # 최대 10초간 명시적 대기(영상 떳는지 확인)
                    element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//video[@class='video-stream html5-main-video']")))

                    # 탭하여 음소거 클릭하여 없애기
                    tab_mute_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ytp-unmute-icon')]")))
                    tab_mute_btn.click()
                    
                    # 정규 표현식을 사용하여 't=' 뒤의 숫자 추출
                    match = re.search(r"t=(\d+)", url)
                    time_value = match.group(1)

                    # 저장할 디렉터리 경로 설정
                    directory = os.path.join(current_project_path, f'Youtube_screenshots/{video_id}')
        
                    # 디렉터리가 존재하지 않으면 생성
                    if not os.path.exists(directory):
                        os.makedirs(directory)
        
                    # 스크린샷 저장 경로 설정
                    screenshot_path = os.path.join(directory, f'{time_value}.png')

                    # 스크린샷 저장(너무 빨리 찍혀서 검은 화면 나오는 경우가 있음)
                    sleep(0.4)
                    element.screenshot(screenshot_path)

                    #video_summary_result 경로 추가 저장
                    video_screenshot_path.append({'video_screenshot_path': 'file://' + str(screenshot_path).replace('\\','/')})
                

                video_summary_result['video_screenshot_paths'] = video_screenshot_path
                self.log.info(f'Video_screenshot_paths_successful : {str(video_summary_result)}')
                

                #해상도원복하기
                sleep(1)
                self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                    "width":int(before_width),
                    "height":int(before_height),
                    "deviceScaleFactor" : 1,
                    "mobile": True
                })


                return video_summary_result 

            except Exception as e:
                
                self.log.error(f'Youtube_Timestamp_Screenshot_Error : {str(e)}')
                self.error_db_reg(video_summary_result['video_id'],video_summary_result['title'],video_summary_result['author'],str(e)) #에러 발생시 DB 기록
                return f'Youtube_Timestamp_Screenshot_Error : {str(e)}'


        