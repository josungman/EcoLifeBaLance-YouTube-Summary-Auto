from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log
from Method.Commom_DB.DB import Common_DB
import datetime



class gpt_summary_method():

    def __init__(self):

        #로그 init
        log = Log()
        self.log = log.activate() 

        # 키파일 열기
        with open('GPT_key.txt', 'r') as file:
            # 파일에서 전체 내용 읽기
            gpt_key = file.read().strip()  # strip()을 사용하여 불필요한 공백이나 줄바꿈 문자 제거

        # Set OpenAI API key
        openai.api_key = gpt_key

        # Answer_format(with caption) 캡션(자막시간) 있는경우
        self.html_caption_format = f'''
        
        <br>

        <h2><span style="font-size: 22px;">한 문장 요약</span></h2>
        <span style='margin: 20px 0px;'>한문장 요약 내용(따뜻한어투)</span>

        <br>

        <h2><span style="font-size: 22px;">동영상 하이라이트</span></h2>
        <details open>
            <summary><strong>접기 또는 펼치기👆</strong></summary>
        <table class="m-table-style noBorder" style="width: 100%;">
		<tbody>
			<tr>
				<td style="width: 50%; text-align: center;">
					<div style="text-align: left;"><strong>start시간(00:00)</strong><sub>(start시간(초로만표시)초)</sub> 동영상 하이라이트 내용(따뜻한어투)</div>
				</td>
				<td style="width: 50%; text-align: center;">

					<p style="text-align: left;"><strong>start시간(00:00)</strong><sub>(start시간(초로만표시)초)</sub> 동영상 하이라이트 내용(따뜻한어투)</p>
				</td>
			</tr>
			<tr>
				<td style="width: 50%; text-align: center;">start시간(초로만표시)초-캡쳐이미지</td>
				<td style="width: 50%; text-align: center;">start시간(초로만표시)초-캡쳐이미지</td>
			</tr>
		</tbody>
	</table>
        </details>

        '''

         # Answer_format(with nocaption) 캡션(자막시간) 없는 경우
        self.html_nocaption_format = f'''
        
        <br>

        <h2><span style="font-size: 22px;">한 문장 요약</span></h2>
        <span style='margin: 20px 0px;'>한문장 요약 내용(따뜻한어투)</span>

        <br>

        <h2><span style="font-size: 22px;">동영상 하이라이트</span></h2>
        <details open>
            <summary><strong>접기 또는 펼치기👆</strong></summary>
        <table class="m-table-style noBorder" style="width: 100%;">
		<tbody>
			<tr>
				<td style="width: 50%; text-align: center;">
					<div style="text-align: left;"><strong>순서.</strong> 동영상 하이라이트 내용(따뜻한어투)</div>
				</td>
				<td style="width: 50%; text-align: center;">

					<p style="text-align: left;"><strong>순서.</strong> 동영상 하이라이트 내용(따뜻한어투)</p>
				</td>
			</tr>
		</tbody>
	</table>
        </details>

        '''


    def error_db_reg(self,video_id,video_title,author,error): #에러시 DB 기록
        DB = Common_DB()
        
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        current_date_time = datetime.datetime.now()

        params = (video_id, video_title,video_url,author,str(current_date_time),'-',error)
        DB.execute_query("INSERT INTO youtube_video_reg_list (video_id, video_title, video_url,author,regdate,wj_url,error) VALUES (%s,%s,%s,%s,%s,%s,%s)",params)
        DB.close()
            
    # Function to parse transcript and extract text information
    def parse_text_info(self,input_list):
        #regex to remove timestamps and speaker names
        pattern = re.compile(r"'text':\s+'(?:\[[^\]]*\]\s*)?([^']*)'")
        output = ""
        for item in input_list:
            match = pattern.search(str(item))
            if match:
                text = match.group(1).strip()
                text = text.replace('\n', ' ')
                text = re.sub(' +', ' ', text)
                output += text + " "
        
        return output.strip()
    
    #캡션 가공
    def parse_captions_info(self,captions): 
       set_captions = str(captions).replace('\\n', '').replace('\\', '').replace('\'', '').replace(' start:','start:') 
       set_captions = re.sub(r', duration: \d+(\.\d+)?', '', str(set_captions))  # ', duration: 숫자' 패턴 제거
       set_captions = re.sub(r'(start: \d+)\.\d+', r'\1', str(set_captions))  # 'start: ' 뒤의 숫자에서 소수점 이하 제거
       
       return set_captions.strip()    

    # 형식 체크 (리스트 안에-> 딕셔너리 인지 체크)
    def check_if_all_dicts_in_list(self,lst):
        return all(isinstance(item, dict) for item in lst)

    # Function to generate summary using OpenAI API
    def generateSummaryWithCaptions(self,captions, summary_length, yt_url, yt_title, yt_description, yt_author,video_id):
        # Set summary length to default value if user does not select a summary length
        
        try:

            self.log.info(f'generateSummaryWithCaptions_start')

            message = f"제공된 동영상 정보 \
            캡션: {captions} \
            동영상 제목 : {yt_title} \
            채널 이름 : {yt_author} \
            캡쳐이미지 태그 부분 필요합니다. \
            캡션 기반으로 참고하여 한문장 요약 과 동영상 하이라이트 목록(start시간 포함) 따뜻한어투으로 답해주세요.\
            출력 토근이 넘어가는 경우 하이라이트 목록 적절하게 조정하여 출력"
            
          
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"귀하는 제공된 모든 YouTube 비디오(입력 URL을 통해)에 대해 긴 요약을 제공하는 보조자 입니다. 모든 규칙을 지켜주세요. \
                     1.따뜻한어투으로 요약(중요) \
                     2.HTML코드로 작성 \
                     3.{self.html_caption_format} 위 형식에 맞춰서 내용 작성 \
                     4.동영상 하이라이트 내용은 따뜻한어투으로 요약 (상황에 맞는 이모티콘 추가)"},
                    {"role": "user", "content": message}
                ],
                max_tokens=3700,
                n=1,
                stop=None,
                temperature=0.3,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Remove newlines and extra spaces from summary
            self.log.info(f'generateSummaryWithCaptions_complete')
            summary = summary = str(response.choices[0].message.content.strip()).replace('\n','').replace('\\','')
            return summary

        except openai.error.InvalidRequestError as e:
            
            self.caption_check = False
            self.log.error(f'generateSummaryWithCaptions_Error : {str(e)}')
            # Return error message if summary cannot be generated
            summaryNoCaptions = self.generateSummaryNoCaptions(summary_length, yt_url, yt_title, yt_description, yt_author,video_id)
            return summaryNoCaptions


    #  - This is a fallback function to generate a summary when no captions are provided by YouTube
    # - This function is called when the video is too long (causes character limit to openAI API, or there are no captions)
    def generateSummaryNoCaptions(self,summary_length, url, yt_title, yt_description, yt_author,video_id):
        
        self.log.info(f'generateSummaryNoCaptions_start')
        

        message = f"제공된 동영상 정보 \
        동영상 제목 :  {yt_title} \
        채널 이름 : {yt_author} \
        영상 설명: {yt_description} \
        정보 참고하여 한 문장 요약 과 동영상 하이라이트 목록 대화체 형식으로 답해주세요."
        
     
        #print("Parsing API without captions due to long video OR not captions (or both)...")
        try: 
            response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"귀하는 제공된 모든 YouTube 비디오(입력 URL을 통해)에 대해 긴 요약을 제공하는 보조자 입니다. 모든 규칙을 지켜주세요. \
                     1.따뜻한어투으로 요약(중요) \
                     2.HTML코드로 작성 \
                     3.{self.html_nocaption_format} 위 형식에 맞춰서 내용 작성 \
                     4.동영상 하이라이트 내용은 따뜻한어투으로 요약 (상황에 맞는 이모티콘 추가)"},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=3700,
                    n=1,
                    stop=None,
                    temperature=0.3,
                    top_p=0.5,
                    frequency_penalty=0,
                    presence_penalty=0
                    
                )
            
        except Exception as e: 
            
            # Return error message if summary cannot be generated
            self.caption_check = False
            self.error_db_reg(video_id,yt_title,yt_author,str(e))#최종 매서드 도착시 에러 발생 하면 에러 DB 등록 하기
            self.log.error(f'generateSummaryNoCaptions_Error : {str(e)}')
            summary = f"GPT_Suammary_Error : {str(e)}"
            return summary
        
        # Remove newlines and extra spaces from summary
        self.log.info(f'generateSummaryNoCaptions_complete')
        summary = str(response.choices[0].message.content.strip()).replace('\n','').replace('\\','')
        return summary



    def start(self,video_id,title,description,author):

        self.log.info(f'video_summary_start : {str(title)}')

        #set
        summary_length = 301
        url = 'https://www.youtube.com/watch?v=' + video_id
        
        #캡션 여부 반환
        self.caption_check = None

        try: #캐싱 부분 추가 하기
                transcript =  YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
                captions = transcript

                # 유효하지 않은 형식이거나 특정 메시지를 포함하는 경우 captions을 None으로 설정
                if not self.check_if_all_dicts_in_list(captions) or 'Could not retrieve a transcript for the video' in captions:
                    self.log.error(f'video_captions_notfound(skip)')
                    captions = None

        except Exception as e:
            
            self.log.error(f'video_captions_notfound(skip)')
            captions = None
                
        if captions:
    
            set_captions = self.parse_captions_info(captions)#캡션 가공
            self.caption_check = True
            summary = self.generateSummaryWithCaptions(set_captions, summary_length, url, title, description, author,video_id)
            
        else:
            
            self.caption_check = False
            summary = self.generateSummaryNoCaptions(summary_length, url, title, description, author,video_id)
            
        
        #return summary
        return {'content' : summary,'caption_check' : self.caption_check}



