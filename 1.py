import DrissionPage
from DrissionPage import ChromiumPage, ChromiumOptions
import time
import traceback
from urllib.parse import urljoin
import os

# 创建配置对象
options = ChromiumOptions()
options.set_argument('--user-data-dir=./chrome_data')

# 使用配置创建页面对象
page = ChromiumPage(options)


url = "https://x.com/geekbb"


if not os.path.exists('./tmp.txt'):
    open('./tmp.txt', 'w', encoding='utf-8').close()
        


def  append_to_file(data):
    try:
        with open('./tmp.txt', 'a', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"保存数据失败: {e}")


def remove_lf(text):
    return text.replace('\n', '')



def get_showed_content(page,month_to_get,month_to_stop):
    try:
        while True: 
            try:    
                total_height = page.run_js('return document.body.scrollHeight')


                divs = page.eles('xpath://div[contains(@aria-label, "时间线：") and contains(@aria-label, "的帖子")]/div/div')
                for div in divs:
                    time_element = div.ele(f'xpath:.//a[contains(@href, "/status/")]')
                    if time_element:
                        publish_time = time_element.text
                        month_element = publish_time.split('月')[0]
                        if month_element == month_to_get:
                            publish_time_href = urljoin("https://x.com", time_element.attr('href'))
                            a_html = '<a href="' + publish_time_href + '">' + publish_time + '</a>'
                            with open('./tmp.txt', 'r', encoding='utf-8') as f:
                                if a_html not in f.read():
                                    append_to_file(a_html)

                            # 处理div部分        
                            div_content = ""
                            div_content = div.ele('xpath:.//div[@dir="auto"]')
                            if div_content:
                                for ele in div_content.eles('*'):
                                    if ele.tag != 'img':
                                        div_content += ele.html
                            
                                content = remove_lf(div_content.text) + "\n"
                                with open('./tmp.txt', 'r', encoding='utf-8') as f:
                                    if content not in f.read():
                                        append_to_file(content)
                            else:
                                continue
                    


                    elif month_element == month_to_stop:
                        return
                    else:
                        continue
                    

                page.run_js('window.scrollBy(0, 2000)')  

            except DrissionPage.errors.ElementLostError:
                print("元素失效，重新获取...")
                divs = page.eles('xpath://div[contains(@aria-label, "时间线：") and contains(@aria-label, "的帖子")]/div/div')
                continue
    except Exception as e:
        print(f"发生其他错误: {e}")
        traceback.print_exc()
        

def get_ranged_content(page,month):


    try:
        while True:
            page.run_js('window.scrollBy(0, 2000)')  
            divs = page.eles('xpath://div[contains(@aria-label, "时间线：") and contains(@aria-label, "的帖子")]/div/div')
            for div in divs:
                time_element = div.ele(f'xpath:.//a[contains(@href, "/status/")]')
                if time_element:
                    publish_time = time_element.text
                    month_element = publish_time.split('月')[0]
                    if month_element == month:
                            return True
                    else:
                            continue
                else:
                    continue
                

    except DrissionPage.errors.ElementLostError:
        print("元素失效，重新获取...")
    except Exception as e:
        print(f"访问页面失败: {e}")
        traceback.print_exc()







try:
    page.get(url)

    if get_ranged_content(page,"3"):
        get_showed_content(page,"3","2")









except Exception as e:
    print(f"访问页面失败: {e}")
    traceback.print_exc()