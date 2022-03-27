# coding = utf-8
import os
import requests
from fake_useragent import UserAgent

from components.headers import get_headers
from components.proxies import getProxies
from components.download import get_video_info, download_covers, download_videos, move_barrages
from arguments import bilibili_argparse

ua = UserAgent(use_cache_server=False, path="components/fake_useragent.json")

args = bilibili_argparse().parse_args()

if __name__ == "__main__":

    session = requests.Session()
    headers = get_headers(ua=ua)
    if args.use_proxy == True:
        proxies = getProxies(proxy=args.proxy, http=False, https=True)
    else:
        proxies = None
    
    if args.crawler_type == "up":
        args.ajax_url = "https://api.bilibili.com/x/space/arc/search?"
    elif args.crawler_type == "favorite":
        args.ajax_url = "https://api.bilibili.com/x/v3/fav/resource/list?"
        args.video_class = "Favorite"

    video_list, args.up_loader = get_video_info(args, session=session, headers=headers, proxies=proxies)
    print('args.up_loader:', args.up_loader)

    args.save_path = os.path.join(args.save_path, args.video_class)
    args.video_path = os.path.join(args.save_path, args.up_loader, 'videos')
    args.audio_path = os.path.join(args.save_path, args.up_loader, 'audios')
    args.cover_path = os.path.join(args.save_path, args.up_loader, 'covers')
    args.barrage_path = os.path.join(args.save_path, args.up_loader, 'barrages')
    for path in [args.video_path, args.audio_path, args.cover_path, args.barrage_path]:
        if not os.path.exists(path):
            os.makedirs(path)


    """下载封面"""
    # download_covers(args, video_list=video_list, session=session, headers=headers, proxies=proxies)


    """下载视频"""
    download_videos(args, video_list=video_list)
    move_barrages(args)
    
