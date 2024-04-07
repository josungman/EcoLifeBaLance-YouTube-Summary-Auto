from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
import os
import sys
current_dir = os.path.dirname(__file__)
utility_path = os.path.join(current_dir, '../../')
sys.path.append(utility_path)
from Method.Utility.Log import Log


class gpt_summary_method():

    def __init__(self):

        #로그 init
        log = Log()
        self.log = log.activate() 

        # Set OpenAI API key
        openai.api_key = '-'

        # Answer_format
        self.html_format = f'''
        <h3>제목</h3>

        <br>
        <br>

        <H4>한 문장 요약</H4>
        <span style='margin: 20px 0px;'>한문장 요약 내용(따뜻한어투)</span>

        <br>
        <br>

        <H4>동영상 하이라이트</H4>

        <ul>
            
            <li style='margin: 20px 0px;'><strong>동영상 하이라이트 내용(따뜻한어투)</strong></li>
            
        </ul>

        '''

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

    # Function to generate summary using OpenAI API
    def generateSummaryWithCaptions(self,captions, summary_length, yt_url, yt_title, yt_description, yt_author):
        # Set summary length to default value if user does not select a summary length
        
        try:

            self.log.info(f'generateSummaryWithCaptions_start')

            if summary_length >= 300:
                message = f"제공된 동영상 정보 \
                캡션: {captions} \
                {summary_length} 단어 인지 확인 하세요. \
                URL : {yt_url} \
                동영상 제목 : {yt_title} \
                채널 이름 : {yt_author} \
                캡션 기반으로 참고하여 한문장 요약 과 동영상 하이라이트 목록 따뜻한어투으로 답해주세요."
                
            else:
                message = f"제공된 동영상 정보 \
                캡션: {captions} \
                {summary_length} 단어 인지 확인 하세요. \
                URL : {yt_url} \
                동영상 제목 : {yt_title} \
                채널 이름 : {yt_author} \
                캡션 기반으로 참고하여 한문장 요약 과 동영상 하이라이트 목록 따뜻한어투으로 답해주세요."
                

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"귀하는 제공된 모든 YouTube 비디오(입력 URL을 통해)에 대해 긴 요약을 제공하는 보조자 입니다. 모든 규칙을 지켜주세요. \
                     1.따뜻한어투으로 요약(중요) \
                     2.HTML코드로 작성 \
                     3.{self.html_format} 위 형식에 맞춰서 내용 작성 \
                     4.동영상 하이라이트 내용은 따뜻한어투으로 요약 (상황에 맞는 이모티콘 추가)"},
                    {"role": "user", "content": message}
                ],
                max_tokens=4500,
                n=1,
                stop=None,
                temperature=0.5,
                frequency_penalty=0,
                presence_penalty=0
            )
            # Remove newlines and extra spaces from summary
            summary = summary = str(response.choices[0].message.content.strip()).replace('\n','').replace('\\','')
            return summary

        except openai.error.InvalidRequestError:

            self.log.error(f'generateSummaryWithCaptions_Error')
            # Return error message if summary cannot be generated
            summaryNoCaptions = self.generateSummaryNoCaptions(summary_length, yt_url, yt_title, yt_description, yt_author)
            return summaryNoCaptions


    #  - This is a fallback function to generate a summary when no captions are provided by YouTube
    # - This function is called when the video is too long (causes character limit to openAI API, or there are no captions)
    def generateSummaryNoCaptions(self,summary_length, url, yt_title, yt_description, yt_author):
        
        self.log.info(f'generateSummaryNoCaptions_start')
        
        if summary_length >= 300: 
            message = f"제공된 동영상 정보 \
            URL: {url} \
            {summary_length} 단어인지 확인하세요. \
            동영상 제목 :  {yt_title} \
            채널 이름 : {yt_author} \
            영상 설명: {yt_description} \
            정보 참고하여 한 문장 요약 과 동영상 하이라이트 목록 대화체 형식으로 답해주세요."
            
        else:
            message = f"제공된 동영상 정보 \
            URL: {url} \
            {summary_length} 단어인지 확인하세요. \
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
                     3.{self.html_format} 위 형식에 맞춰서 내용 작성 \
                     4.동영상 하이라이트 내용은 따뜻한어투으로 요약 (상황에 맞는 이모티콘 추가)"},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=4500,
                    n=1,
                    stop=None,
                    temperature=0.5,
                    top_p=0.5,
                    frequency_penalty=0,
                    presence_penalty=0
                    
                )
            
        except Exception as e: 
            # Return error message if summary cannot be generated
            #summary = "Uh oh! Sorry, we couldn't generate a summary for this video and this error was not handled. Please visit source-code: https://github.com/nicktill/YTRecap/issues and open a new issue if possibe (it is likely due to the content of the yt video description being too long, exceeding the character limit of the OpenAI API).  "
            self.log.error(f'generateSummaryNoCaptions_error : {str(e)}')
            summary = f"GPT_Suammary_Error : {str(e)}"
            return summary
        
        # Remove newlines and extra spaces from summary
        summary = str(response.choices[0].message.content.strip()).replace('\n','').replace('\\','')
        return summary



    def start(self,video_id,title,description,author):

        self.log.info(f'video_summary_start : {str(title)}')

        #set
        summary_length = 301
        url = 'https://www.youtube.com/watch?v=' + video_id


        try: 
                transcript =  YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
                captions = self.parse_text_info(transcript)

                if captions in 'Could not retrieve a transcript for the video':
                   captions = None

        except Exception as e:
            #print(f'{str(e)}')
            self.log.error(f'video_captions_notfound(skip)')
            captions = None
                
        if captions:
            summary = self.generateSummaryWithCaptions(captions, summary_length, url, title, description, author)
        else:
            summary = self.generateSummaryNoCaptions(summary_length, url, title, description, author)

        return summary






