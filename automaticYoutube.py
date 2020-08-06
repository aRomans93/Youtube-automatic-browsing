from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from selenium import webdriver
#import comments as com
import random
import time
import argparse
import numpy as np
from datetime import datetime
    
def headless_mode(headless, homedir, cwd):
    '''
    Seleccionando mode ejecución, el modo headless ejecuta el navehador en modo 
    oculto y no despliega una ventana de navegación.
    Nota: Cuando Headless sen encuentra en modo False es necesario tener las 
    ventanas del navegador cerradas.
    '''
    
    if headless:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("user-data-dir="+homedir+"/AppData/Local/Google/Chrome/User Data")
        driver = webdriver.Chrome(cwd + 'chromedriver.exe',chrome_options=chrome_options)
    
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
        chrome_options.add_argument("user-data-dir="+homedir+"/AppData/Local/Google/Chrome/User Data")
        driver = webdriver.Chrome(cwd + 'chromedriver.exe',chrome_options=chrome_options)
    
    return(driver)
    
def find_video_in_youtube(driver,search,name_video,pause):
    '''
    Esta función simula una busqueda real de un video en youtube, navega hacia
    la pagina, escribe y lanza la busqueda, a continiución realiza un scroll
    hasta encontrar el video indicado y entrar a vizualizarlo
    '''
    print('[INFO]: Navengando hacia Youtube')
    driver.get(url='https://www.youtube.com/')
    time.sleep(pause) # Descanso antes de escribir la busqueda
    
    print('[INFO]: Escribiendo la busqueda')
    element = driver.find_element_by_xpath("//input[contains(@id,'search')]")
    element.send_keys(search)
    element.submit() # Realizando busqueda 
    time.sleep(pause) # Descanso despues de escribir la busqueda, antes de enviarla
    
    start = time.time()
    while True:
        try:
            path_video = "//a[contains(@title,'" + name_video + "')]"
            element = driver.find_element_by_xpath(path_video)            
            ActionChains(driver).move_to_element(element).click(element).perform()
            #element.click()
            print('[INFO]: El video '+name_video+' ha sido encontrado y esta siendo vizualizado')
            time.sleep(10) # Tiempo para que cargue la pagina
            skipAd(driver)
            video_response = 1
            break
        except:
            time.sleep(pause)
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            print('[INFO]: El video aún no ha sido encontrado')
            end = time.time()
            elapsed = end - start
            print('[INFO]: El tiempo trancurrido es: ' + str(round(elapsed)) + ' segundos')
            
        if elapsed >= 20: # Tiempo que durará la busqueda se video
            print('[INFO]: El video no ha sido encontrado')
            video_response = 0
            break
        else:
            pass
        
    return driver, video_response
    
def likeVideo(driver, option):
    if option == 0:
        like_path = "//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a/yt-icon-button/button"
        to_like = driver.find_element_by_xpath(like_path)
        ActionChains(driver).move_to_element(to_like).click(to_like).perform()
        print("[INFO]: Me gusta ha sido seleccionado.")
    else:
        like_path = "//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a/yt-icon-button/button"
        to_like = driver.find_element_by_xpath(like_path)
        ActionChains(driver).move_to_element(to_like).click(to_like).perform()
        print("[INFO]: No me gusta ha sido seleccionado.")

def commentVideo(driver,comment):
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    time.sleep(5)
    
    comment_box_path = "//div[contains(@id,'placeholder-area')]/yt-formatted-string"
    comment_box = driver.find_element_by_xpath(comment_box_path)
    ActionChains(driver).move_to_element(comment_box).click(comment_box).perform()
    time.sleep(3)
    print("[INFO]: Se ha seleccionado la caja de comentarios")
    
    comment_box_path = "//div[contains(@id,'contenteditable-root')]"
    comment_box = driver.find_element_by_xpath(comment_box_path)
    comment_box.send_keys(comment)
    print("[INFO]: Se ha escrito el comentario")
            
    comment_button_path = "//ytd-button-renderer[contains(@id,'submit-button')]"
    to_comment = driver.find_element_by_xpath(comment_button_path)
    ActionChains(driver).move_to_element(to_comment).click(to_comment).perform()
    print("[INFO]: El comentario ha sido publicado.")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY - 300)")

def subscribeChannel(driver):
    subscribe_path = "//div[@id='meta-contents'] //*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button"
    to_subscribe = driver.find_element_by_xpath(subscribe_path)
    ActionChains(driver).move_to_element(to_subscribe).click(to_subscribe).perform()
    print("[INFO]: Se ha suscrito el usuario")
    
def getVideolen(driver):
    sel = Selector(text=driver.page_source)
    time_duration_path = "//span[contains(@class,'ytp-time-duration')]/text()"
    time_duration = sel.xpath(time_duration_path).extract_first()
    if time_duration.count(":") == 1:
        time_duration = "0:" + time_duration 
    video_length = datetime.strptime(time_duration,'%H:%M:%S')
    video_length_seconds = video_length.second + video_length.minute*60 + video_length.hour*3600
    return video_length_seconds
    
    
def nextVideo(driver):
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    time.sleep(5)
    path_next_videos = "//ytd-watch-next-secondary-results-renderer/div/ytd-compact-video-renderer["+str(np.random.choice(range(1,6)))+"]"
    next_video_random = driver.find_element_by_xpath(path_next_videos)
    ActionChains(driver).move_to_element(next_video_random).click(next_video_random).perform()
    print("[INFO]: Se selecionado el siguiente video de forma aleatoria")
    time.sleep(10)
    skipAd(driver)
    
