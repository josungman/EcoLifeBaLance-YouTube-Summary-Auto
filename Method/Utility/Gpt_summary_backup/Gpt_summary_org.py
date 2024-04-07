from youtube_transcript_api import YouTubeTranscriptApi
import os
import re
import openai


class gpt_summary_method():

    def __init__(self):

        # Set OpenAI API key
        openai.api_key = '-'

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
        # Set default length to 200 tokens
        # Set summary length to default value if user does not select a summary length
        capprint = len(captions)
        #print(f"{capprint}")
        try:
            if summary_length >= 300:
                message = f"Please provide a extremely long and comprehensive summary based on the closed captions of this yt video provided here:\n\n {captions}\n\n MAKE SURE IT IS AROUND {summary_length} words long.Here is the video link: {yt_url} along with its title: {yt_title} from the channel: {yt_author} and in highlight list format Please answer in Korean"
            else:
                message = f"Please provide a long and comprehensive summary based on the closed captions of this yt video provided here:\n\n {captions}\n\n MAKE SURE IT IS AROUND {summary_length} words long.Here is the video link: {yt_url} along with its title: {yt_title} from the channel: {yt_author} and in highlight list format Please answer in Korean"

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant for YTRecap, a webapp that provides very comprehensive and lengthy summaries for any provided youtube video (via input url)"},
                    {"role": "user", "content": message}
                ],
                max_tokens=4500,
                n=1,
                stop=None,
                temperature=0.5,
            )
            # Remove newlines and extra spaces from summary
            summary = response.choices[0].message.content.strip()
            return summary

        except openai.error.InvalidRequestError:
            # Return error message if summary cannot be generated
            summaryNoCaptions = self.generateSummaryNoCaptions(summary_length, yt_url, yt_title, yt_description, yt_author)
            return summaryNoCaptions


    #  - This is a fallback function to generate a summary when no captions are provided by YouTube
    # - This function is called when the video is too long (causes character limit to openAI API, or there are no captions)
    def generateSummaryNoCaptions(self,summary_length, url, yt_title, yt_description, yt_author):
        if summary_length >= 300: 
            message = f"Please provide a extremely long and in depth comprehensive summary about this video \n\n URL: {url} \n\n Please make sure summary length is approximately {summary_length} words. Please use the title of the video here {yt_title} \n\n the channel name here {yt_author} \n\n and the descripton here: {yt_description} to provide a summary overview of the video and in highlight list format Please answer in Korean"
        else:
            message = f"Please provide an in depth summary about this video \n\n. URL: {url} \n\n Please make sure summary length is approximately {summary_length} words. Please use the title of the video here {yt_title} \n\n the channel name here \n\n {yt_author} and the descripton here: \n\n {yt_description} to provide a summary overview of the video and in highlight list format Please answer in Korean"
        #print("Parsing API without captions due to long video OR not captions (or both)...")
        try: 
            response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI assistant for YTRecap, a webapp that provides very comprehensive and lengthy summaries for any provided youtube video (via input url)"},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=4500,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
        except: 
            # Return error message if summary cannot be generated
            summary = "Uh oh! Sorry, we couldn't generate a summary for this video and this error was not handled. Please visit source-code: https://github.com/nicktill/YTRecap/issues and open a new issue if possibe (it is likely due to the content of the yt video description being too long, exceeding the character limit of the OpenAI API).  "
            return summary
        
        # Remove newlines and extra spaces from summary
        summary = response.choices[0].message.content.strip()
        return summary



    def start(self,video_id,title,description,author):

        #set
        summary_length = 301
        url = 'https://www.youtube.com/watch?v=' + video_id


        try: 
                transcript =  YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
                captions = self.parse_text_info(transcript)

                if captions in 'Could not retrieve a transcript for the video':
                   captions = None

        except Exception as e:

            print(f'{str(e)}')
            captions = None
                
        if captions:
            summary = self.generateSummaryWithCaptions(captions, summary_length, url, title, description, author)
        else:
            summary = self.generateSummaryNoCaptions(summary_length, url, title, description, author)

        return summary






