import os
import re
import difflib
import requests
from arguments import bilibili_argparse
from components.danmaku2ass import Danmaku2ASS
from components.process import *
from components.headers import get_headers
from components.proxies import getProxies
from components.download import get_video_info, download_covers, download_videos
from arguments import bilibili_argparse

from fake_useragent import UserAgent
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


    """格式转换，音频提取"""
    # for videoName in sorted(os.listdir(args.video_path)):
    #     if videoName[-3:] == 'mp4':
    #         videoFile = os.path.join(args.video_path, videoName)
    #         audioFile = os.path.join(args.audio_path, videoName)

    #         # convertFormat(args.video_path, videoName, sourceFormat='flv', targetFormat='mp4')  # 视频格式转换
    #         audioExtract(args.video_path, videoName, args.audio_path, sourceFormat='mp4', targetFormat='mp3')  # 从视频提取音频
            

    """音频封面嵌入"""
    # for audioName in sorted(os.listdir(args.audio_path)):
    #     print('audioName:', audioName)
    #     flag = False
    #     pattern = re.compile('\(P\d\.|P\d\.')
    #     if audioName[-3:] == 'mp3':
    #         # coverName = audioName.replace('.mp3', '.jpg')
    #         coverName = re.split(pattern, audioName)[0].strip() + '.jpg'
    #         print('coverName:', coverName)
    #         for existCoverName in sorted(os.listdir(args.cover_path)):
    #             if difflib.SequenceMatcher(None, coverName, existCoverName).quick_ratio() > 0.85:
    #                 audioCoverEmbed(audioPath=args.audio_path, audioName=audioName, picPath=args.cover_path, picName=existCoverName)
    #                 flag = True
    #                 break
    #             else:
    #                 continue
    #         if not flag:
    #             with open(os.path.join(args.save_path, 'coverNotFound.txt'), 'a+', encoding='utf-8') as f:
    #                 f.write(coverName + '\n')


    """视频封面嵌入"""
    for videoName in sorted(os.listdir(args.video_path)):
        print(videoName)
        flag = False
        pattern = re.compile('\(P\d\.|P\d\.')
        if videoName[-3:] == 'mp4' or 'flv':
            coverName = re.split(pattern, videoName)[0].strip() + '.jpg'
            for existCoverName in sorted(os.listdir(args.cover_path)):
                if difflib.SequenceMatcher(None, coverName, existCoverName).quick_ratio() > 0.85:
                    # print('coverName:', coverName)
                    # print('existCoverName', existCoverName)
                    videoCoverEmbed(videoPath=args.video_path, videoName=videoName, picPath=args.cover_path, picName=existCoverName)
                    flag = True
                    break
                else:
                    continue
            if not flag:
                with open(os.path.join(args.save_path, args.up_loader, 'coverNotFound.txt'), 'a+', encoding='utf-8') as f:
                    f.write(coverName + '\n')

    """弹幕文件转换(xml -> ass)"""
    # for barrageName in sorted(os.listdir(args.barrage_path)):
    #     if barrageName[-3:] == 'xml':
    #         barrageFile = os.path.join(args.barrage_path, barrageName)
    #         outputbarrageFile = barrageFile.replace('.xml', '.ass')
    #         Danmaku2ASS(input_files=barrageFile, input_format='autodetect', output_file=outputbarrageFile,
    #                     stage_width=1920, stage_height=1080, reserve_blank=0, font_face="sans-serif",
    #                     font_size=48.0, text_opacity=1.0, duration_marquee=15.0, duration_still=5.0,
    #                     comment_filter=None, comment_filters_file=None, is_reduce_comments=False,
    #                     progress_callback=None)
