import os
import re
import httpx

import requests


class Downloader:
    def split_list(lst):
        n = len(lst)
        num_lists = 10
        quotient = n // num_lists
        remainder = n % num_lists

        result = []
        start = 0
        for i in range(num_lists):
            sublist_length = quotient + (1 if i < remainder else 0)
            sublist = lst[start:start + sublist_length]
            result.append(sublist)
            start += sublist_length

        return result


class Muttertube:
    def __init__(self, base_home: str, storage_path=None, extra_url:list=None):
        self.index_m3u8 = "index.m3u8"
        self.base_home = base_home + "/"
        self.storage_url = "https://storage.murrtube.net/murrtube-production/"
        if storage_path is not None:
            self.storage_path = storage_path + "/"
            self.aioname = f"""{self.base_home}/{self.storage_path.replace("/", "")}"""
        elif extra_url is not None:
            self.storage_path = extra_url[0].split("?")[0].replace("https://storage.murrtube.net/murrtube-production/", "").replace("thumbnail.jpg", "")
            self.aioname = extra_url[1].replace("https://murrtube.net/videos", "").replace("/", "")
        else:
            raise Exception("Unknown Select")

    def m3u8_get(self, what):
        urla = f"{self.storage_url}{self.storage_path}{what}"
        print(f"解析中: {urla}")
        return requests.get(urla).text

    def m3u8_index(self, content: str):
        contentf = content.split("\n")
        if "#EXTM3U" == contentf[0]:
            contentf.pop(0)
        else:
            raise Exception(f"{contentf}\nIndex.m3u8 Formatter @ Wrong Extension: No #EXTM3U")
        print("选择需要的版本（画质区别）下载：")
        contentl = []
        for i in range(0, len(contentf), 2):
            contentl.append(contentf[i + 1])
            print(f"{int(i / 2)}: {contentf[i + 1]}")
        which_download = int(input(": "))
        try:
            assd = f"{self.storage_url}/{self.storage_path}/{contentl[which_download]}"
            print(assd)
            ctld = requests.get(assd).text
            self.m3u8_video_d(ctld)
        except:
            raise Exception(f"Sorry, M3U8_Index @ Out of Range, {which_download}/{len(contentl)}")

    def m3u8_video_d(self, ccr: str):
        ccrf = ccr.split("\n")
        if "#EXTM3U" == ccrf[0]:
            for p in range(0, 4):
                """
                    #EXTM3U
                    #EXT-X-VERSION
                    #EXT-X-TARGETDURATION
                    #EXT-X-MEDIA-SEQUENCE
                """
                ccrf.pop(0)
            for p in range(0, 2):
                """
                    '#EXT-X-ENDLIST',
                    ''
                """
                ccrf.pop(-1)
        else:
            raise Exception(f"{ccrf}\nIndex.m3u8 Formatter @ Wrong Extension: No #EXTM3U")
        ccrl = []
        for i in range(0, len(ccrf), 2):
            ccrl.append(ccrf[i + 1])
        print(f"下载详情：共 {len(ccrl)} 个文件")
        print(ccrl)
        # 检测目录创建情况

        if not os.path.exists(self.aioname): os.mkdir(self.aioname)
        down_url = "{}/{}/{}"
        #
        print(f"""0.分段下载\n1.合并下载""")
        if int(input(": ")) == 0:
            print("分段下载: ")
            self.thumbnail_d(self.aioname)
            for d in range(0, len(ccrl)):
                #     downloader.Downloader(url=down_url.format(self.storage_url, self.storage_path, ccrl[d]), file_path=f"{downpath}/{ccrl[d]}").start()
                with open(f"{self.aioname}/{ccrl[d]}", "wb") as f:
                    dl = down_url.format(self.storage_url, self.storage_path, ccrl[d])
                    print(f"{d} | 下载中: {dl}")
                    req = requests.get(dl).content
                    f.write(req)
                    f.flush()
                    f.close()
        else:
            self.thumbnail_d(self.aioname)
            aiofn = self.base_home+"/"+self.aioname + ".mp4"
            print(f"合并文件下载到: {self.base_home}/{aiofn}")
            print(f"尝试合并文件到 {self.base_home}/{aiofn}")
            with open(aiofn, "wb") as aio:
                for d in range(0, len(ccrl)):
                    # downloader.Downloader(url=down_url.format(self.storage_url, self.storage_path, ccrl[d]),
                    # file_path=f"{downpath}/{ccrl[d]}").start()
                    dl = down_url.format(self.storage_url, self.storage_path, ccrl[d])
                    print(f"块 {d} | 下载中: {dl}")
                    req = requests.get(dl).content
                    aio.write(req)

    def thumbnail_d(self, downpath):
        thumbnailu = f"""{downpath}/thumbnail.jpg"""
        print(f"下载封面: {thumbnailu}...")
        tb = open(thumbnailu, "wb")
        tb.write(requests.get(f"{self.storage_url}/{self.storage_path}/thumbnail.jpg").content)
        tb.flush()
        tb.close()


def extra_url(url):
    """<img loading="lazy" alt="" src="">"""
    global authenticity_token, csrf_token
    uca = requests.get(url)
    uca_cookie = uca.cookies
    uc = uca.text
    # 未成年绕过，获得Token
    match = re.search(r'name="authenticity_token" value="([^"]+)"', uc)
    if match:
        authenticity_token = match.group(1)
    else:
        print("未找到 authenticity_token")

    matchaa = re.search(r'meta name="csrf-token" content="([^"]+)"', uc)
    if matchaa:
        csrf_token = matchaa.group(1)
    else:
        print("未找到 csrf_token")

    authenticity_token_postdata = {"authenticity_token": authenticity_token}
    authenticity_token_posthead = {"X-Csrf-Token": csrf_token}
    print(f"组装请求头：{authenticity_token_postdata}")
    headers = {
        "Host": "murrtube.net",
        "Sec-Ch-Ua": '"Not;A=Brand";v="99", "Chromium";v="106"',
        "Accept": "text/vnd.turbo-stream.html, text/html, application/xhtml+xml",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-Csrf-Token": f"{csrf_token}",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/106.0.5249.91 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://murrtube.net",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://murrtube.net/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    response = httpx.post("https://murrtube.net/accept_age_check", headers=headers, data=authenticity_token_postdata,
                          cookies=uca_cookie)

    if response.status_code == 200 or response.status_code == 302:
        print("请求成功 | 也许无返回头")
        if response.text == """<html><body>You are being <a href="https://murrtube.net/">redirected</a>.</body></html>""":
            print("重定向..OK!")
    else:
        print(f"请求失败: {response.status_code}")

    AAC_BYPASS_COOKIES = response.cookies
    # 给主页发送请求咯
    MAINP = requests.get(url, cookies=AAC_BYPASS_COOKIES)
    src_match = re.findall(r'poster="([^"]+)"', MAINP.text)[0]
    return [src_match, url]


def mutterbate_setting(base_home):
    mymut = Muttertube(
        # input("VideoPath(e.g.: /c02/xxxxxxxxxxxxxxxx/): "),
        extra_url=extra_url(input("VideoPath(e.g.: https://murrtube.net/videos/...): ")),
        base_home=base_home
    )
    indexm3u8 = mymut.m3u8_get("index.m3u8")
    mymut.m3u8_index(indexm3u8)


if __name__ == '__main__':
    mutterbate_setting(base_home=".\downloaded")
