#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 目标：笔趣阁排行榜小说批量下载

'''
抓取网页头
'''
import requests,sys
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        # r.status_code # 获取响应码
        r.raise_for_status()  # 失败请求（响应码非200）主动抛出异常
        r.encoding = 'utf-8'  # 编码，因为返回报文中有中文字符，因此需要对返回信息进行编码
        return r.text # 字符串方式的响应体
    except:
        return 'error'


# 爬取每一类型的小说排行榜，获取小说链接，并写入文件（小说名称+小说链接）
def get_contnet(url):
    url_list = []
    soup = BeautifulSoup(get_html(url),'lxml') # 需要lxml模块

    category_list = soup.find_all('div',attrs={'class':'index_toplist mright mbottom'})
    history_list = soup.find_all('div', attrs={'class': 'index_toplist mbottom'})

    for cate in category_list:
        name = cate.find('div',attrs={'class':'toptab'}).span.text
        with open('novel_list.csv','a+') as f:
            f.write('\n小说种类：{} \n'.format(name))
            f.write(format(name))

        book_list = cate.find('div',attrs={'class':'topbooks'}).find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)

            with open('novel_list.csv','a') as f:
                f.write('小说名:{} \t 小说地址:{} \n'.format(title, link))

    for his in history_list:
        name = his.find('div', attrs={'class':'toptab'}).span.text
        with open('novel_list.csv', 'a') as f:
            f.write('\n小说种类: {} \n'.format(name))

        book_list = his.find('div', attrs={'class':'topbooks'}).find_all('li')

        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)

            with open('novel_list.csv', 'a') as f:
                f.write('小说名:{} \t 小说地址:{} \n'.format(title, link))

    url_list = list(set(url_list))
    return url_list


'''
获取章节内容及标题，写入文件
参数：
url-章节地址
txt_name-小说名称
'''
def get_one_txt(url,txt_name):
    print(url)
    print(txt_name)
    html = get_html(url).replace('<br/>','\n')
    soup = BeautifulSoup(html,'lxml')
    # 移除不必要的script标签，去除部分错误数据
    for s in soup('script'):
        s.extract()
    # print(soup.prettify())
    try:
        txt = soup.find('div',attrs={'id':'content'}).text
        title = soup.find('h1').text

        with open('小说/{}.txt'.format(txt_name),'a',encoding='UTF-8') as f:
            f.write(title + '\n\n')
            print('ok_1')
            f.write(txt)
            print('ok_2')
    except:
        print('ERROR!')

'''
获取单本小说所有的章节地址
参数：
url-小说地址
'''
def get_txt_url(url):
    url_list = []
    soup = BeautifulSoup(get_html(url), 'lxml')

    list_a = soup.find_all('dd')
    print(list_a)
    txt_name = soup.find('dt').text

    '''
    with open('小说/{}.txt'.format(txt_name), 'a') as f:
        f.write('小说名称：{} \n'.format(txt_name))
    '''

    for url in list_a:
        url_list.append('http://www.qu.la/' + url.a['href'])

    print(url_list)
    return url_list,txt_name


if __name__ == '__main__':
    url = 'http://www.qu.la/paihangbang/'
    url_list = get_contnet(url)
    for url in url_list:
        chart_list ,txt_name = get_txt_url(url)
        for char_url in chart_list:
            get_one_txt(char_url,txt_name)
