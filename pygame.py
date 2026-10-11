import os, sys, tempfile, threading, time

def _pick_ao():
    if sys.platform.startswith("win"): return "wasapi"
    if sys.platform == "darwin": return "coreaudio"
    if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ: return "aaudio"
    return "pulseaudio"

def _mpv():
    try:
        import mpv
        return mpv
    except Exception:
        return None

def _new_player():
    m = _mpv()
    if m is None: return None
    try:
        return m.MPV(ao=_pick_ao(), video=False, ytdl=False, idle=True,
                     keep_open="yes", terminal=False, config=False)
    except Exception:
        try:
            return m.MPV(video=False, ytdl=False, idle=True,
                         keep_open="yes", terminal=False)
        except Exception:
            return None

def _src(s):
    if s is None: return None
    if isinstance(s, os.PathLike): return os.fspath(s)
    if isinstance(s, str): return s
    if isinstance(s, (bytes, bytearray, memoryview)):
        fd, p = tempfile.mkstemp(prefix="mixer_", suffix=".bin")
        with os.fdopen(fd, "wb") as f: f.write(bytes(s))
        return p
    n = getattr(s, "name", None)
    if isinstance(n, str): return n
    if hasattr(s, "read"):
        d = s.read()
        if isinstance(d, str): d = d.encode("utf-8")
        fd, p = tempfile.mkstemp(prefix="mixer_", suffix=".bin")
        with os.fdopen(fd, "wb") as f: f.write(d)
        return p
    return None

def _length(p):
    if not p or not os.path.exists(p): return 0.0
    try:
        import mutagen
        info = getattr(mutagen.File(p), "info", None)
        if info is not None: return float(info.length)
    except Exception: pass
    try:
        import wave
        with wave.open(p, "rb") as w: return w.getnframes() / float(w.getframerate() or 1)
    except Exception: pass
    return 0.0

_tickables = []
_ticker = None
_lock_t = threading.Lock()

def _start_ticker():
    global _ticker
    if _ticker and _ticker.is_alive(): return
    with _lock_t:
        if _ticker and _ticker.is_alive(): return
        _ticker = threading.Thread(target=_tick_loop, daemon=True)
        _ticker.start()

def _tick_loop():
    while True:
        time.sleep(0.05)
        for o in list(_tickables):
            try: o.tick()
            except Exception: pass

class _Player:
    def __init__(self):
        self._p = None; self._lk = threading.RLock(); self._sound = None
        self._path = None; self._vol = 1.0; self._gain = 1.0
        self._playing = False; self._paused = False
        self._loops = 0; self._loops_done = 0
        self._fade_t0 = 0.0; self._fade_dur = 0.0
        self._fade_from = 1.0; self._fade_to = 1.0; self._fade_stop = False
        self._deadline = None; self._eof = False

    def _m(self):
        if self._p is None: self._p = _new_player()
        return self._p

    def _kill(self):
        p = self._p; self._p = None; self._playing = False
        if p is None: return
        try: p.terminate()
        except Exception:
            try: p.command("quit")
            except Exception: pass

    def _av(self):
        if self._p is None: return
        try: self._p.volume = max(0.0, min(130.0, self._vol * self._gain * 100.0))
        except Exception: pass

    def _begin(self, path, loops=0, maxtime=0, fade_ms=0, start=0.0):
        p = self._m()
        if p is None or not path: return False
        now = time.monotonic()
        self._path = path; self._loops = int(loops); self._loops_done = 0
        self._playing = True; self._paused = False; self._eof = False
        if fade_ms and fade_ms > 0:
            self._gain = 0.0; self._fade_t0 = now
            self._fade_dur = float(fade_ms) / 1000.0
            self._fade_from = 0.0; self._fade_to = 1.0; self._fade_stop = False
        else:
            self._gain = 1.0; self._fade_dur = 0.0
        self._deadline = (now + maxtime / 1000.0) if maxtime and maxtime > 0 else None
        try: p.loop_file = "inf" if loops == -1 else "no"
        except Exception: pass
        try:
            p.play(path); p.pause = False
            if start and start > 0:
                try: p.command("seek", float(start), "absolute")
                except Exception: pass
            self._av()
        except Exception:
            self._playing = False; return False
        _start_ticker(); return True

    def _halt(self):
        self._playing = False; self._paused = False; self._gain = 1.0
        self._fade_dur = 0.0; self._fade_stop = False
        self._deadline = None; self._eof = False
        if self._p is not None:
            try: self._p.command("stop")
            except Exception: pass

    def _do_pause(self):
        if self._p is None or not self._playing: return
        try: self._p.pause = True; self._paused = True
        except Exception: pass

    def _do_unpause(self):
        if self._p is None or not self._playing: return
        try: self._p.pause = False; self._paused = False
        except Exception: pass

    def _do_fadeout(self, ms):
        if not self._playing: return
        self._fade_t0 = time.monotonic()
        self._fade_dur = max(0.001, float(ms) / 1000.0)
        self._fade_from = self._gain; self._fade_to = 0.0; self._fade_stop = True
        _start_ticker()

    def _on_finished(self):
        self._playing = False; self._paused = False; self._gain = 1.0

    def tick(self):
        with self._lk:
            if not self._playing: return
            now = time.monotonic()
            if self._fade_dur > 0:
                t = (now - self._fade_t0) / self._fade_dur
                done = t >= 1.0
                if done: t = 1.0; self._fade_dur = 0.0
                self._gain = self._fade_from + (self._fade_to - self._fade_from) * t
                self._av()
                if done and self._fade_stop: self._halt(); return
            if self._deadline is not None and now >= self._deadline: self._halt(); return
            if self._p is None: return
            try: eof = bool(self._p.eof_reached)
            except Exception: eof = False
            if not eof: self._eof = False; return
            if self._eof: return
            self._eof = True
            if self._loops > 0 and self._loops_done < self._loops:
                self._loops_done += 1
                try: self._p.play(self._path); self._p.pause = False; self._av()
                except Exception: self._on_finished()
            else:
                self._on_finished()

