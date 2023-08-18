import locale
import os

if __name__ == "__main__":
    if os.getcwd().split("/")[-1] != "language":
        print("Your work dictionary must in .../language")
        exit(10)
    locale = locale.getdefaultlocale()
    if os.path.exists(locale[0]) is False:
        file_name = f"{locale[0]}.lang"
        encoding_code = locale[1]
        locale_name = locale[0]

        ff = open(file_name, "w+", encoding=encoding_code)
        ff.write("""
        {
            "exception.unknown_select": "Unknown Select",
            "exception.m3u8.formatter.wrong_extension.noextm3u": "{contentf}\\nIndex.m3u8 Formatter @ Wrong Extension: Without #EXTM3U",
            "exception.m3u8.index.out_of_range": "M3U8_Index @ Out of Range",
            "m3u8_analyzing_url": "Analyzing: ",
            "select.quality.download": "Select the version(quality) to download: ",
            "download.info.file_count": "Download details: {file_count} files in total.",
            "select.download_method": "0.Segmented Download\\n1.Merge Download",
            "select.download_method.segmented_download": "Segmented Download: ",
            "select.download_method.merge_download": "Merge Download: ",
            "download.info.downloading": "Downloading",
            "download.info.try_to_download_to": "Merge files to download to",
            "download.info.try_to_merge_file_to": "Merge to merge files into",
            "download.info.block_downloading": "Block {block} | Downloading: {dl}",
            "ffmpeg4if.info.running": "Running: ",
            "ffmpeg4if.info.finish": "Finish.",
            "ffmpeg4if.err.convert_err": "Err, Couldn't Convert. {err}",
            "download.info.downloading_thumbnail": "Download Thumbnail: ",
            "extra_url.notfound.authenticity_token": "authenticity_token Not Found",
            "extra_url.notfound.csrf_token": "csrf_token Not Found",
            "extra_url.notfound.video_title_element": "video_title_element Not Found",
            "extra_url.notfound.authenticity_token.connect": "authenticity_token Not Found, Trying to connect server as authed as possible.",
            "extra_url.process.build_header": "Building request header",
            "extra_url.process.request.ok_may_without_header": "Request successful | Perhaps without return header",
            "extra_url.process.request.ok.redirect": "Redirect Success",
            "extra_url.process.request.err": "Request Error: {err}"
        }
        """)
        ff.flush()
        ff.close()
        print(f"Created File: {locale_name}, Encoding with: {encoding_code}")
    else:
        print(f"File is exists.")
