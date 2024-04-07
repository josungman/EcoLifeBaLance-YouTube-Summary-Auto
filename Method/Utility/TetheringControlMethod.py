import subprocess
import time
import requests
import random
from PyQt5.QtCore import QObject, pyqtSignal

class IntermediateObject(QObject):
    result_signal = pyqtSignal(str)

class TetheringControlMethod:
    def __init__(self):
        # 중간 결과를 전달하기 위한 객체 생성
        self.object = IntermediateObject()

    # USB 테더링을 켜는 함수
    def dataOn(self):
        subprocess.call("adb shell svc data enable",shell=True)

    # USB 테더링을 끄는 함수
    def dataOff(self):
        subprocess.call("adb shell svc data disable",shell=True)

    # 장치 연결 여부 확인 함수
    def check_android_device_connected(self):
        try:
            # adb devices 명령 실행
            result = subprocess.check_output(["adb", "devices"]).decode('utf-8')
            
            # 이제 각 줄을 확인하여 연결된 장치가 있는지 검사
            lines = result.splitlines()
            for line in lines:
                if "\tdevice" in line:
                    # 연결된 Android 장치가 존재함
                    return True
            return False
        except subprocess.CalledProcessError:
            # adb 명령이 실행 중 오류가 발생한 경우
            return False

    #IP 체크 하는 함수
    def get_external_ip_address(self):
        try:
            # 외부 IP 주소를 확인할 수 있는 무료 웹 서비스를 사용합니다.
            response = requests.get("http://ipinfo.io")
            time.sleep(random.randint(1,2))
            data = response.json()
            return data['ip']
        except Exception as e:
            return str(e)

   
    def check_and_tethering_connect(self):
        #이더넷 확인
        result = subprocess.run(["powershell", "(Get-NetAdapter).Status"], stdout=subprocess.PIPE, text=True)

        if "Up" in result.stdout:
            self.object.result_signal.emit(f"기존 이더넷 연결이 활성화되어 있습니다.\n\n테더링 실행전 안드로이드 장치를 USB에서 제거후 이더넷을 [사용안함] 으로 해주세요.\n\n*이미 테더링 실행중이라면 USB재연결후 '테더링연결' 다시 눌러주세요.")
            subprocess.run(["powershell", "control.exe /name Microsoft.NetworkAndSharingCenter"])
            return False
        else:
            self.object.result_signal.emit(f"이더넷 연결이 비활성화되어\n 테더링 실행 합니다.")
            

        if self.check_android_device_connected():
            self.object.result_signal.emit(f'안드로이드 장치가 연결되었습니다.')
            try:
                    #모델명
                    result = subprocess.check_output(["adb", "shell", "getprop" ,"ro.product.model"]).decode('utf-8')
                    print(result)
                    self.object.result_signal.emit(f'연결모델명 : {str(result.strip())}')

                    #화면켜기
                    subprocess.call("adb shell input keyevent KEYCODE_WAKEUP",shell=True)

                    time.sleep(2)
        
                    #IP확인
                    before_ip = self.get_external_ip_address()
                    if 'Error' in before_ip or 'error' in before_ip:
                        before_ip = '[찾을수 없음]'

                    time.sleep(2)

                    #테더링켜기
                    subprocess.call("adb shell svc usb setFunctions rndis",shell=True)
                
                    time.sleep(2)

                    #데이터 끄기 -> 켜기
                    self.dataOff()
                    time.sleep(2)
                    self.dataOn()
                    time.sleep(2)
                    #IP확인
                    after_ip = self.get_external_ip_address()
                    self.object.result_signal.emit(f'기존IP : {str(before_ip)} -> 변경IP : {str(after_ip)}')
                    
                    return True
                
            except Exception as e:
                    self.object.result_signal.emit(f'tethering_error : {str(e)}')
                    print(f'tethering_error : {str(e)}') 

        else:
            self.object.result_signal.emit(f"Android 장치가 연결되어 있지 않습니다.\nUSB를 통하여 Android 장치를 연결해주세요.(IP변경스킵됩니다)")
            print("Android 장치가 연결되어 있지 않습니다.")
            return False


    def tethering_connect(self):
       
        if self.check_android_device_connected():
            self.object.result_signal.emit(f'안드로이드 장치가 연결되었습니다.')
            try:
                    #모델명
                    result = subprocess.check_output(["adb", "shell", "getprop" ,"ro.product.model"]).decode('utf-8')
                    print(result)
                    self.object.result_signal.emit(f'연결모델명 : {str(result.strip())}')

                    #화면켜기
                    subprocess.call("adb shell input keyevent KEYCODE_WAKEUP",shell=True)

                    time.sleep(2)
        
                    #IP확인
                    before_ip = self.get_external_ip_address()
                    if 'Error' in before_ip or 'error' in before_ip:
                        before_ip = '[찾을수 없음]'

                    time.sleep(2)

                    #테더링켜기
                    subprocess.call("adb shell svc usb setFunctions rndis",shell=True)
                
                    time.sleep(2)

                    #데이터 끄기 -> 켜기
                    self.dataOff()
                    time.sleep(2)
                    self.dataOn()
                    time.sleep(2)
                    #IP확인
                    after_ip = self.get_external_ip_address()
                    self.object.result_signal.emit(f'기존IP : {str(before_ip)} -> 변경IP : {str(after_ip)}')
                    
                    return True
                
            except Exception as e:
                    self.object.result_signal.emit(f'tethering_error : {str(e)}')
                    print(f'tethering_error : {str(e)}') 

        else:
            self.object.result_signal.emit(f"Android 장치가 연결되어 있지 않습니다.\nUSB를 통하여 Android 장치를 연결해주세요.(IP변경스킵됩니다)")
            print("Android 장치가 연결되어 있지 않습니다.")
            return False


    #백과사전 진행시 사용되는 매서드
    def tethering_ipchange(self):
        if self.check_android_device_connected():
                    
                    print(f'테더링(안드로이드) 장치가 연결되었습니다.')

                    try:
                            #모델명
                            result = subprocess.check_output(["adb", "shell", "getprop" ,"ro.product.model"]).decode('utf-8')
                            print(result)
                            print(f'연결모델명 : {str(result.strip())}')

                            #화면켜기
                            subprocess.call("adb shell input keyevent KEYCODE_WAKEUP",shell=True)

                            time.sleep(2)
                
                            #IP확인
                            before_ip = self.get_external_ip_address()
                            if 'Error' in before_ip or 'error' in before_ip:
                                before_ip = '[찾을수 없음]'

                            time.sleep(2)

                            #테더링켜기
                            subprocess.call("adb shell svc usb setFunctions rndis",shell=True)
                        
                            time.sleep(2)

                            #데이터 끄기 -> 켜기
                            self.dataOff()
                            time.sleep(2)
                            self.dataOn()
                            time.sleep(2)
                            
                            #IP확인
                            after_ip = self.get_external_ip_address()
                            print(f'기존IP : {str(before_ip)} -> 변경IP : {str(after_ip)}')
                    
                            return str(after_ip)
                    
                    except Exception as e:
                            
                            print(f'tethering_error : {str(e)}') 
                            return 'Stop'
                            

        else:
                
                print(f'테더링(안드로이드) 장치를 찾을 수 없습니다.')
                return 'Stop'