import locale
import os
import sys
import re
import httpx
import requests
from language import LanguageFormatter

global lformat
lformat = LanguageFormatter(locale.getlocale())

class CLI:
    def __init__(self, cmd: list):
        self.command = cmd
        self.author = "thisCarbondoXD, forCarbondoXD-Organizations of Github"
        self.version = "20230818AFT.GITHUB"
        self.description = """"""
        self.changelog = f"""CHANGELOG {self.version}
            Changed the url, add demo CLI, add authpass detect, add more-language-support(Thanks for yours translations!)
        """

    def parse(self):
        cmd = self.command
        if cmd[0] == "-m":
            cmd.pop(0)
        elif cmd[0] == "-h":
            self.print_usage()
        elif cmd[0][:1] == "-":
            self.print_usage()
        try:
            parsed_url = cmd[0]
        except:
            self.print_usage()
            exit(5)
        try:
            parsed_save_path = cmd[1]
        except:
            parsed_save_path = "./"
        try:
            parsed_ffmpeg2mp4 = True if cmd[3] == "true" else False
        except:
            parsed_ffmpeg2mp4 = True

        mymut = Muttertube(
            extra_url=extra_url(parsed_url),
            base_home=parsed_save_path,
            ffmpeg2mp4=parsed_ffmpeg2mp4,
            videotitle_asfiletitle=True
        )
        indexm3u8 = mymut.m3u8_get("index.m3u8")
        mymut.m3u8_index(indexm3u8)


    def print_usage(self):
        print(f"""MurrtubeDownloaderPy({self.author}) {self.version} \n{self.description} \n{self.changelog} \n Help usage: (Last edit ) MurrtubeDownloaderPy <url> <@Nullable save_path | default = "./"> <@Nullable ffmpeg2mp4 | default = "true"> """)


class Downloader:
    @staticmethod
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
    def __init__(self, base_home: str, storage_path=None, extra_url: list = None, ffmpeg2mp4: bool = True,
                 videotitle_asfiletitle: bool = True):
        self.index_m3u8 = "index.m3u8"
        self.base_home = base_home + "/"
        self.storage_url = "https://storage.murrtube.net/murrtube-production/"
        self.ffmpeg2mp4 = ffmpeg2mp4
        self.videotitle_asfiletitle = videotitle_asfiletitle
        if storage_path is not None:
            self.storage_path = storage_path + "/"
            self.aioname = f"""{self.base_home}/{self.storage_path.replace("/", "")}"""
        elif extra_url is not None:
            self.storage_path = extra_url[0].split("?")[0].replace("https://storage.murrtube.net/murrtube-production/",
                                                                   "").replace(
                "http://storage.murrtube.net/murrtube-production/", "").replace("thumbnail.jpg", "").replace(" ", "")
            if videotitle_asfiletitle is None:
                self.aioname = extra_url[1].replace("https://murrtube.net/v", "").replace("/", "")
            else:
                self.aioname = extra_url[2]["video_title"]
        else:
            raise Exception(lformat.lang("exception.unknown_select"))

    def m3u8_get(self, what):
        urla = f"{self.storage_url}{self.storage_path}{what}"
        print(f"""{lformat.lang("m3u8_analyzing_url")}: {urla}""")
        return requests.get(urla).text

    def m3u8_index(self, content: str):
        contentf = content.split("\n")
        if "#EXTM3U" == contentf[0]:
            contentf.pop(0)
        else:
            raise Exception(lformat.lang("exception.m3u8.formatter.wrong_extension.noextm3u").format(contentf=contentf))
        while 1:
            try:
                contentf.pop(contentf.index(""))
            except:
                break
        print(lformat.lang("select.quality.download"))
        contentl = []
        for i in range(0, len(contentf), 2):
            contentl.append(contentf[i + 1])
            print(f"{int(i / 2)}: {contentf[i + 1]}")
        which_download = int(input(": "))
        self.download_method_which_download(contentl, which_download)

    def download_method_which_download(self, contentl, which_download):
        try:
            assd = f"{self.storage_url}/{self.storage_path}/{contentl[which_download]}"
            print(assd)
            ctld = requests.get(assd).text
            self.m3u8_video_d(ctld)
        except:
            raise Exception(
                f"""{lformat.lang("exception.m3u8.index.out_of_range")} {which_download}/{len(contentl)}""")

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
            raise Exception(lformat.lang("exception.m3u8.formatter.wrong_extension.noextm3u").format(contentf=ccrf))
        ccrl = []
        for i in range(0, len(ccrf), 2):
            ccrl.append(ccrf[i + 1])
        print(lformat.lang("download.info.file_count").format(file_count=len(ccrl)))
        print(ccrl)
        # 检测目录创建情况

        if not os.path.exists(f"{self.base_home}/{self.aioname}"):
            os.mkdir(f"{self.base_home}/{self.aioname}")
        down_url = "{}/{}/{}"
        #
        print(lformat.lang("select.download_method"))
        self.download_method_part_download(int(input(": ")), ccrl, down_url)

    def download_method_part_download(self, select: int, ccrl, down_url):
        if select == 0:
            print(lformat.lang("select.download_method.part_download"))
            self.thumbnail_d(f"{self.base_home}/{self.aioname}")
            for d in range(0, len(ccrl)):
                #     downloader.Downloader(url=down_url.format(self.storage_url, self.storage_path, ccrl[d]), file_path=f"{downpath}/{ccrl[d]}").start()
                fileg = f"{self.aioname}/{ccrl[d]}"
                with open(fileg, "wb") as f:
                    dl = down_url.format(self.storage_url, self.storage_path, ccrl[d])
                    print(f"""{d + 1}/{len(ccrl)} | {lformat.lang("download.info.downloading")}: {dl}""")
                    req = requests.get(dl).content
                    f.write(req)
                    f.flush()
                    f.close()
                self.ffmpeg4if(f"{self.aioname}/{ccrl[d]}")
        else:
            self.thumbnail_d(f"{self.base_home}/{self.aioname}")
            aiofn = f"{self.base_home}/{self.aioname}/" + self.aioname + ".ts"
            print(f"""{lformat.lang("download.info.try_to_download_to")}: {aiofn}""")
            print(f"""{lformat.lang("download.info.try_to_merge_file_to")}: {aiofn}""")
            with open(aiofn, "wb") as aio:
                for d in range(0, len(ccrl)):
                    # downloader.Downloader(url=down_url.format(self.storage_url, self.storage_path, ccrl[d]),
                    # file_path=f"{downpath}/{ccrl[d]}").start()
                    dl = down_url.format(self.storage_url, self.storage_path, ccrl[d])
                    print(
                        f"""{lformat.lang("download.info.block_downloading").format(block=f"{d + 1}/{len(ccrl)}", dl=dl)}""")
                    req = requests.get(dl).content
                    aio.write(req)
            self.ffmpeg4if(aiofn)

    def ffmpeg4if(self, inf):
        inf = os.path.abspath(inf)
        print(f"""[FFMPEG4IF] {lformat.lang("ffmpeg4if.info.running")}:{inf.replace(".ts", ".mp4")}""")
        if self.ffmpeg2mp4 is not False:
            import ffmpy
            try:
                inff = ffmpy.FFmpeg(
                    inputs={inf: None},
                    outputs={inf.replace(".ts", ".mp4"): None}
                )
                inff.run()
                print(f"""[FFMPEG4IF] {lformat.lang("ffmpeg4if.info.finish")}""")
            except Exception as err:
                print(f"""[FFMPEG4IF] {lformat.lang("ffmpeg4if.err.convert_err").format(err=err)}""")

    def thumbnail_d(self, downpath):
        thumbnailu = f"""{downpath}/thumbnail.jpg"""
        print(f"""{lformat.lang("download.info.downloading_thumbnail")}: {thumbnailu}...""")
        tb = open(thumbnailu, "wb")
        tb.write(requests.get(f"{self.storage_url}/{self.storage_path}/thumbnail.jpg").content)
        tb.flush()
        tb.close()


