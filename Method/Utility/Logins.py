from time import sleep
import pyperclip
from selenium.webdriver.common.keys import Keys
from Method.Utility.Random_clicks import Random_clicks
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class logins:
    
    #각 플랫폼 로그인 매서드(우정,네이버,아하,알통(예정..))

    def __init__(self,driver): 
       
        try:
            self.driver = driver
        except Exception as e:
            print(f'logins_init_error : {str(e)}')

        try:
            self.random_clicks = Random_clicks(self.driver)
        except Exception as e:
            print(f'random_clicks_init_error : {str(e)}')


    def wj_login(self,id,pw):
        
        try:
            self.driver.get('https://www.woowarhanclean.com/login?back_url=Lw%3D%3D&used_login_btn=Y')
            
            #ID
            sleep(1)
            ID = self.driver.find_element(By.XPATH,'//*[@id="w20200801c2bdc5238d65c"]/div/div/form/div[1]/div[1]/input')
            ID.click()
            pyperclip.copy(id)
            ID.send_keys(Keys.CONTROL, 'v')
            
            #PW
            sleep(1)
            PW = self.driver.find_element(By.XPATH,'//*[@id="w20200801c2bdc5238d65c"]/div/div/form/div[1]/div[2]/input')
            PW.click()
            pyperclip.copy(pw)
            PW.send_keys(Keys.CONTROL, 'v')
            
            #로그인 버튼
            pyperclip.copy('blank')
            self.driver.find_element(By.XPATH,'//*[@id="w20200801c2bdc5238d65c"]/div/div/form/p/button').click()
            sleep(1)


        except Exception as e:
            
            print(f'login_error : {str(e)}')
    

    def naver_login(self,id,pw):
        
        #네이버 로그인 URL
        self.driver.get('https://nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/aside/')
        self.driver.implicitly_wait(2) 

        try: 
            #ID
            ID = self.driver.find_element(By.CSS_SELECTOR,'#id')
            sleep(0.5)
            self.random_clicks.random_click('#id',"CSS_SELECTOR")
            pyperclip.copy(id)
            ID.send_keys(Keys.CONTROL, 'v')

            #PW
            sleep(0.5)
            PW = self.driver.find_element(By.CSS_SELECTOR,'#pw')
            self.random_clicks.random_click('#pw',"CSS_SELECTOR")
            pyperclip.copy(pw)
            PW.send_keys(Keys.CONTROL, 'v')
            
            #로그인 버튼
            sleep(0.5)
            pyperclip.copy('blank')
            #self.random_clicks.random_click("//button[@id='log.login']",'XPATH')
            self.random_clicks.random_click('//*[@id="upper_login_btn"]','XPATH')
            
        
        
            #팝업 화면이 나왔을때 닫기.
            sleep(0.5)
            if self.driver.find_elements(By.XPATH,"//button[text()='확인']"):
                    sleep(1)
                    self.random_clicks.random_click("//button[text()='확인']","XPATH")   

            sleep(0.5)

        except Exception as e:
            
            print(f"naver_login_error' : {str(e)}")


    def aha_login(self,id,pw):
        
        #아하 이메일 로그인 URL
        self.driver.get('https://auth.a-ha.io/login/email')
        self.driver.implicitly_wait(2) 

        try: 

            #email
            Email = self.driver.find_element(By.XPATH,'//input[@id="email"]')
            sleep(0.5)
            self.random_clicks.random_click('//input[@id="email"]',"XPATH")
            pyperclip.copy(id)
            Email.send_keys(Keys.CONTROL, 'v')

            #PW
            sleep(0.5)
            PW = self.driver.find_element(By.XPATH,'//input[@id="password"]')
            self.random_clicks.random_click('//input[@id="password"]',"XPATH")
            pyperclip.copy(pw)
            PW.send_keys(Keys.CONTROL, 'v')
            
            #로그인 버튼
            sleep(0.5)
            pyperclip.copy('blank')
            self.random_clicks.random_click("//button[contains(text(), '로그인')]",'XPATH')
            
        
            #청소 질문 목록으로 이동하기
            sleep(1)
            self.driver.get('https://www.a-ha.io/questions/categories/98')    

            
        except Exception as e:
            
            print(f"aha_login_error' : {str(e)}")


       