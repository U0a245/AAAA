@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================
REM  音乐批量转 MP3 脚本
REM  用法: 把本脚本放到音乐目录下双击运行
REM        或在命令行传目录: convert_to_mp3.bat "D:\Music"
REM ============================================

if "%~1"=="" (
    set "MUSIC_DIR=%~dp0"
) else (
    set "MUSIC_DIR=%~1"
)

if not exist "%MUSIC_DIR%" (
    echo [ERROR] 目录不存在: %MUSIC_DIR%
    pause
    exit /b 1
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [ERROR] 未找到 ffmpeg，请先安装并加入 PATH
    echo         下载: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo.
echo ============================================
echo  音乐目录: %MUSIC_DIR%
echo  目标格式: MP3 (libmp3lame, V2 质量)
echo ============================================
echo.

set /a TOTAL=0
set /a CONVERTED=0
set /a SKIPPED=0
set /a FAILED=0

pushd "%MUSIC_DIR%"

for %%F in (*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma *.opus *.ape *.mp4 *.mkv) do (
    set "IN=%%~fF"
    set "NAME=%%~nF"
    set "OUT=%MUSIC_DIR%\!NAME!.converted.mp3"

    if exist "!OUT!" del /q "!OUT!"

    set /a TOTAL+=1
    echo [!TOTAL!] 处理: %%F

    REM 先检测真实编码格式
    set "IS_REAL_MP3=0"
    for /f "delims=" %%I in ('ffprobe -v error -select_streams a:0 -show_entries stream^=codec_name -of default^=noprint_wrappers^=1:nokey^=1 "!IN!" 2^>nul') do (
        if /i "%%I"=="mp3" set "IS_REAL_MP3=1"
    )

    if "!IS_REAL_MP3!"=="1" (
        echo     - 检测到真实 MP3，跳过转码
        set /a SKIPPED+=1
    ) else (
        ffmpeg -y -hide_banner -loglevel error -i "!IN!" -vn -c:a libmp3lame -q:a 2 "!OUT!"
        if errorlevel 1 (
            echo     - [FAILED] 转码失败
            set /a FAILED+=1
        ) else (
            echo     - [OK] 已生成: !NAME!.converted.mp3
            set /a CONVERTED+=1
        )
    )
)

echo.
echo ============================================
echo  完成
echo  总计: !TOTAL!  转码: !CONVERTED!  跳过: !SKIPPED!  失败: !FAILED!
echo ============================================
echo.

echo 是否删除原始文件？
echo   1 = 只删除已成功转码的原文件
echo   2 = 全部保留
echo   3 = 全部删除（危险）
set /p CHOICE=请输入选项 [1/2/3]: 

if "%CHOICE%"=="1" (
    for %%F in (*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma *.opus *.ape *.mp4 *.mkv) do (
        set "NAME=%%~nF"
        if exist "%MUSIC_DIR%\!NAME!.converted.mp3" (
            echo 删除: %%F
            del /q "%%~fF"
        )
    )
    echo 已删除已转码的原文件
) else if "%CHOICE%"=="3" (
    for %%F in (*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma *.opus *.ape *.mp4 *.mkv) do (
        set "NAME=%%~nF"
        if exist "%MUSIC_DIR%\!NAME!.converted.mp3" (
            echo 删除: %%F
            del /q "%%~fF"
        )
    )
    echo 警告: 已删除所有原文件（包括未转码的）
) else (
    echo 保留所有原文件
)

REM 把 .converted.mp3 改回原名
for %%F in (*.converted.mp3) do (
    set "BASE=%%~nF"
    set "BASE=!BASE:.converted=!"
    if exist "!BASE!.mp3" del /q "!BASE!.mp3"
    ren "%%F" "!BASE!.mp3"
    echo 重命名: %%F  ->  !BASE!.mp3
)

popd

echo.
echo 全部完成，按任意键退出...
pause >nul