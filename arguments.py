import time
import argparse

local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def bilibili_argparse():
    parser = argparse.ArgumentParser()

    # Basic Information
    parser.add_argument('--user', default='yuhong', type=str)
    parser.add_argument('--date', default=local_time.split(' ')[0], type=str)
    parser.add_argument('--time', default=local_time.split(' ')[1].replace(':', '-'), type=str)
    parser.add_argument('--description', default='Download videos from bilibili.com!', type=str)

    # Definition Information
    parser.add_argument('--save_path', default="E:\Videos\Collections\BiliBili", type=str)
    parser.add_argument('--crawler_type', default="up", choices=['up', 'favorite'], type=str, help="爬取方式，up主稿件(up)或者收藏夹(favorite)，爬取的收藏夹需要权限公开")
    parser.add_argument('--video_class', default="Dance", type=str, help="视频类型，up模式下决定本次爬取的保存目录，favorite模式下自动切换保存目录为'Favorite'")
    parser.add_argument('--video_url', default="https://www.bilibili.com/video/", type=str, help="视频链接")
    parser.add_argument('--ajax_url', default="https://api.bilibili.com/x/space/arc/search?", type=str, help="获取UP主视频列表的api链接")
    parser.add_argument('--downloaded_log_file', default="downloaded_videos.txt", type=str, help="记录已下载的视频")

    # Network Information
    parser.add_argument('--use_proxy', default=True, type=bool)
    parser.add_argument('--proxy', default='127.0.0.1:2021', type=str)
    parser.add_argument('--proxy_http', default=True, type=bool)
    parser.add_argument('--proxy_https', default=False, type=bool)

    # Download Information
    parser.add_argument('--up_loader', default="", type=str)
    parser.add_argument('--mid', default=15116573, type=int, help="up主的uid，主页链接末尾的数字，例如'https://space.bilibili.com/7552204'")
    parser.add_argument('--start_page_number', default=1, type=int, help="开始下载的视频列表页码")
    parser.add_argument('--ps', default=20, type=int, help="每页显示的视频数量")
    parser.add_argument('--tid', default=129, type=int, help="控制视频列表类别，比如全部(0)，舞蹈(129)，生活等，具体可在网站查看")
    parser.add_argument('--keyword', default='', type=str, help="关键词检索")
    parser.add_argument('--order', default='pubdate', type=str, help="视频排序方式，爬取up主稿件时'pubdate'表示最新时间排序，爬取收藏夹时''")
    parser.add_argument('--jsonp', default='jsonp', type=str)

    parser.add_argument('--media_id', default=1315457945, type=int, help="收藏夹的id，例如我的收藏夹中Dance(1306336245)，Music(1315457945)")
    parser.add_argument('--type', default=0, type=int)
    parser.add_argument('--platform', default='web', type=str)

    return parser