class Channel(_Player):
    def __init__(self, index):
        super().__init__(); self._index = index; _tickables.append(self)

    @property
    def index(self): return self._index

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        if isinstance(sound, Sound):
            path = sound._path; self._sound = sound; self._vol = sound.get_volume()
        else:
            path = _src(sound); self._sound = None; self._vol = 1.0
        if not path: return None
        with self._lk:
            if self._begin(path, loops=loops, maxtime=maxtime, fade_ms=fade_ms): return self
        return None

    def queue(self, sound):
        path = sound._path if isinstance(sound, Sound) else _src(sound)
        if not path: return
        p = self._m()
        if p is None: return
        try: p.command("loadfile", path, "append")
        except Exception: pass

    def get_queue(self): return None
    def stop(self):
        with self._lk: self._halt()
    def pause(self):
        with self._lk: self._do_pause()
    def unpause(self):
        with self._lk: self._do_unpause()
    def fadeout(self, ms):
        with self._lk: self._do_fadeout(ms)

    def get_busy(self):
        if not self._playing or self._p is None: return False
        try:
            if self._p.eof_reached: return False
        except Exception: pass
        return True

    def get_sound(self): return self._sound if self._playing else None
    def set_volume(self, v):
        with self._lk: self._vol = max(0.0, min(1.0, float(v))); self._av()
    def get_volume(self): return self._vol

class Sound:
    def __init__(self, file=None, buffer=None, **kw):
        s = file if file is not None else buffer
        if s is None: s = kw.get("file", kw.get("buffer"))
        if s is None: raise ValueError("Sound() 需要文件路径或 buffer")
        self._path = _src(s)
        if not self._path: raise ValueError("无法解析音频来源")
        self._vol = 1.0; self._len = None

    def play(self, loops=0, maxtime=0, fade_ms=0):
        ch = mixer.find_channel(True)
        if ch is None: return None
        return ch.play(self, loops=loops, maxtime=maxtime, fade_ms=fade_ms)

    def stop(self):
        for ch in mixer._channels:
            if ch._sound is self: ch.stop()

    def fadeout(self, ms):
        for ch in mixer._channels:
            if ch._sound is self: ch.fadeout(ms)

    def set_volume(self, v): self._vol = max(0.0, min(1.0, float(v)))
    def get_volume(self): return self._vol

    def get_length(self):
        if self._len is None: self._len = _length(self._path)
        return self._len

    def get_num_channels(self): return sum(1 for c in mixer._channels if c._sound is self and c.get_busy())
    def get_raw(self): return b""
    @property
    def path(self): return self._path

