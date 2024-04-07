#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Detection_Driver import make_driver

from Method.Utility.Gpt_summary import gpt_summary_method



class Test:

    def __init__(self):  #init

      self.summary = gpt_summary_method()

    def gpt_summary_method_test(self):
       
       #ccJcuQvzYyw (캡션)
       #mfyrVJpe4Bw (노캡션)

       video_id = 'ccJcuQvzYyw'
       video_title = '청소비용 700만원? 3년방치된 고양이 쓰레기 집 청소하기'
       description = '안녕하세요. 더러운일, 궂은일 마다하지 않는 청소명장 박보성 입니다. 실제로 700만원 짜리 쓰레기집청소 의뢰를 받고 현장에 출동 ...'
       author = '청소명장 박보성 / Clean Meister'


       summary_result = self.summary.start(video_id, video_title, description, author)
       print(summary_result)


#test하기
          
test = Test()
test.gpt_summary_method_test()