# install_and_build.py
import os
import sys
import shutil
import glob
import py_compile
import subprocess
from pathlib import Path

# ================= 配置区 =================
WHL_FILE = "music_player.whl"
RES_DIR = Path("res")
# =========================================


def install_whl():
    """1. 安装 whl 包"""
    whl = Path(WHL_FILE)
    if not whl.exists():
        candidates = list(Path(".").rglob("music_player-*.whl"))
        if not candidates:
            sys.exit(f"[!] 找不到 {WHL_FILE}，也没在目录里搜到 whl 文件")
        whl = candidates[0]
    print(f"[*] 安装: {whl}")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        str(whl), "--force-reinstall"
    ])
    print("[+] whl 安装完成")


def delete_jpgs():
    """2. 删除当前目录下所有 jpg 图片"""
    jpgs = glob.glob("*.jpg") + glob.glob("*.jpeg")
    for f in jpgs:
        os.remove(f)
        print(f"[-] 删除图片: {f}")
    if not jpgs:
        print("[*] 当前目录没有 jpg 文件")


def delete_music_player_py():
    """3. 删除当前目录下的 music_player.py"""
    f = Path("music_player.py")
    if f.exists():
        f.unlink()
        print(f"[-] 删除文件: {f}")
    else:
        print("[*] 当前目录没有 music_player.py")


def clear_res_dir():
    """4. 删除 res/ 目录下所有文件（保留目录本身）"""
    if not RES_DIR.exists():
        print("[*] res/ 目录不存在，跳过")
        return
    for item in RES_DIR.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
            print(f"[-] 删除文件: {item}")
        elif item.is_dir():
            shutil.rmtree(item)
            print(f"[-] 删除目录: {item}")
    print("[+] res/ 已清空")


def create_runner_py():
    """5. 创建新的 music_player.py，导入库并执行 main()"""
    code = '''# -*- coding: utf-8 -*-
"""自动生成的入口脚本"""
import music_player

if __name__ == "__main__":
    music_player.main()
'''
    Path("music_player.py").write_text(code, encoding="utf-8")
    print("[+] 已创建 music_player.py")


def compile_to_pyc():
    """6. 把 music_player.py 编译成 .pyc"""
    pyc_path = py_compile.compile(
        "music_player.py",
        cfile="music_player.pyc",
        doraise=True
    )
    print(f"[+] 已生成字节码: {pyc_path}")
    return Path(pyc_path)


def rename_pyc_to_py(pyc_path):
    """7. 把 .pyc 改名为 .py"""
    py_path = pyc_path.with_suffix(".py")
    if py_path.exists():
        py_path.unlink()
    pyc_path.rename(py_path)
    print(f"[+] 已重命名为: {py_path}")
    return py_path


def main():
    install_whl()
    delete_jpgs()
    delete_music_player_py()
    clear_res_dir()
    create_runner_py()
    pyc_path = compile_to_pyc()
    py_path = rename_pyc_to_py(pyc_path)

    print("\n[✓] 全部完成")
    print(f"    最终产物: {py_path.resolve()}")
    print("    注意: 这个 .py 文件实际内容是字节码，")
    print("          不是文本源码，不能当作普通 .py 编辑或运行。")


if __name__ == "__main__":
    main()