class _Music(_Player):
    def __init__(self):
        super().__init__(); self._queue = []; self._endevent = None
        self._loaded = False; _tickables.append(self)

    def load(self, filename):
        p = _src(filename)
        if not p: raise ValueError("music.load() 无法解析音频来源")
        if not os.path.exists(p): raise FileNotFoundError(p)
        with self._lk:
            self._halt(); self._path = p; self._loaded = True; self._queue = []

    def unload(self):
        with self._lk:
            self._halt(); self._path = None; self._queue = []; self._loaded = False

    def queue(self, filename):
        p = _src(filename)
        if not p: return
        with self._lk:
            if self._playing and self._p is not None:
                try: self._p.command("loadfile", p, "append")
                except Exception: pass
            else: self._queue.append(p)

    def play(self, loops=0, start=0.0, fade_ms=0):
        with self._lk:
            if not self._loaded or not self._path: raise RuntimeError("music 未加载")
            self._begin(self._path, loops=loops, fade_ms=fade_ms, start=start)

    def rewind(self):
        with self._lk:
            if self._p is None: return
            try: self._p.command("seek", 0, "absolute")
            except Exception: pass

    def stop(self):
        with self._lk:
            self._halt(); self._queue = []; self._post()

    def pause(self):
        with self._lk: self._do_pause()
    def unpause(self):
        with self._lk: self._do_unpause()
    def fadeout(self, ms):
        with self._lk: self._do_fadeout(ms)

    def get_busy(self):
        if not self._playing or self._p is None: return False
        try:
            if self._p.eof_reached: return False
        except Exception: pass
        return True

    def set_pos(self, pos):
        with self._lk:
            if self._p is None: return
            try: self._p.command("seek", float(pos), "absolute")
            except Exception: pass

    def get_pos(self):
        if self._p is None: return -1
        try: t = self._p.time_pos
        except Exception: return -1
        if t is None: return -1
        try: return int(float(t) * 1000)
        except Exception: return -1

    def set_volume(self, v):
        with self._lk: self._vol = max(0.0, min(1.0, float(v))); self._av()
    def get_volume(self): return self._vol
    def set_endevent(self, e=None): self._endevent = e
    def get_endevent(self): return self._endevent

    def _post(self):
        if self._endevent is None: return
        try:
            import pygame
            pygame.event.post(pygame.event.Event(self._endevent))
        except Exception: pass

    def _on_finished(self):
        super()._on_finished()
        if self._queue:
            nxt = self._queue.pop(0)
            if self._begin(nxt, loops=self._loops): return
        self._post()

class _Mixer:
    Sound = Sound
    Channel = Channel

    def __init__(self):
        self._lk = threading.RLock(); self._channels = []; self._num = 8
        self._reserved = 0; self._rr = 0; self._inited = False
        self.music = _Music(); self._ensure(self._num)

    def _ensure(self, n):
        while len(self._channels) < n: self._channels.append(Channel(len(self._channels)))

    def set_num_channels(self, n):
        n = max(0, int(n))
        with self._lk:
            self._num = n; self._ensure(n)
            while len(self._channels) > n:
                ch = self._channels.pop()
                try: ch.stop()
                except Exception: pass

    def get_num_channels(self): return self._num
    def set_reserved(self, n): self._reserved = max(0, int(n))
    def get_reserved(self): return self._reserved

    def find_channel(self, force=False):
        with self._lk:
            avail = self._channels[self._reserved:]
            if not avail: return None
            for ch in avail:
                if not ch.get_busy(): return ch
            if force:
                ch = avail[self._rr % len(avail)]; self._rr += 1; return ch
            return None

    def init(self, frequency=44100, size=-16, channels=2, buffer=512,
             devicename=None, allowedchanges=0):
        with self._lk:
            self._inited = True; self.music._m()
        _start_ticker()

    def quit(self):
        with self._lk:
            for ch in self._channels:
                try: ch.stop(); ch._kill()
                except Exception: pass
            try: self.music.stop(); self.music._kill()
            except Exception: pass
            self._inited = False

    def get_init(self): return (44100, -16, 2) if self._inited else None
    def stop(self):
        for ch in self._channels: ch.stop()
    def pause(self):
        for ch in self._channels: ch.pause()
    def unpause(self):
        for ch in self._channels: ch.unpause()
    def fadeout(self, ms):
        for ch in self._channels: ch.fadeout(ms)
    def get_busy(self): return any(ch.get_busy() for ch in self._channels)

mixer = _Mixer()
music = mixer.music

def init(*a, **k): return mixer.init(*a, **k)
def quit(): return mixer.quit()
def get_init(): return mixer.get_init()
def stop(): return mixer.stop()
def pause(): return mixer.pause()
def unpause(): return mixer.unpause()
def fadeout(ms): return mixer.fadeout(ms)
def set_num_channels(n): return mixer.set_num_channels(n)
def get_num_channels(): return mixer.get_num_channels()
def find_channel(force=False): return mixer.find_channel(force)
def get_busy(): return mixer.get_busy()
def get_pygame(): return _mpv() is None