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


url = "https://x.com/lindaofheaven"


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
                repeat = 0
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
                                else:
                                    continue

                            # 处理div部分        
                            div_content = ""
                            div_elements = div.eles('xpath:.//div[@dir="auto"]')
                            if div_elements:
                                for ele in div_elements:
                                    if ele.tag != 'img':
                                        div_content += ele.text
                                
                                content = remove_lf(div_content) + "\n"
                                with open('./tmp.txt', 'r', encoding='utf-8') as f:
                                    if content not in f.read():
                                        append_to_file(content)
                                    else:
                                        repeat += 1
                                        continue
                            else:
                                continue
                    


                    elif month_element == month_to_stop:
                        return
                    else:
                        continue
                
                print(f"重复{repeat}次")

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
            try:
                page.run_js('window.scrollBy(0, 2000)')  
                divs = page.eles('xpath://div[contains(@aria-label, "时间线：") and contains(@aria-label, "的帖子")]/div/div')
                for div in divs:
                    time_element = div.ele(f'xpath:.//a[contains(@href, "/status/")]')
                    if time_element:
                        publish_time = time_element.text
                        month_element = publish_time.split('月')[0]
                        if month_element == month:
                            seek_time = time.time()
                            elapsed_seek_time = (seek_time - start_time)/60
                            print(f"找到{month}月，用时{elapsed_seek_time:.2f}分钟")
                            with open('./time.txt', 'a', encoding='utf-8') as f:
                                f.write(f"找到{month}月，用时{elapsed_seek_time:.2f}分钟\n")
                            return True
                        else:
                            continue
                    else:
                        continue
            except DrissionPage.errors.ElementLostError:
                print("元素失效，重新获取...")
                continue
            except Exception as e:
                print(f"发生其他错误: {e}")
                traceback.print_exc()

    except Exception as e:
        print(f"访问页面失败: {e}")
        traceback.print_exc()







try:
    page.get(url)
    start_time = time.time()
    if get_ranged_content(page,"2"):
        get_showed_content(page,"2","1")

    total_end_time = time.time()
    elapsed_total_time = (total_end_time - start_time)/60
    print(f"总用时: {elapsed_total_time:.2f}分钟")
    with open('./time.txt', 'a', encoding='utf-8') as f:
        f.write(f"总用时: {elapsed_total_time:.2f}分钟\n")






except Exception as e:
    print(f"访问页面失败: {e}")
    traceback.print_exc()