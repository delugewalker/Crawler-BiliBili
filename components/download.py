import os
import re
import json
import time
import shutil
# from components.headers import get_headers


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def get_video_info(args, session, headers, proxies):
    videoList = []

    pageNumber = args.start_page_number

    while True:
        if args.crawler_type == "up":
            params = {
            'mid': args.mid,
            'ps': args.ps,
            'tid': args.tid,
            'pn': pageNumber,
            'keyword': args.keyword,
            'order': args.order, 
            'jsonp': args.jsonp
            }
        elif args.crawler_type == "favorite":
            "media_id=1315457945&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp"
            params = {
            'media_id': args.media_id,
            'ps': args.ps,
            'pn': pageNumber,
            'keyword': args.keyword,
            'order': args.order, 
            'type': args.type,
            'tid': args.tid,
            'platform': args.platform,
            'jsonp': args.jsonp
            }
        else:
            raise EOFError("There is no such crawler type: {}!".format(args.crawler_type))

        page = session.get(url=args.ajax_url, params=params, headers=headers, proxies=proxies)
        # page.encoding = chardet.detect(page.content)['encoding']
        page.encoding = 'uft-8'
        page = page.text
        page = json.loads(page)

        if args.crawler_type == "up":
            if not page['data']['list']['tlist']:
                break
            videoList += page['data']['list']['vlist']
            authorName = page['data']['list']["vlist"][0]["author"]
        elif args.crawler_type == "favorite":
            if not page['data']['medias']:
                break
            videoList += page['data']['medias']
            authorName = page['data']['info']['title']   # 使用收藏夹名称做为文件夹名称

        pageNumber += 1

    return videoList, authorName


def download_covers(args, video_list, session, headers, proxies):
    for index, videoInfo in enumerate(video_list):

        if args.crawler_type == "up":
            title = videoInfo['title']
            title = validateTitle(title).strip()
            picUrl = videoInfo['pic']
        elif args.crawler_type == "favorite":
            title = videoInfo['title']
            title = validateTitle(title).strip()
            picUrl = videoInfo['cover']

        picExtentionName = picUrl[-4:]
        imgData = session.get(url=picUrl, headers=headers, proxies=proxies).content
        save_name = os.path.join(args.cover_path, title + picExtentionName)
        # save_name = os.path.join(coverPath, 'cnm.jpg')

        with open(save_name, 'wb') as fp:
            fp.write(imgData)
        print('Successfully save cover {}!'.format(title))


def download_videos(args, video_list):

    downloaded_videos_info_file = os.path.join(args.save_path, args.up_loader, args.downloaded_log_file)

    if not os.path.isfile(downloaded_videos_info_file):
        with open(downloaded_videos_info_file, 'w', encoding='utf-8') as f:
            f.close()
    
    for index, videoInfo in enumerate(video_list):
        """获取视频信息"""
        if args.crawler_type == "up":
            localTime = time.localtime(videoInfo['created'])
        elif args.crawler_type == "favorite":
            localTime = time.localtime(videoInfo['ctime'])
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        dateArray = timeArray[0:10]
        bvid = videoInfo['bvid']
        title = validateTitle(videoInfo['title'])

        """对比当前视频和已下载视频信息，若已经下载过，则跳过"""
        with open(downloaded_videos_info_file, 'r+', encoding='utf-8') as f:
            info = dateArray + "  " + bvid + "  " + title
            lines = [line.strip() for line in f.readlines()]
            if info in lines:
                continue
            else:
                f.write(info)
                f.write('\n')

        """下载视频"""
        os.chdir(args.video_path)
        video_url = args.video_url + bvid
        if not args.use_proxy:
            os.system("you-get --playlist " + str(video_url))
        else:
            os.system("you-get " + "-s" + args.proxy + " --playlist " + str(video_url))  # 使用代理
        print('Successfully download bilibili video {}!'.format(bvid))
        os.chdir(args.save_path)


def move_barrages(args):
    print(args.video_path)
    for file in os.listdir(args.video_path):
        if file[-3:] == 'xml':
            oldName = os.path.join(args.video_path, file)
            newName = os.path.join(args.barrage_path, file)
            shutil.move(oldName, newName)