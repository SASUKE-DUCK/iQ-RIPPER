#https://github.com/jym66/Dlink_Parse/blob/master/iqiyi.py
#https://github.com/wayneclub/Subtitle-Downloader
import logging
import coloredlogs
import json
import requests
from bs4 import BeautifulSoup
import http.cookiejar
import os
import subprocess
from hashlib import md5
from time import time
import shutil
from urllib.parse import urlencode
import re
import argparse
import execjs

parser = argparse.ArgumentParser(description="Fetch video information from a given URL")
parser.add_argument("-i", "--url", required=True, help="URL of the video episode")
args = parser.parse_args()

# Define paths and directories
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_path = os.path.join(current_dir, "temp")
downloads_path = os.path.join(current_dir, "downloads")
subtitles_path = os.path.join(current_dir, "subtitles")
if not os.path.exists(subtitles_path):
    os.mkdir(subtitles_path)
# Change the current working directory
os.chdir(current_dir)

# Configure logging
LOG_FORMAT = "{asctime} [{levelname[0]}] {name} : {message}"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_STYLE = "{"

logger = logging.getLogger("iQ")
coloredlogs.install(level="INFO", fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, style=LOG_STYLE)

# Configure session and cookies
session = requests.Session()
cookie_jar = http.cookiejar.MozillaCookieJar()
cookie_jar.load("iq_cookies.txt")
session.cookies = cookie_jar
cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}
uid = cookie_dict.get('P00003', '0')

# Make a request to a web page
response = session.get(args.url)
soup = BeautifulSoup(response.text, 'html.parser')

data_pb = soup.find('a', class_='btn play')['data-pb']
album_id = data_pb.split('=')[-1]

headers = {
    'origin': 'https://www.iq.com',
    'referer': 'https://www.iq.com/',
    'user-agent': 'QYPlayer/Android/4.7.2201;BT/mcto;Pt/TV;NetType/wifi;Hv/10.2.3.1803;QTP/2.2.59.5',
}

params = {
    'platformId': 3,
    'modeCode': 'pe',
    'langCode': 'en_us',
    'deviceId': '21fcb553c8e206bb515b497bb6376aa4',
    'endOrder': 6,
    'startOrder': 1,
}

episode_list_url = f'https://pcw-api.iq.com/api/episodeListSource/{album_id}'

response_episode = session.get(url=episode_list_url, headers=headers, params=params, timeout=5)
data = json.loads(response_episode.text)
albumName = None
subtitles = []
languages = set()

