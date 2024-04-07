
from time import sleep
from selenium.webdriver.common.by import By
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import pyautogui
from Method.Utility.Detection_Driver import make_user_agent
import autoit
import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log



# 우정 및 카페 등록 메서드
class Wj_Cafe_Method:

    def __init__(self,driver):  #init

        try:
            self.driver = driver
        except Exception as e:
            print(f'logins_init_error : {str(e)}')

        #로그 init
        log = Log()
        self.log = log.activate() 

    def wj_webpage_reg_method(self,video_summary_result): #웹페이지 등록 메서드(핫영상요약)
        
        try:
            # 사용할 변수 셋팅
            video_title = video_summary_result['title']
            video_summary = video_summary_result['video_summary']

            # 액션 체인 활성화
            action = ActionChains(self.driver)

            # 임시로 user-agent 및 해상도 바꾸기
            try:
               #기존 크롬 사이즈 추출(뷰포트)
                before_width = self.driver.execute_script("return window.innerWidth;")
                before_height = self.driver.execute_script("return window.innerHeight;")
                print(f"Viewport size: {before_width}x{before_height}")    

                self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                    "width":1920,
                    "height":1080,
                    "deviceScaleFactor" : 1,
                    "mobile": True
                })

                before_user_agent = self.driver.execute_script("return navigator.userAgent;")
                print(f'before_UA : {before_user_agent}')
                self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'})   
            except Exception as e:
                self.log.error(f'우정_유저에이전트 변경 에러, 타이틀 : {str(video_title)}, {str(e)}')
                

            try:
                sleep(0.7)
                self.driver.get('https://www.woowarhanclean.com/woowarhannews/?category=Q007HE244E')
                sleep(0.7)
                if EC.alert_is_present()(self.driver):
                    alert = self.driver.switch_to.alert
                    alert.accept()

                sleep(0.7)
                self.driver.get('https://www.woowarhanclean.com/woowarhannews/?category=Q007HE244E')
                sleep(0.7)
                if EC.alert_is_present()(self.driver):
                    alert = self.driver.switch_to.alert
                    alert.accept()
            except Exception as e:
                self.log.error(f'우정_등록 에러, 영상제목 : {str(video_title)}, {str(e)}')
                

            # 자바스크립트를 사용하여 채널톡 팝업요소 일시적 삭제
            sleep(1)
            try:
                self.driver.execute_script("""
                    var element = document.getElementById('ch-plugin');
                    if (element) {
                        element.parentNode.removeChild(element);
                    }
                    """)
            except Exception as e:
                
                self.log.error(f'채널톡 팝업 찾을 수 없음 (skip)')


            sleep(1)
            try:
                button = self.driver.find_element(By.XPATH,"//a[contains(text(), '글쓰기')]")#글쓰기 버튼
                action.move_to_element(button).click().perform() #웹상 클릭
            except Exception as e:
                self.log.error(f'우정_글쓰기 버튼 에러, 타이틀 : {str(video_title)}, {str(e)}')
                
            # 자바스크립트를 사용하여 채널톡 팝업요소 일시적 삭제
            sleep(1)
            try:
                self.driver.execute_script("""
                    var element = document.getElementById('ch-plugin');
                    if (element) {
                        element.parentNode.removeChild(element);
                    }
                    """)
            except Exception as e:
                
                self.log.error(f'채널톡 팝업 찾을 수 없음(skip), 타이틀 : {str(video_title)}, {str(e)}')
                

            sleep(0.7)
            category = self.driver.find_element(By.XPATH,"//div[@class='div_select category_select']")#카테고리부분
            action.move_to_element(category).click().perform()

            sleep(0.7)
            category_1 = self.driver.find_element(By.XPATH,"//span[contains(text(), '핫 영상 AI요약')]")#카테고리부분_1
            action.move_to_element(category_1).click().perform()

            sleep(0.7)
            title_area = self.driver.find_element(By.XPATH,'//*[@id="post_subject"]')#제목부분
            action.move_to_element(title_area).click().perform()
            
            sleep(0.7)
            action.send_keys(Keys.HOME).perform()
            pyperclip.copy(video_title)
            title_area.send_keys(Keys.CONTROL, 'v')
            
            sleep(0.7)
            code_btn = self.driver.find_element(By.XPATH,'//*[@id="html-1"]')#코드 버튼
            code_btn.click()

            sleep(0.7)
            body_code = self.driver.find_element(By.XPATH,'//*[@id="post_body"]/div[1]/div[2]/div[6]/div[1]/div/div/div/div[5]/div[1]/pre')#본문코드 부분
    
            sleep(0.7)
            pyperclip.copy(video_summary) #video요약본(html코드)
            action.move_to_element(body_code).click().perform()
            action.key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).pause(0.2).perform()

            sleep(0.7)
            code_btn.click()#코드 버튼

            #캡션(자막 시간)있는 경우 이미지 넣기(테스트중..)
            if video_summary_result['caption_check'] == True:
                
                for i in video_summary_result['video_screenshot_paths']:
                
                    # 파일 경로에서 숫자를 추출합니다.
                    file_path = str(i['video_screenshot_path'])
                    file_number = int(re.search(r"/(\d+)\.png$", file_path).group(1))

                    # 스크린샷 태그
                    sleep(0.7)
                    screenshots_area = self.driver.find_element(By.XPATH,f"//td[contains(text(), '{str(file_number)}초-캡쳐이미지')]")#스크린샷 첨부 부분
                    action.move_to_element(screenshots_area).click().perform() #웹상 클릭

                    # 해당 요소까지 스크롤하기
                    sleep(0.7)
                    self.driver.execute_script("arguments[0].scrollIntoView();", screenshots_area)
                    action.move_to_element(screenshots_area).click().perform() #웹상 클릭

                    # 스크린샷 텍스트 부분 블록잡기(모두)
                    sleep(0.7)
                    action.send_keys(Keys.HOME).pause(0.2).perform()
                    action.key_down(Keys.SHIFT).send_keys(Keys.END).key_up(Keys.SHIFT).pause(0.2).perform()

                    # 사진 버튼 클릭 후 이미지 등록하기
                    sleep(0.7)
                    img_btn = self.driver.find_element(By.XPATH,'//*[@id="insertCustomImage-1"]')#이미지 첨부 버튼
                    img_btn.click()

                    pyperclip.copy(str(file_path))
                    sleep(0.7)
                    pyautogui.hotkey("ctrl", "v") 
                    sleep(0.7)
                    pyautogui.press('enter')
                    sleep(3)


            sleep(1)
            reg_btn = self.driver.find_element(By.XPATH,'//*[@id="board_container"]/div[1]/div/div[2]/button')#등록버튼
            action.move_to_element(reg_btn).click().perform() #웹상 클릭
            
            sleep(1)
            current_url = self.driver.current_url # 등록후 현재 페이지의 URL 가져오기
            
            #useragent 및 해상도원복하기
            UA_DATA = make_user_agent(before_user_agent,True)
            self.driver.execute_cdp_cmd("Network.setUserAgentOverride",UA_DATA)   

            sleep(1)
            self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":int(before_width),
                "height":int(before_height),
                "deviceScaleFactor" : 1,
                "mobile": True
            })

            sleep(1)
            
            video_summary_result['wj_url'] = current_url
            self.log.info(f'우정 등록 완료  : {str(video_title)}, Result : {str(video_summary_result)}')
            return video_summary_result


        except Exception as e:
            
            self.log.error(f'우정 등록중 에러, 타이틀 : {str(video_title)}, {str(e)}')
            self.driver.save_screenshot('./error_screenshots/wj_reg_error.png')

            video_summary_result['wj_url'] = str(e)
            return video_summary_result



    def ncafe_webpage_reg_method(self,wj_url,newtitle,imagepath): #웹페이지 등록 메서드(네이버카페)
        try:
            
            action = ActionChains(self.driver)

            #기존 크롬 사이즈 추출(뷰포트)
            before_width = self.driver.execute_script("return window.innerWidth;")
            before_height = self.driver.execute_script("return window.innerHeight;")
            print(f"Viewport size: {before_width}x{before_height}")            

            sleep(1)
            self.driver.get(wj_url)
        
            sleep(1)
            self.driver.find_element(By.XPATH,'//*[@class="mobile_right dropdown"]').click()#수정 토글 버튼
            sleep(1)
            self.driver.find_element(By.XPATH,"//a[text()='수정']").click()#수정 버튼

            # 자바스크립트를 사용하여 채널톡 팝업요소 일시적 삭제
            sleep(1)
            try:
                self.driver.execute_script("""
                    var element = document.getElementById('ch-plugin');
                    if (element) {
                        element.parentNode.removeChild(element);
                    }
                    """)
            except Exception as e:
                print(f'채널톡 팝업 찾을 수 없음 (넘김)')

            sleep(1)
            body_code = self.driver.find_element(By.XPATH,"//div[@class='board-name' and text()='자주 묻는 질문 FAQ']")#본문코드 (자주 묻는 질문 FAQ) 부분으로 클릭
            
            action.move_to_element(body_code).click().perform() #웹상 클릭
            #action.move_to_element(body_code).context_click().perform() #웹상 클릭 위치 확인

            #크롬 사이즈 늘리기 (표복사 버그로 실행 필요.)
            self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":1920,
                "height":1080,
                "deviceScaleFactor" : 1,
                "mobile": True
            })

            sleep(1)
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            sleep(0.5)
            action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
            
        
            #크롬 사이즈 모바일용으로 원복
            sleep(0.5)
            self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":int(before_width),
                "height":int(before_height),
                "deviceScaleFactor" : 1,
                "mobile": True
            })

            sleep(3)             
            self.driver.get('https://m.cafe.naver.com/ca-fe/web/cafes/13598135/articles/write') #네이버 카페 (지식 답변 QnA)

            #카테고리 지식인으로 바꾸기
            category = self.driver.find_element(By.XPATH, '//*[@class="selectbox"]') #카테고리 버튼 선택
            action.move_to_element(category).click().perform() #웹상 클릭

            sleep(0.5)

            option = self.driver.find_element(By.XPATH, '//*[@id="menu_16"]') #카테고리 -> 지식인 버튼 선택
            action.move_to_element(option).click().perform() #웹상 클릭

            sleep(0.5)
            textarea = self.driver.find_element(By.XPATH, '//textarea[@type="text" and @placeholder="제목"]') #카페 제목 부분
            
            textarea.send_keys(str(newtitle))

            # 클래스 이름이 'se-content'인 div 태그 찾기(본문)
            div_element = self.driver.find_element(By.CLASS_NAME, "se-content")
            action.move_to_element(div_element).click().perform() #웹상 클릭
            
            sleep(0.5)
            for _ in range(7): 
                action.send_keys(Keys.ARROW_UP).pause(0.2).perform()

            
            sleep(0.5)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
     

            # ===== 붙여넣으면서 불필요한 내용 가공 하기 START =====
            
            #내용 잘 불러와졌는지 체크(이미지로 명시적 대기)
            try:
                
                element = WebDriverWait(self.driver, 20).until(
                   EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'se-image-resource')]"))
                )
            except Exception as e:

                #self.logger.error(f'카페_내용붙여넣기_에러, 타이틀 : {str(newtitle)}, {str(e)}')
                self.driver.save_screenshot('./screenshots/cafe_paste_reg_error.png')
            
            #확실하게 위치 선정하기 Q.제목, Q. 부분 조회하여 클릭
            sleep(1)
            div_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Q.')]")
            action.move_to_element(div_element).click().perform() #웹상 클릭

            
            
            #붙여넣은 사진 지우기, 본문 내용 맨 위쪽으로 이동하기 
            try:
                action.send_keys(Keys.HOME).pause(0.2).perform()
                
                for _ in range(22): 
                    action.key_down(Keys.SHIFT).send_keys(Keys.ARROW_UP).pause(0.2).perform()

            except Exception as e:
                
                #self.logger.error(f'카페 위 화살표 에러, 타이틀 : {str(newtitle)}, {str(e)}')
                self.driver.save_screenshot('./screenshots/cafe_arrow_up_error.png')
                
            finally:
                
                action.key_up(Keys.SHIFT).pause(0.2).perform()
                sleep(0.5)
          

            #기존 사진 구역까지 블록 잡은후 쓸때없는 내용 지우기
            for _ in range(3): 
                action.send_keys(Keys.ARROW_UP).pause(0.2).perform()
            
            sleep(0.5)
            action.key_down(Keys.SHIFT).perform()
            for _ in range(12):
                action.send_keys(Keys.ARROW_DOWN).pause(0.2).perform()
                
            sleep(1)
            #pyautogui.press('delete')
            for _ in range(2):
                #pyautogui.press('backspace')
                action.send_keys(Keys.BACKSPACE).pause(0.2).perform()

            sleep(0.5)
            action.send_keys(Keys.HOME).pause(0.2).perform()
            action.key_up(Keys.SHIFT).perform()

            
            #사진 버튼 누르기
            sleep(1)
            picture = self.driver.find_element(By.XPATH, '//*[@class="se-image-toolbar-button se-document-toolbar-basic-button __se-sentry"]') #네이버 카페 사진버튼
            picture.click()

            #사진 경로 로컬로 수정후 재등록하기
            sleep(0.5)
            img_set1 = str(imagepath).replace('/','\\')
            print(img_set1)
            img_set2 = str(img_set1).replace('https:\\\\elbserver.store\\static\\woowarhanclean_img\\AI_Image\\','C:\\AI_IMAGE_FAQ\\')
            print(img_set2)

            img_path= img_set2
            print(img_path)
            
            
            #Basic Window info 값 handle 변수에 저장 #32770 다이얼로그 기본 값
            handle = "[CLASS:#32770; TITLE:열기]"

            #이름이 '열기'인 창이 나올 때까지 3초간 대기
            autoit.win_wait_active("열기", 3)
            
            #사진 클릭시 나오는 윈도우 창에서 파일이름(N)에 이미지 경로값 전달
            autoit.clip_put(img_path)  # 경로를 클립보드에 복사
            autoit.control_focus(handle, "Edit1")  # Edit 컨트롤에 포커스
            sleep(1)
            autoit.send("^v")  # 붙여넣기

            #사진 클릭시 나오는 윈도우 창에서 Button1 클릭
            sleep(0.5)
            autoit.control_click(handle, "Button1")
            
        
            #관련 링크 적용(사진 나오는지 잠시텀 주기,명시적대기)
            try:    
                
                element = WebDriverWait(self.driver, 20).until(
                   EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'se-image-resource')]"))
                )

            except Exception as e:
                #self.logger.error(f'카페_사진등록_에러, 타이틀 : {str(newtitle)}, {str(e)}')
                self.driver.save_screenshot('./screenshots/cafe_picture_reg_error.png')

            sleep(1)
            match = re.search(r'idx=(\d+)', wj_url)
            if match:
                idx_value = match.group(1)
                print(idx_value)
            else:
                print("idx 값을 찾을 수 없습니다.")
                return f"Error : NotFound Idx"
            
            pyperclip.copy('blank')
            pyperclip.copy(f"https://www.woowarhanclean.com/junktip/?idx={str(idx_value)}&bmode=view")
            
            # 텍스트가 "관련글"인 span 태그 찾기
            related_article_span = self.driver.find_element(By.XPATH, "//span[contains(text(), '관련글 : ')]")
            
            action.move_to_element(related_article_span).click().perform()
            action.send_keys(Keys.END).perform()
        
            sleep(1)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            
            element = WebDriverWait(self.driver, 20).until( #링크 썸네일이 표시 되었는지 최대 20초 동안 대기
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'se-module') and contains(@class, 'se-module-oglink') and contains(@class, '__se-unit')]"))
                    )

            reg_btn = self.driver.find_element(By.XPATH, '//a[@class="GnbBntRight__green" and @role="button"]')#등록버튼
            action.move_to_element(reg_btn).click().perform()
          
            
            sleep(2)
            current_url = self.driver.current_url # 등록후 현재 페이지의 URL 가져오기
            
            return current_url

            
        except Exception as e:
            
            print(f'cafe_reg_error : {str(e)}')
            #self.logger.error(f'카페_등록 에러, 타이틀 : {str(newtitle)}, {str(e)}')
            self.driver.save_screenshot('./screenshots/cafe_reg_error.png')
            
            replace_e = str(e).replace("\'","")
            return f'Error : {replace_e}'
            