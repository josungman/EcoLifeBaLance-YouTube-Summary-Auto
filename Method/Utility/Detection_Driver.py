from user_agents import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import random, time
import os


def make_user_agent(ua,is_mobile):

    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"

    if is_mobile:
       platform_info = "Linux armv8l"
       architecture = ""
    else: # Window
       platform_info = "Win32"
       model = ""
    RET_USER_AGENT = {
       "appVersion" : ua.replace("Mozilla/",""),
       "userAgent" : ua,
       "platform" : platform_info,
       "acceptLanguage" : "ko-KR, ko, en-US, en",
       "userAgentMetadata":{
          "brands":[
             #{"brand":" Not?A_Brand", "version":"24"},
             #{"brand":"Chromium","version":f"{version}"},
             #{"brand":"Google Chrome","version":f"{version}"},
             {"brand":"Google Chrome","version":f"{version}"},
             {"brand":"Chromium","version":f"{version}"},
             {"brand":" Not?A_Brand", "version":"24"}   
          ],
          "fullVersion":f"{ua_full_version}",
          "platform" : platform,
          "platformVersion" : platform_version,
          "architecture" : architecture,
          "model" : model,
          "mobile" : is_mobile
       }
    }
    return RET_USER_AGENT

def read_agents():
   agents = []
   f = open("./useragents/useragents.txt","r",encoding="utf8")
   while True:
      line = f.readline()
      if not line:
         break
      agents.append(line.rstrip())
   return agents

def make_driver(): #드라이버 호출 함수
   try:
    pc_device = ["1920,1440","1920,1200","1920,1080","1600,1200","1600,900",
            "1536,864","1440,1080","1440,900","1360,768"]

    mo_device = ["360,640","360,740","375,667","375,812","412,732",
            "412,846","412,869","412,892","412,915"]
    
    
    width,height = random.choice(mo_device).split(",")
    print(width,height)

    UA_list = read_agents()
    UA = random.choice(UA_list)
    print(UA)

    options = uc.ChromeOptions()

    #User Agent 속이기
    options.add_argument(f'--user-agent={UA}')
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument("--disable-logging")

    #쿠키
    rand_user_folder = random.randrange(1,100)
    userCookieDir = os.path.abspath(f"./cookies/{rand_user_folder}")
    if os.path.exists(userCookieDir) == False:
       print(userCookieDir,"폴더가 없어서 생성함")
       os.mkdir(userCookieDir)
    options.user_data_dir = userCookieDir


    driver = uc.Chrome(options=options)

    UA_Data = make_user_agent(UA,True)
    driver.execute_cdp_cmd("Network.setUserAgentOverride",UA_Data)   
    

    #Max Touch Point 변경
    Mobile = {"enabled":True,"maxTouchPoints":random.choice([1,5])}
    driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled",Mobile)
    driver.execute_cdp_cmd("Emulation.setNavigatorOverrides",{"platform":"Linux armv8l"})
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
        "width":int(width),
        "height":int(height),
        "deviceScaleFactor" : 1,
        "mobile": True
    })

    #위치 정보 변경 Geo Location 변경하기
    def generate_random_geolocation():
        ltop_lat = 37.600675591386036
        ltop_long = 126.91886223283079
        rbottom_lat = 37.54418005997888
        rbottom_long = 127.05543528099847

        targetLet = random.uniform(rbottom_lat,ltop_lat)
        targetLong = random.uniform(ltop_long,rbottom_long)
        return {"latitude" : targetLet,"longitude" : targetLong,"accuracy":100}
    GEO_DATA = generate_random_geolocation()
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride",GEO_DATA)
   
    #User Agent 적용
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride",UA_Data)
    driver.set_window_position(0, 0)
    
    return driver
   
   except Exception as e:
      print(f'Error : {str(e)}')
      driver = None
      return driver