def extra_url(url):
    """<img loading="lazy" alt="" src="">"""
    global authenticity_token, csrf_token, video_title
    uca = requests.get(url)
    uca_cookie = uca.cookies
    uc = uca.text
    # 未成年绕过，获得Token
    match = re.search(r'name="authenticity_token" value="([^"]+)"', uc)
    if match:
        authenticity_token = match.group(1)
    else:
        print(lformat.lang("extra_url.notfound.authenticity_token"))

    matchaa = re.search(r'meta name="csrf-token" content="([^"]+)"', uc)
    if matchaa:
        csrf_token = matchaa.group(1)
    else:
        print(lformat.lang("extra_url.notfound.csrf_token"))

    matchab = re.search(r'<title>([^"]+)</title>', uc)
    if matchab:
        video_title = matchab.group(1).replace(" - Murrtube", "").replace(" ", "_")
    else:
        print(lformat.lang("extra_url.notfound.video_title_element"))

    try:
        authenticity_token_postdata = {"authenticity_token": authenticity_token}
    except:
        print(lformat.lang("extra_url.notfound.authenticity_token.connect"))
        return getSrcMatched(url, uca_cookie, {"video_title": video_title})

    authenticity_token_posthead = {"X-Csrf-Token": csrf_token}
    print(f"""{lformat.lang("extra_url.process.build_header")}：{authenticity_token_postdata}""")
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
        print(lformat.lang("extra_url.process.request.ok_may_without_header"))
        if response.text == """<html><body>You are being <a href="https://murrtube.net/">redirected</a>.</body></html>""":
            print(lformat.lang("extra_url.process.request.ok.redirect"))
    else:
        print(lformat.lang("extra_url.process.request.err").format(err={response.status_code}))

    AAC_BYPASS_COOKIES = response.cookies
    # 给主页发送请求咯
    return getSrcMatched(url, AAC_BYPASS_COOKIES, {"video_title": video_title})


def getSrcMatched(url, AAC_BYPASS_COOKIES, something_with):
    MAINP = requests.get(url, cookies=AAC_BYPASS_COOKIES)
    src_match = re.findall(r'poster="([^"]+)"', MAINP.text)[0]
    return [src_match, url, something_with]


def murrtube_setting(base_home, ffmpeg2mp4: bool):
    mymut = Muttertube(
        # storage_path=input("VideoPath(e.g.: /c02/xxxxxxxxxxxxxxxx/): "),
        extra_url=extra_url(input("VideoPath(e.g.: https://murrtube.net/v/...): ")),
        base_home=base_home,
        ffmpeg2mp4=ffmpeg2mp4,
        videotitle_asfiletitle=True
    )
    indexm3u8 = mymut.m3u8_get("index.m3u8")
    mymut.m3u8_index(indexm3u8)


if __name__ == '__main__':
    murrtube_setting(base_home="./", ffmpeg2mp4=True)
else:
    CLI(sys.argv).parse()
