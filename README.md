# __Murrtube Downloader for Python 3.10__

![GitHub](https://img.shields.io/github/license/forCarbondoXD/MurrtubeDownloaderPy)
![GitHub stars](https://img.shields.io/github/stars/forCarbondoXD/MurrtubeDownloaderPy)
![GitHub forks](https://img.shields.io/github/forks/forCarbondoXD/MurrtubeDownloaderPy)
![GitHub issues](https://img.shields.io/github/issues/forCarbondoXD/MurrtubeDownloaderPy)

## 📕 简介 | Description

这是一个工具用来下载网站 _murrtube.net_[^website] 的视频内容，项目开源且遵循 __Murrtube__ 的协议；请合理使用，作为开源开发者，我不会承担任何法律行为！
<br>This is a tool designed for downloading video content from _murrtube.net_ , project is opensource and adheres to license of __Murrtube__; Use it in legal and responsibly, as a opensource developer, I will not take any result of yours ilegal using.

## 📦 部署 | Deploy

> [!IMPORTANT]
> 使用这个Python脚本，需要你使用 __Python 3.10+__ 进行操作；推荐你先创建一个虚拟环境用来执行
>   
> Use this Python script, you need __Python 3.10+__; Create a virtual environment to run script if you like

```
# 创建一个虚拟环境 | Create a virtual env
python3 -m venv <your_virtual_env_name>

# 打开虚拟环境 | Use the virtual env
. <your_virtual_env_name>/scripts/activate

# 安装依赖 | Install Requirements
python3 -m pip install -r requirements.txt

# 打开 | Enjoy it
python3 MurrtubeDownloaderPy.py
```

## 🧾 许可证 | License
> [!CAUTION]
> 我们仍然不清楚 __Murrtube__ 使用的协议，所以我们将使用项目自己的协议！
>
> We still don't know what license is __Murrtube__ using, so we use our license!

> [!NOTE]
> __branch$230818_urlfix__: Outer Support -> ffmpeg licenses[^ffmpeg_lic]

## ⬆️ 更新内容 | Updated Content of This Branch

由于Murrtube的x/video/x变成了x/v/x，随着更改了。
<br />
Changed Murrtube x/video/x to x/v/x
<br />
<br />
新添加了CLI
<br />
Support CLI
<br />
<br />
```shell
<python_executable> -m MurrtubeDownloaderPy <url> <part/merge> <@Nullable save_path | default = "./"> <@Nullable ffmpeg2mp4 | default = "true">

或者(or)
使用这个获取帮助(Execute it for help)

<python_executable> -m MurrtubeDownloaderPy -h
```
<br />
<br />
__需要在PATH中设置有ffmpeg，需要安装ffmpeg 、 可以选择无ffmpeg版本__
__It is necessary to set ffmpeg in the PATH, install ffmpeg, or choose a version without ffmpeg__

[^website]: [Murrtube Website](https://murrtube.net)
[^ffmpeg_lic]: [GNU Lesser General Public License (LGPL)](https://www.gnu.org/licenses/#LGPL), [GNU General Public License (GPL)](https://www.gnu.org/licenses/#GPL)
