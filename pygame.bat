@echo off
cd /d %~dp0
if exist pygame.py (
    ren pygame.py pygame.py.disabled
    echo Switched to real pygame
) else (
    ren pygame.py.disabled pygame.py
    echo Switched to mpv
)
pause