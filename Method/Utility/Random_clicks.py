from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.action_chains import ActionChains


class Random_clicks:

    def __init__(self,driver): 
       
        try:
            self.driver = driver
        except Exception as e:
            print(f'Random_clicks_init_error : {str(e)}')


    #선택한 앨리먼트 안바운더리안에 랜덤으로 클릭하기 
    def random_click(self,element_selector,selector_type="CSS_SELECTOR"):
        
        if selector_type == "CSS_SELECTOR":
            element = self.driver.find_element(By.CSS_SELECTOR,element_selector)
        else:
            element = self.driver.find_element(By.XPATH,element_selector)
        
        print(f'앨리먼트 사이즈 체크 : {str(element.size)}')
        if element.size['width'] != 0 and element.size['height'] != 0: #사이즈 찾을수 없는 경우 건너띄기..

            el_width,el_height = element.size['width'],element.size['height']
            targetX = random.randint(- int(el_width*0.3),int(el_width*0.3))
            targetY = random.randint(- int(el_height*0.3),int(el_height*0.3))
            print(f'{targetX},{targetY}')

            #클릭위치 확인시 주석해제
            # ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX,targetY).context_click().perform()
            # sleep(2)
            ActionChains(self.driver).move_to_element(element).pause(1).move_by_offset(targetX,targetY).click().perform()