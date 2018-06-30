# -*- coding: utf-8 -*-

"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""


works_Jiahe = ['毕业前杀人游戏', '沉睡的森林', '麒麟之翼', '恶意', '红手指', '祈祷落幕时', '谁杀了他', '我杀了他', '新参者', '再一个谎言之寒冷的灼热']
works_Tangchuan = ['嫌疑犯X的献身', '伽利略的苦恼', '禁忌游戏', '圣女的救济', '盛夏方程式', '虚像的小丑', '侦探伽利略', '侦探俱乐部']

# cookies and user agent have been replaced
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',\
    'Cookie': 'll="118172"; bid=vYEOA3Bzm-Q; __yadk_uid=3esCXn0AAxGgzpvy8pJDfpzKZ67Yfck1; viewed="5958726"; gr_user_id=e6d49a87-95a5-4faf-9522-64bed670fd3d; _vwo_uuid_v2=EFBFC5B9C59D45AB4D171C508310329B|f057734b9d44fdb1334f40bb79bdeb27; ap=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1515258996%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0-pBdmCt49kUg--j7M8DI7JeIQBtT-H6o2-LOJuEmwe%26wd%3D%26eqid%3Dbcd0121d0002a339000000045a510471%22%5D; __utmt=1; _ga=GA1.2.807433426.1490775536; _gid=GA1.2.1715481460.1515258998; ps=y; ue="lyditalee@gmail.com"; dbcl2="122980628:GtLbF4C+8Jk"; ck=qAch; _pk_id.100001.8cb4=134a18767bcb8b15.1491198526.15.1515259373.1515249584.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.807433426.1490775536.1515249571.1515258998.25; __utmb=30149280.3.10.1515258998; __utmc=30149280; __utmz=30149280.1515258998.25.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.12298',\
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',\
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',\
    'Cache-Control': 'max-age=0'}

# repeatedly request data from website
para = {'t':'general', 'q': '毕业前杀人游戏', 'correction': '1', 'search_hash_id':'4f6c83f37717c6bd8a4f339f08fbac89', 'offset': '5', 'limit': '10'}
para2 = {'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics',\
        'offset':'2',\
        'limit':'20',\
        'sort_by':'default'}

Book_Comment_Path = 'D:\DataMiningCourse\\Book_Comment.txt'
Video_Comment_Path = 'D:\DataMiningCourse\\Video_Comment.txt'
Movie_Comment_Path = 'D:\DataMiningCourse\\Movie_Comment.txt'
projectPath = 'D:\DataMiningCourse\爬虫结果\\'


def Searching_html(work, num = 10):
    book_dict = {}
    video_dict = {}
    movie_dict = {}
    book_cnt = video_cnt = movie_cnt = 0
    url = 'https://www.douban.com/search?q=' + work
    r = requests.get(url, headers=headers)
    content = r.content
    soup = bs4.BeautifulSoup(content, 'lxml')

    # From the source code of douban website <div class = title>
    results = soup.find_all('div', {'class': 'title'})
    pat_content = r'<a href="(.*?)"'
    pat_type = r'<span>(.*)</span>'

    for result in results:
        soup2 = bs4.BeautifulSoup(str(result), 'lxml')
        type = soup2.find('span')
        type = re.findall(pat_type, str(type))
        print(type)
        if type != []:
            title_url = soup2.find("a")
            title_url = re.findall(pat_content, str(title_url))
            if type[0] == "[书籍]":
                book_cnt += 1
                book_dict[type[0] + '_' + work + str(book_cnt)] = title_url[0]
            elif type[0] == "[电视剧]":
                video_cnt += 1
                video_dict[type[0] + '_' + work + str(video_cnt)] = title_url[0]
            elif type[0] == "[电影]":
                movie_cnt += 1
                movie_dict[type[0] + '_' + work + str(movie_cnt)] = title_url[0]
            else:
                pass
        else:
            pass
    print(book_dict)
    print(video_dict)
    print(movie_dict)
    return book_dict, video_dict, movie_dict


def collect_info(name, url, LogPath):
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    short_comments = soup.find_all('p', {'class': 'comment-content'})
    pat_comment_content = r'<p class="comment-content">([\s\S]*?)</p>'
    # pat_html = r'<[\s\S]*?>'
    try:
        for comment in short_comments:
            comment_string = str(comment)
            print('comment: ' + comment_string)
            tmp = re.findall(pat_comment_content, comment_string)
            print('tmp: ' + str(tmp[0]))
            tmp_str = str(tmp[0])
            if len(tmp_str) != 0:
                result = tmp_str
            result = name + '\r\n' + result + '\r\n==============\r\n'
            print('result:' + result)
            with open(LogPath + '\\short_comments.txt', 'a') as f:
                try:
                    f.write(result)
                except:
                    logging.warning(name + '      ' + url)
                    pass
    except:
        logging.warning(name + '===>null')


def main():
    for work in works_Tangchuan[0:]:
        print(work)
        work_Path = projectPath+work
        os.mkdir(work_Path)
        book_dict, video_dict, movie_dict = Searching_html(work, 80)
        with open(work_Path+'\\dict.txt', 'w') as f:
            for name, url in book_dict.items():
                try:
                    f.write(name+'     '+url+'\r\n')
                except:
                    logging.warning(url)
            f.write('==========================\r\n')
            for name, url in video_dict.items():
                try:
                    f.write(name+'     '+url+'\r\n')
                except:
                    logging.warning(url)
            f.write('==========================\r\n')
            for name, url in movie_dict.items():
                try:
                    f.write(name+'     '+url+'\r\n')
                except:
                    logging.warning(url)
            f.write('==========================\r\n')
        for name, url in book_dict.items():
            collect_info(name, url, work_Path)
            time.sleep(0.1)
        for name, url in video_dict.items():
            collect_info(name, url, work_Path)
            time.sleep(0.1)
        for name, url in movie_dict.items():
            collect_info(name, url, work_Path)
            time.sleep(0.1)


if __name__ == '__main__':
    import requests
    import bs4
    import re
    import logging, os, time
    logging.basicConfig(filename='D:\DataMiningCourse\\failLog.log', level=logging.DEBUG, filemode='w')
    main()