# Iterate through the episodes
for episode in data.get("data", {}).get("epg", []):
    playLocSuffix = episode.get("playLocSuffix")
    albumName = episode.get("albumName")
    response_episode = session.get(f'https://www.iq.com/play/{playLocSuffix}', headers=headers, timeout=5)
    response = requests.get(f'https://www.iq.com/play/{playLocSuffix}', headers=headers, timeout=5)
    html_content = response.text if response.status_code == 200 else ''
    soup = BeautifulSoup(html_content, 'html.parser')
    span_order_info_element = soup.find('span', {'style': 'display:none', 'id': 'h5OrderInfo'})
    title_episode = span_order_info_element.text if span_order_info_element else ''
    if response_episode.status_code == 200:
        html_content = response_episode.text
        tv_id_match = re.search(r'"tvId":(\d+),\s*', html_content)
        if tv_id_match:
            tv_id = tv_id_match.group(1)
        vid_match = re.search(r'"m3u8Url":"",\s*"vid":"([a-f0-9]+)"', html_content)

        if vid_match:
            vid = vid_match.group(1)
        else:
            script_tag = soup.find('script', id='__NEXT_DATA__')
            data = json.loads(script_tag.string) if script_tag else {}
            vid = data.get("props", {}).get("initialState", {}).get("play", {}).get("curVideoInfo", {}).get("vid", "No se encontró el valor de 'vid'")
        text = f"d41d8cd98f00b204e9800998ecf8427e{int(time() * 1000)}{tv_id}"
        md = md5()
        md.update(text.encode())
        auth_key = md.hexdigest()
        tm = int(time() * 1000)

        params_hevc = {
            "tvid": tv_id,
            "bid": "600",
            "vid": vid,
            "src": "01011021010010000000",
            "vt": "0",
            "rs": "1",
            "uid": cookie_dict.get('P00003', '0'),
            "ori": "pcw",
            "ps": "0",
            "k_uid": cookie_dict.get('QC005', ''),
            "pt": "0",
            "d": "0",
            "s": "",
            "lid": "",
            "slid": "0",
            "cf": "",
            "ct": "",
            "authKey": auth_key,
            "k_tag": "1",
            "ost": "0",
            "ppt": "0",
            "dfp": cookie_dict.get('__dfp', ''),
            "locale": "zh_cn",
            "k_err_retries": "0",
            "qd_v": "2",
            "tm": int(time() * 1000),
            "qdy": "a",
            "qds": "0",
            "prio": '{"ff":"","code":}',
            "k_ft2": "8191",
            "k_ft1": "143486267424900",
            "k_ft4": "1581060",
            "k_ft7": "4",
            "k_ft5": "1",
            'bop': f'{{"version":"10.0","dfp":{cookie_dict.get("__dfp", "")},"b_ft1":0}}',
            "ut": "1",
        }
        params_avc = {
            "tvid": tv_id,
            "bid": "600",
            "vid": vid,
            "src": "01011021010010000000",
            "vt": "0",
            "rs": "1",
            "uid": cookie_dict.get('P00003', '0'),
            "ori": "pcw",
            "ps": "0",
            "k_uid": cookie_dict.get('QC005', ''),
            "pt": "0",
            "d": "0",
            "s": "",
            "lid": "",
            "slid": "0",
            "cf": "",
            "ct": "",
            "authKey": auth_key,
            "k_tag": "1",
            "ost": "0",
            "ppt": "0",
            "dfp": cookie_dict.get('__dfp', ''),
            "locale": "zh_cn",
            "k_err_retries": "0",
            "qd_v": "2",
            "tm": int(time() * 1000),
            'prio': '{"ff":"f4v","code":2}',
            "qd_v": "2",
            'su': '2',
            'sver': '2',
            'X-USER-MODE': 'id',
            'k_ft1': '141287244169348',
            'k_ft4': '34359738372',
            'k_ft7': '0',
            'k_ft5': '16777217',
            'bop': f'{{"version":"10.0","dfp":{cookie_dict.get("__dfp", "")},"b_ft1":0}}',
            "ut": "1",
        }
        url_avc = "/dash?" + urlencode(params_avc)
        cmd5js = execjs.compile(open("cmd5x.js").read())
        vf_avc = cmd5js.call("parse_vf", url_avc)

        url_hevc = "/dash?" + urlencode(params_hevc)
        cmd5js = execjs.compile(open("cmd5x.js").read())
        vf_hevc = cmd5js.call("parse_vf", url_hevc)

        dash_url_avc = f"https://intl-api.iq.com/3f4/cache-video.iq.com{url_avc}&vf={vf_avc}"
        response_episode = session.get(dash_url_avc)
        data = response_episode.json()
        scrsz = next(filter(lambda x: 'm3u8' in x, data['data']['program']['video']))['scrsz']
        m3u8_uwu_avc = next(filter(lambda x: 'm3u8' in x, data['data']['program']['video']))['m3u8']

        dash_url_hevc = f"https://intl-api.iq.com/3f4/cache-video.iq.com{url_hevc}&vf={vf_hevc}"
        response_episode_hevc = session.get(dash_url_hevc)
        data_hevc = response_episode_hevc.json()
        scrsz = next(filter(lambda x: 'm3u8' in x, data_hevc['data']['program']['video']))['scrsz']
        m3u8_uwu_hevc = next(filter(lambda x: 'm3u8' in x, data_hevc['data']['program']['video']))['m3u8']
        response_dash = session.get(dash_url_avc)
        data = response_dash.json()
        subtitles = data['data']['program']['stl']
        subtitles_dict = {subtitle['_name']: subtitle['srt'] for subtitle in subtitles if 'srt' in subtitle}
        playLocSuffix_clean = re.sub(r'[\\/:*?"<>|]', '_', playLocSuffix)
        resolution = alto = int(scrsz.split('x')[1])
        title_episode_uwu = title_episode.replace(" ", ".")
        title_video = f'Title: {title_episode}'
        info_video = f"Getting tracks for {title_episode} [{tv_id}]"
        logger.info(title_video)
        logger.info(info_video)
        filename_audio = f'\u251C AUD | [AAC] | 2.0'
        filename_video_avc = f'{title_episode_uwu}.iQ.{resolution}p.WEB-DL.AAC2.0.H.264'
        filename_info_avc = f'\u251C VID | [H.264, SDR] | {scrsz}'
        filename_video_hevc = f'{title_episode_uwu}.iQ.{resolution}p.WEB-DL.AAC2.0.H.265'
        filename_info_hevc = f'\u251C VID | [H.265, SDR] | {scrsz}'
        m3u8_file_avc = f'{title_episode_uwu}.iQ.avc.m3u8'
        m3u8_file_hevc = f'{title_episode_uwu}.iQ.hevc.m3u8'

        # Write M3U8 URLs to files
        with open(m3u8_file_avc, 'w') as file:
            file.write(m3u8_uwu_avc)
        with open(m3u8_file_hevc, 'w') as file:
            file.write(m3u8_uwu_hevc)

        # Command for processing AVC video
        logger.info("Video Tracks:")
        logger.info(filename_info_avc)
        logger.info("Audio Tracks:")
        logger.info(filename_audio)
        logger.info("Subtitle Tracks:")
        for language, srt_url in subtitles_dict.items():
            filename_subtitle = f'\u251C SUB | [SRT] | {language}'
            logger.info(filename_subtitle)
            response_subtitle = session.get(f'http://meta.video.iqiyi.com{srt_url}')
            if response_subtitle.status_code == 200:
                language_clean = re.sub(r'[\\/:*?"<>|]', '_', language)
                filename = os.path.join(subtitles_path, f'{title_episode_uwu}_{language_clean}.srt')
                with open(filename, 'wb') as subtitle_file:
                    subtitle_file.write(response_subtitle.content)
            else:
                logger.error("Failed to download subtitle for language %s", language)
        subprocess.run([
                    os.path.join(current_dir, "RE.exe"),
                    m3u8_file_avc,
                    "-mt",
                    f"--tmp-dir={temp_path}",
                    f"--save-dir={downloads_path}",
                    "--download-retry-count=5",
                    "--check-segments-count=false",
                    "--no-date-info",
                    "--log-level=OFF",
                    "--save-name", filename_video_avc,
                    f"--mux-after-done", f"format=mkv:muxer=mkvmerge:bin_path=mkvmerge.exe"
                ])
        logger.info("Download concluded!")

        # Command for processing HEVC video
        logger.info("Video Tracks:")
        logger.info(filename_info_hevc)
        logger.info("Audio Tracks:")
        logger.info(filename_audio)
        logger.info("Subtitle Tracks:")
        for language, srt_url in subtitles_dict.items():
            filename_subtitle = f'\u251C SUB | [SRT] | {language}'
            logger.info(filename_subtitle)
        subprocess.run([
                    os.path.join(current_dir, "RE.exe"),
                    m3u8_file_hevc,
                    "-mt",
                    f"--tmp-dir={temp_path}",
                    f"--save-dir={downloads_path}",
                    "--download-retry-count=5",
                    "--check-segments-count=false",
                    "--no-date-info",
                    "--log-level=OFF",
                    "--save-name", filename_video_hevc,
                    f"--mux-after-done", f"format=mkv:muxer=mkvmerge:bin_path=mkvmerge.exe"
                ])
        logger.info("Download concluded!")

        # Remove M3U8 files
        os.remove(m3u8_file_avc)
        os.remove(m3u8_file_hevc)
    else:
        logger.error("Request was unsuccessful. Response code: %s", response_episode.status_code)
