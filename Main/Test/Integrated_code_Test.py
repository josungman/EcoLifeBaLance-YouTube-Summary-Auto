#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Detection_Driver import make_driver
from Method.Integrated_code.Integrated_code import Integrated_code



class Test: #통합 작업 테스트 코드

    def __init__(self):  #init

      # 계정 파일 열기
      with open('WJ_Account.txt', 'r') as file:
        # 파일에서 첫 번째 줄 읽기
        line = file.readline().strip()  # strip()을 사용하여 줄바꿈 문자 제거    
        # 쉼표로 구분하여 ID와 PW 추출
        ID, PW = line.split(',')

      #언디텍티드 드라이브 init
      self.driver = make_driver()
      self.integrated_code = Integrated_code(self.driver,ID,PW)

    def Integrated_code_Test(self):
       
        self.integrated_code.start()
       


#test하기   
test = Test()
test.Integrated_code_Test()