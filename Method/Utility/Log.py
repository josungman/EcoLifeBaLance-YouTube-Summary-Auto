from logging.handlers import RotatingFileHandler
import logging


#로그
class Log:

    def __init__(self):  #init

        # 로그 생성
        self.logger = logging.getLogger("Youtube_Summary_Project")

        # 로그의 출력 기준 설정
        self.logger.setLevel(logging.INFO)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # log를 console에 출력(로깅 핸들러 중복방지)
        if not any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers):
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        # log를 파일에 출력 (50MB 단위로 자르기,로깅 핸들로 중복방지)
        if not any(isinstance(handler, RotatingFileHandler) for handler in self.logger.handlers):            
            file_handler = RotatingFileHandler('./Logs/Youtube_Summary_Project.txt', maxBytes=50 * 1024 * 1024, backupCount=7, encoding='utf-8')  # 50MB, 최대 7개 파일 유지
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)


    def activate(self):

        return self.logger
