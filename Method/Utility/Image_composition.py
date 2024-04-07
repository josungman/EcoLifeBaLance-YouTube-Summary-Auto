from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import re
import os
import paramiko

class image_composition:

   def composition(self,aha_url,title):
    try:
        # 현재 스크립트 파일의 절대 경로 Method 까지
        project_path = os.path.dirname(os.path.realpath(__file__))
        # 프로젝트 경로 두단계 위
        project_dir = os.path.abspath(os.path.join(project_path, "../.."))
        
        # 이미지와 폰트 파일 로드
        image_path = os.path.join(project_dir, 'imgs', 'base', '2.png')
        font_path = os.path.join(project_dir, 'fonts', 'Jalnan2TTF.ttf')
        logo_path = os.path.join(project_dir, 'imgs', 'loge', 'black.png')
        
        #font_path = 'C:\\Python_Project\\Automatic_creation_of_content_intellectual_bypass_Advancement_V1\\fonts\\Jalnan2TTF.ttf'
        #logo_path = 'C:\\Python_Project\\Automatic_creation_of_content_intellectual_bypass_Advancement_V1\\imgs\\loge\\white.png'

        image = Image.open(image_path)
        logo = Image.open(logo_path)
        font = ImageFont.truetype(font_path, 60)

        # 이미지의 밝기를 조절 (70%로 설정)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.8)

        # 로고의 크기를 조절하고 이미지의 우측 상단에 위치시키기
        logo.thumbnail((100, 100))  # 로고의 최대 크기를 100x100px로 설정
        image_width, image_height = image.size
        logo_width, logo_height = logo.size

        # 로고를 이미지 우측 상단에 위치시키기 위한 좌표 계산
        logo_position = (image_width - logo_width - 10, 5)

        # 로고를 이미지에 합성
        image.paste(logo, logo_position, logo)

        # 이미지 드로잉 객체 초기화
        draw = ImageDraw.Draw(image)

        # 텍스트 줄바꿈 함수 정의
        def draw_multiline_text(draw, text, font, max_width, fill, shadow_color):
            lines = []
            words = text.split()
            while words:
                line = words.pop(0)
                while words and draw.textsize(line + ' ' + words[0], font=font)[0] < max_width:
                    line += ' ' + words.pop(0)
                lines.append(line)

            # 전체 텍스트 블록의 높이를 계산하여 이미지 중앙에 배치
            total_height = sum([draw.textsize(line, font=font)[1] for line in lines])
            current_height = (image.height - total_height) / 2

            for line in lines:
                line_width, line_height = draw.textsize(line, font=font)
                # 텍스트 그림자 추가
                draw.text(((image.width - line_width) / 2 + 3, current_height + 3), line, font=font, fill=shadow_color)
                # 텍스트 그리기
                draw.text(((image.width - line_width) / 2, current_height), line, font=font, fill=fill)
                current_height += line_height

        # 텍스트 위치와 최대 너비 설정
        max_text_width = image.width - 2 * 10  # 양쪽에 10픽셀의 여백

        # 텍스트를 이미지에 그리는 함수 호출
        text = f"Q.{str(title)}"
        draw_multiline_text(draw, text, font, max_text_width, "white", "black")

        # 아하 url docid 추출
        path_part = aha_url.split("?")[0]  # Removes the query parameters
        extracted_part = path_part.split("/")[-1]
        
        # 폴더 경로 설정
        folder_path = f'C:\\AI_IMAGE_FAQ\\{extracted_part}'

        # 폴더가 존재하지 않으면 생성
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 줄바꿈 처리된 텍스트가 포함된 이미지 저장
        edited_image_path_multiline = f'{folder_path}\\faq_img.png'
        image.save(edited_image_path_multiline)

        
        # SFTP 추가 업로드
        # 연결 정보
        local_image_path = edited_image_path_multiline
        sftp_host = ''
        sftp_port = 22  # SFTP 기본 포트는 22번입니다
        sftp_user = ''
        sftp_password = ''

        # SFTP 서버 경로
        remote_folder_path = f'{extracted_part}'

        # SFTP 연결 설정
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_user, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # 폴더 생성 여부 확인 및 생성
        self.create_remote_folder(sftp, remote_folder_path)

        # SFTP 서버 경로로 이동
        sftp.chdir(remote_folder_path)

        # 이미지 업로드
        remote_image_path = f'{remote_folder_path}/faq_img.png'
        sftp.put(local_image_path,f'/{remote_image_path}')


        #return edited_image_path_multiline #로걸경로
        return 'https://elbserver.store/static/woowarhanclean_img/AI_Image/' + remote_image_path #서버경로

    except  Exception as e:

        print(f'image_composition_error : {str(e)}')
        return f'image_composition_error : {str(e)}'
    


   def create_remote_folder(self,sftp, remote_folder_path):
        folders = remote_folder_path.split('/')
        current_path = ''
        for folder in folders:
            if folder:
                current_path += f'/{folder}'
                try:
                    sftp.stat(current_path)  # 폴더가 이미 존재하는지 확인
                except IOError:
                    print(f"폴더가 존재하지 않아 새로 생성합니다: {current_path}")
                    sftp.mkdir(current_path)