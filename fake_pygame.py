import os

_mpv_inst = None
_current = None

def _get_mpv():
    global _mpv_inst
    if _mpv_inst is None:
        import mpv
        _mpv_inst = mpv.MPV(ao="opensles", ytdl=False,
                            http_headers="Referer: https://www.bilibili.com\r\n")
    return _mpv_inst


class _Music:
    def load(self, path):
        global _current
        _current = path

    def play(self, *a, **k):
        if _current is None:
            return
        try:
            _get_mpv().play(_current)
        except Exception:
            pass

    def pause(self):
        try: _get_mpv().pause = True
        except Exception: pass

    def unpause(self):
        try: _get_mpv().pause = False
        except Exception: pass

    def stop(self):
        try: _get_mpv().command("stop")
        except Exception: pass

    def rewind(self):
        try: _get_mpv().command("seek", 0, "absolute")
        except Exception: pass

    def set_pos(self, sec):
        try: _get_mpv().command("seek", float(sec), "absolute")
        except Exception: pass

    def get_pos(self):
        try:
            t = _get_mpv().time_pos
            return int(float(t) * 1000) if t is not None else -1
        except Exception:
            return -1

    def get_busy(self):
        try:
            m = _get_mpv()
            return _current is not None and not m.pause
        except Exception:
            return False

    def set_volume(self, v):
        try: _get_mpv().volume = int(v * 100)
        except Exception: pass


class _Sound:
    def __init__(self, path):
        self.path = path
    def get_length(self):
        try:
            import mutagen
            return float(mutagen.File(self.path).info.length)
        except Exception:
            return 0.0


class _Mixer:
    def __init__(self):
        self.music = _Music()
    def init(self, *a, **k):
        _get_mpv()
    def quit(self):
        global _mpv_inst, _current
        if _mpv_inst is not None:
            try: _mpv_inst.terminate()
            except Exception: pass
            _mpv_inst = None
        _current = None
    def get_init(self):
        return _get_mpv() is not None
    def Sound(self, path):
        return _Sound(path)

mixer = _Mixer()