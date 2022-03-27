# Crawler-BiliBili
A crawler project for BiliBili video site based on [you-get](https://github.com/soimort/you-get).

- 本项目基于you-get包批量爬取Bilibili视频，目前可以实现爬取up主稿件列表以及具有公开权限的收藏夹；
- 项目依赖：
  - python >= 3.5
  - you-get
  - ffmpeg
- up主mid可在网站获取，收藏夹media_id通过检查ajax页面得到

<center>
<img style="border-radius: 0.3125em;
box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
width="80%"
src="./images/ajax.png">
<br>
<div style="color:orange; display: inline-block; color: black; padding: 2px;">检查ajax页面</div>
</center>
