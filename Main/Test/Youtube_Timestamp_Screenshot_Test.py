#현제 디렉토리에서 상위 폴더 디렉토리 추가
import sys
import os
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Project_Exclusive_Method.Youtube_Timestamp_Screenshot import Youtube_Timestamp_Screenshot
from Method.Utility.Detection_Driver import make_driver



class Test:

    def __init__(self):  #init

        #언디텍티드 드라이브 init
        self.driver = make_driver()

        # 요약 파싱 클래스 활성화(프로젝트 전용)
        self.youtube_Timestamp_Screenshot = Youtube_Timestamp_Screenshot(self.driver)

    def Youtube_Timestamp_Screenshot_test(self):

        #테스트 파라미터
        video_summary_result = {'video_id': 'FJQOTpGq_Sw','summary_timestamp_links': [{'timestamp_link': 'https://www.youtube.com/watch?v=QDWUNnUUt9g&t=0'}, {'timestamp_link': 'https://www.youtube.com/watch?v=QDWUNnUUt9g&t=14'}]}
      
        self.youtube_Timestamp_Screenshot.get_screenshot(video_summary_result)

#test하기
          
test = Test()
test.Youtube_Timestamp_Screenshot_test()