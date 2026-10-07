import os
import sys
import types


def _pick_ao():
    if sys.platform.startswith("win"):
        return "wasapi"
    if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
        return "aaudio"
    return "pulseaudio"


class _MMusic:
    def __init__(self):
        self._p = None
        self._cur = None
    def _m(self):
        if self._p is None:
            import mpv
            self._p = mpv.MPV(ao=_pick_ao(), ytdl=False)
        return self._p
    def load(self, p): self._cur = p
    def play(self, *a, **k):
        if self._cur:
            try: self._m().play(self._cur)
            except Exception: pass
    def pause(self):
        try: self._m().pause = True
        except Exception: pass
    def unpause(self):
        try: self._m().pause = False
        except Exception: pass
    def stop(self):
        try: self._m().command("stop")
        except Exception: pass
    def rewind(self):
        try: self._m().command("seek", 0, "absolute")
        except Exception: pass
    def set_pos(self, s):
        try: self._m().command("seek", float(s), "absolute")
        except Exception: pass
    def get_pos(self):
        try:
            t = self._m().time_pos
            return int(float(t) * 1000) if t is not None else -1
        except Exception: return -1
    def get_busy(self):
        try: return self._cur is not None and not self._m().pause
        except Exception: return False
    def set_volume(self, v):
        try: self._m().volume = int(v * 130)
        except Exception: pass


class _MMixer:
    def __init__(self):
        self.music = _MMusic()
    def init(self, *a, **k):
        self.music._m()
    def quit(self):
        if self.music._p:
            try: self.music._p.command("quit")
            except Exception: pass
            self.music._p = None
    def get_init(self):
        return self.music._p is not None
    def Sound(self, p):
        class _S:
            def get_length(self_):
                try:
                    import mutagen
                    return float(mutagen.File(p).info.length)
                except Exception: return 0.0
        return _S()


def get_pygame():
    try:
        import mpv
        return False
    except Exception:
        return True


mixer = _MMixer()