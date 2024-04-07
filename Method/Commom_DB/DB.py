import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log
import pymysql
from time import sleep

class Common_DB:
        
        def __init__(self):  #init
            
           #로그 init
           log = Log()
           self.log = log.activate() 
           
           #DB init(연결 실패시 최대 5번 재시도)
           max_retries = 5
           retry_delay = 5  # 5초 후 재시도
           retries = 0

           #DB에서 커넥션 정보 가져오기
           file_path = './DB_Connecting_Info.txt'
           with open(file_path, 'r') as file:
                connection_info = file.readlines()

           get_host = connection_info[0].split("=")[1].strip()
           get_user = connection_info[1].split("=")[1].strip()
           get_db = connection_info[2].split("=")[1].strip()
           get_password = connection_info[3].split("=")[1].strip()

           while retries < max_retries:
               
                try:
                    self.connection = pymysql.connect(host=get_host, user=get_user, db=get_db, password=get_password, charset='utf8',connect_timeout=15)
                    self.cursor = self.connection.cursor()
                    self.log.info(f"DB_Init_Complete")
                    break
                except Exception as e: 
                    
                    self.connection = None
                    self.cursor = None
                    
                    #self.log.error(f'DB_Init_Error : {str(e)}')
                    self.log.error(f"DB_Init_Error: {str(e)}, {retries + 1}Re Trying...")
                    
                    sleep(retry_delay)  # 재시도 전 대기
                    retries += 1
            
           if retries == max_retries: #최대횟수 초과 에러 발생
            self.log.error(f"Database connection failed, maximum number of retries exceeded")     


        def execute_query(self, query, params=None):
            """SQL 쿼리 실행"""
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                self.connection.commit()
                self.log.info(f'DB_execute_query_successful\n{str(query)}')

            except pymysql.Error as e:
                self.log.error(f'DB_execute_query_Error : {str(e)}')
                print(f"Error: {e}")


        def execute_read_query(self, query, params=None):
            """데이터 조회 쿼리 실행"""
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                
                result = self.cursor.fetchall()
                self.log.info(f'DB_execute_read_query_successful\n{str(query)}')
                return result
            
            except pymysql.Error as e:
                self.log.error(f'DB_execute_read_query_Error : {str(e)}')
                return None
            
        def close(self):
            """데이터베이스 연결 종료"""
            if self.connection:
               self.connection.close()
               self.cursor.close()