def skipAd(driver):
    try:
        ad_button_path = "//button[contains(@class,'ytp-ad-skip-button ytp-button')]"
        to_skip = driver.find_element_by_xpath(ad_button_path)
        ActionChains(driver).move_to_element(to_skip).click(to_skip).perform()
        print("[INFO]: Se ha omitido el anuncio")
    except:
        print("[INFO]: No hubo anuncio")
    
def organic_find_video(search, name_video, comment, homedir, cwd, headless=False):
    '''
    Función para realizar visitas a videos de youtube de forma orgánica: Credenciales
    predefinidas del usuario, modo oculto del navegador, busqueda y selección del video, 
    consulta de status de inicio de sesión y Me gusta
    dic_videos: Diccionario con keys de busqueda de Youtube y con values de listas de nombres 
    con videos localizados en la misma busqueda.
    '''
    #search = random.choice(list(dict_videos.keys()))
    #name_video = random.choice(list(dict_videos[search]))
    #comment = random.choice(dict_videos[search][name_video])
    #print(search,name_video)
    
    homedir = homedir.replace("\\","/")
    cwd = cwd.replace("\\","/") + '/'
    
    pause = round(random.uniform(5, 6))
    driver = headless_mode(headless, homedir, cwd)
    driver, video_response = find_video_in_youtube(driver,search,name_video,pause)
    
    if video_response == 1:

        sel = Selector(text=driver.page_source)
        
        status_login_path = "//paper-button[contains(@aria-label,'Acceder')]/@aria-label"
        status_login = sel.xpath(status_login_path).extract_first()
        
        # Tiempo de reproducción del video
        average_timewatch = 0.7
        sd_timewatch = 0.1
        timewatch = np.random.normal(loc=average_timewatch, scale=sd_timewatch)
        video_length_seconds = getVideolen(driver)
        if timewatch > average_timewatch:
            timewatch2 = 20
        else: 
            timewatch2 = 0
        timewatch_1 = min(1, timewatch)
        timewatch_1 = round(video_length_seconds*timewatch_1)
        print(timewatch)
        print(timewatch_1)
        print(timewatch2)
        time.sleep(min(0,max(10,timewatch_1-10)))
        
        
        if status_login != 'Acceder': # Si la sesión esta iniciada status login será igual a None
            extra_time = 0
            prob_like = 0.5
            prob_comment = 0.5
            
            if np.random.choice([True,False], p=[prob_like, 1-prob_like]):
                status_like_path = "//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/@aria-pressed"
                status_like = sel.xpath(status_like_path).extract_first()
                status_dislike_path = "//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a/yt-icon-button/button/@aria-pressed"
                status_dislike = sel.xpath(status_dislike_path).extract_first()
                status_subs_path = "//div[@id='meta-contents'] //*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button/yt-formatted-string/text()"
                status_subs = sel.xpath(status_subs_path).extract_first()
                if (status_like == 'false') and (status_dislike == 'false'):
                    likes_dislikes_ratios = [0.95, 0.85, 0.75, 0.65, 0.55, 0.25]
                    likes_dislikes_ratio_distribution = [0.73, 0.1, 0.05, 0.04, 0.04, 0.04]
                    rng = np.random.RandomState(len(name_video))
                    likes_ratio = rng.choice(likes_dislikes_ratios, p=likes_dislikes_ratio_distribution)
                    like_options = [0, 1] # 0:Me Gusta, 1:No Me Gusta
                    like_or_dislike = np.random.choice(like_options, p=[likes_ratio, 1-likes_ratio])
                    likeVideo(driver, like_or_dislike)
                    if (like_or_dislike == 0) and (status_subs == 'Suscribirse'):
                        subscribeChannel(driver)
                else:
                    print("[INFO]: Ya se ha seleccionado Me gusta anteriormente en este video")
                    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
                    time.sleep(5)
                    driver.execute_script("window.scrollTo(0, window.scrollY - 300)")
                    if average_timewatch < timewatch < 1:
                        extra_time = 5
            if np.random.choice([True,False], p=[prob_comment, 1-prob_comment]):
                commentVideo(driver,comment)
                if average_timewatch < timewatch < 1:
                    extra_time = 5
            time.sleep(extra_time)
        if status_login == 'Acceder': # Si la sesión esta iniciada status login será igual a Acceder
            print("El status de la sesion es: ",status_login ,"No ha sido posible seleccionar me gusta")
        
        if timewatch > average_timewatch:
            start_time = time.time()
            while True:
                if timewatch < 1:
                    nextVideo(driver)
                else:
                    time.sleep(10)
                # Tiempo de reproducción del video
                average_timewatch = 0.7
                sd_timewatch = 0.3
                timewatch = np.random.normal(loc=average_timewatch, scale=sd_timewatch)
                video_length_seconds = getVideolen(driver)
                timewatch_1 = round(video_length_seconds*timewatch)
                print(timewatch)
                print(timewatch_1)
                time.sleep(min(0,timewatch_1))
                elapsed_time = time.time() - start_time
                if elapsed_time >= timewatch2:
                    break
            
        time.sleep(5)
    
    driver.close()    

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('search')
    parser.add_argument('name_video')
    #parser.add_argument('comment')
    #parser.add_argument('homedir')
    homedir = ""
    cwd = os.getcwd() #Ruta al driver de Chrome
    #parser.add_argument('cwd')
    args = parser.parse_args()
    
    organic_find_video(args.search, args.name_video, "Nice!", homedir, cwd)
    