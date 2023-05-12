# 1.从 https://i.iacg.site/ 复制专栏链接到剪贴板
# 2.直接运行此文件
# 如果出现keyerror，可能是因为cookie过期，需要去页面获取新cookie，后面会尝试自动获取cookie

import os 
import requests
from bs4 import BeautifulSoup

url = ""

global cookie
cookie = "_ga=GA1.1.1446522122.1683050021; _ga_5SMKPF4FNJ=GS1.1.1683817923.5.1.1683817942.0.0.0; cloudreve-session=MTY4MzgxNzk0MXxOd3dBTkZkTVRETlFRbFUxUmtaUVNsRkdTVUZOTWtSQldsVkpSRlJIUkVOTVZWUkZVMWd6VDFSRVQxWk1TMDlMTkVaU1RVZEhNMUU9fMjAo2zAt_O29zujgAkbqAb1pS3dsALXFjkErX6-esqD"

# 传入专栏网址，返回
def get_Title_n_link(url):
    """get专栏名和在线预览链接

    Args:
        url (str): 专栏网址

    Returns:
        tuple: 专栏名和在线预览链接
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'} 
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser') 
    title_tag = soup.find('h1', class_='post-title mb-3') 
    download_btn = soup.find('a', class_='btn btn-dark btn-sm btn-w-md btn-rounded')
    # TODO 增加另一种网页布局的兼容
    if (title_tag == None) or (download_btn == None):
        print("这种网页布局还没兼容")
        exit()
    return title_tag.text, download_btn['href']

# 从在线预览链接找到链接关键词和文件列表链接
def filelist(url):
    header = {'authority': 'share.sakurato.date', 'scheme': 'https', 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'cache-control': 'no-cache', 'cookie': cookie, 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(url, headers= header)
    if ('code' in res.text) and ('403' in res.text):
        print(f'l34:出现访问问题：{res.text}')
        exit()
    keyword = res.url.split('/')[-1]
    file_list_url = rf"https://share.sakurato.date/api/v3/share/list/{keyword}%2F?password=IACG.RIP"
    return keyword, file_list_url

# 通过文件列表得到文件id
def get_pic_ids(list_url):
    import requests
    header = {'authority': 'share.sakurato.date', 'scheme': 'https', 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'cache-control': 'no-cache', 'cookie': cookie, 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(list_url, headers= header)
    # if res.encoding =='br':
    #     res = brotli.decompress(res.read()).decode('UTF-8')
    data = res.json()
    try:
        data= data['data']['objects']
    except KeyError:
        print(f'{KeyError}, l51:这个错误可能产生于目标网站网络波动')
        exit()
    ids = []
    for i in data:
        ids.append((i['name'],i['id']))
    return ids

# 具体下载单个图片并返回其流数据
def download_pic(title_id, pic_id):
    import requests
    url = rf"https://share.sakurato.date/api/v3/share/thumb/{title_id}/{pic_id}?path=%2F"
    header = {'authority': 'share.sakurato.date', 'scheme': 'https', 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'cache-control': 'no-cache', 'cookie': cookie, 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=header)
    return res.content

# 通过ids调用图片的下载
def get_pics(post_title, title_id, var: list):
    """下载图片

    Args:
        post_title (_type_): 文章名
        title_id (_type_): 文件名
        var (list): 待下载文件列表
    """
    import random
    import time
    from tqdm import tqdm
    ok = ps = 0
    for i in tqdm(var, desc="下载图片中:", ascii=True):
        # 对文件进行一个覆盖写入
        if os.path.exists(rf"{folderpath}\{post_title}\{i[0]}"):
            ps += 1
            continue
        with open(rf"{folderpath}\{post_title}\{i[0]}", "wb") as p:
            p.write(download_pic(title_id, i[1]))
            ok += 1
        time.sleep(random.random())
    print(f'任务完成，{ok}张图片下载成功，{ps}张图片已存在')


if __name__ == "__main__":
    import pyperclip
    try:
        if url == "":
            print("正在读取剪贴板内容")
            url = pyperclip.paste()
        global folderpath 
        folderpath = r'D:\tmp'
        
        # get到专栏里面的标题和在线预览链接
        tmp = get_Title_n_link(url)
        post_title = tmp[0].replace('?', '')
        post_link = tmp[1]
        
        # Create a new directory
        print(f'当前任务：{post_title}')
        if not (os.path.exists(rf"{folderpath}\{post_title}")):
            os.mkdir(rf"{folderpath}\{post_title}")
        keywd_n_url = filelist(post_link)
        get_pics(post_title, keywd_n_url[0], get_pic_ids(keywd_n_url[1]))

    except KeyboardInterrupt:
        print('\n---用户手动中止---')
    