import os
import re
import time

def audioExtract(videoPath, videoName, audioPath, sourceFormat='flv', targetFormat='mp3'):
    videoFile = os.path.join(videoPath, videoName)
    videoFile = '"' + videoFile + '"'
    audioFile = os.path.join(audioPath, videoName.replace(sourceFormat, targetFormat))
    audioFile = '"' + audioFile + '"'

    """此处根据具体格式和编码，修改ffmpeg命令！"""
    order = 'ffmpeg -i ' + videoFile + ' -y -vn -ab 320k ' + audioFile

    os.system(order)


def convertFormat(videoPath, videoName, sourceFormat='flv', targetFormat='mp4'):
    videoFile = os.path.join(videoPath, videoName)
    videoFile = '"' + videoFile + '"'
    newAudioFile = videoFile.replace(sourceFormat, targetFormat)

    """此处根据具体格式和编码，修改ffmpeg命令！"""
    order = 'ffmpeg -i ' + videoFile + ' -y -codec copy ' + newAudioFile

    os.system(order)


def audioCoverEmbed(audioPath, audioName, picPath, picName):
    audioFile = os.path.join(audioPath, audioName)
    oldName = audioFile
    audioFile = '"' + audioFile + '"'
    picFile = os.path.join(picPath, picName)
    picFile = '"' + picFile + '"'

    newaudioFile = os.path.join(audioPath, 'new_' + audioName)
    newName = newaudioFile
    newaudioFile = '"' + newaudioFile + '"'

    argument1 = ' -map 0:0 -map 1:0 -c copy -id3v2_version 3 '
    # argument2 = ' -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" '
    argument2 = ' '

    order = 'ffmpeg -i ' + audioFile + ' -i ' + picFile + argument1 + argument2 + newaudioFile

    os.system(order)
    os.remove(oldName)
    time.sleep(0.1)
    os.rename(newName, oldName)


def videoCoverEmbed(videoPath, videoName, picPath, picName):
    videoFile = os.path.join(videoPath, videoName)
    videoFile = '"' + videoFile + '"'
    picFile = os.path.join(picPath, picName)
    picFile = '"' + picFile + '"'

    newVideoPath = videoPath.split('\\')
    newVideoPath[-1] = newVideoPath[-1] + '_covered'
    newVideoPath = '\\'.join(newVideoPath)
    if not os.path.exists(newVideoPath):
        os.mkdir(newVideoPath)

    newVideoFile = os.path.join(newVideoPath, videoName)
    newVideoFile = '"' + newVideoFile + '"'

    argument = ' -map 0 -map 1 -c copy -c:v:1 png -disposition:v:1 attached_pic '

    order = 'ffmpeg -i ' + videoFile + ' -i ' + picFile + argument + newVideoFile
    print(order)
    os.system(order)


def renameFile(filePath, fileName, upLoader):
    pat = re.compile(pattern='《(.*?)》')
    newFileName = re.findall(pattern=pat, string=fileName)
    if len(newFileName) == 0:
        return

    newFileName = newFileName[0] + ' - ' + upLoader + fileName[-4:]

    oldName = os.path.join(filePath, fileName)
    newName = os.path.join(filePath, newFileName)

    os.rename(oldName, newName)