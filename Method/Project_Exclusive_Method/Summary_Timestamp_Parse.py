import re
import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log
from Method.Commom_DB.DB import Common_DB
import datetime

class Summary_Timestamp_Parse:
        
        def __init__(self):  #init
            
           #로그 init
           log = Log()
           self.log = log.activate() 
           
        
        def error_db_reg(self,video_id,video_title,author,error): #에러시 DB 기록
            DB = Common_DB()
            
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            current_date_time = datetime.datetime.now()

            params = (video_id, video_title,video_url,author,str(current_date_time),'-',error)
            DB.execute_query("INSERT INTO youtube_video_reg_list (video_id, video_title, video_url,author,regdate,wj_url,error) VALUES (%s,%s,%s,%s,%s,%s,%s)",params)
            DB.close()


        def parse_text_info(self, video_summary_result):
            
            try:
                video_summary = video_summary_result['video_summary']
                link = video_summary_result['link']
                
                # 정규식을 사용하여 <strong> 태그 안의 숫자와 '초'를 포함하는 패턴으로 추출하되, 매칭이 성공했는지 확인
                extracted_numbers = []
                
                #matches = re.findall(r'<strong>(\d+)초</strong>', video_summary)
                #matches = re.findall(r'<strong>\((\d+)초\)</strong>', video_summary)
                matches = re.findall(r'<sub>\((\d+)초\)</sub>', video_summary)
                
                for match in matches:
                    extracted_numbers.append({'timestamp_link': str(link) + '&t=' + str(int(match))})
                
                
                video_summary_result['summary_timestamp_links'] = extracted_numbers
                self.log.info(f'Summary_Timestamp_Parse_successful : {str(video_summary_result)}')

                return video_summary_result

            except Exception as e:
                
                self.log.error(f'Summary_Timestamp_Parse_Error : {str(e)}')
                self.error_db_reg(video_summary_result['video_id'],video_summary_result['title'],video_summary_result['author'],str(e)) #에러 발생시 DB 기록
                return f'Summary_Timestamp_Parse_Error : {str(e)}'



 