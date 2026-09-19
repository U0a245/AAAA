#!/usr/bin/env python3
import curses
import os
import random
input()
def is_chinese():
    lang = os.environ.get('LANG', '')
    return lang.startswith('zh')

def main(stdscr):
    cn = is_chinese()
    curses.curs_set(0)
    speed = 100
    stdscr.timeout(speed)

    sh, sw = stdscr.getmaxyx()
    snake = [(sh // 2, sw // 2), (sh // 2, sw // 2 - 1), (sh // 2, sw // 2 - 2)]
    dx, dy = 0, 1
    food = None
    auto_pilot = False

    stdscr.clear()
    stdscr.border(0)
    stdscr.refresh()

    while True:
        if not food:
            while True:
                fy = random.randint(1, sh - 2)
                fx = random.randint(1, sw - 2)
                if (fy, fx) not in snake:
                    break
            food = (fy, fx)
            try:
                stdscr.addch(food[0], food[1], ord('*'))
            except curses.error:
                pass

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('a'):
            auto_pilot = not auto_pilot
            if not auto_pilot:
                hx, hy = snake[0]
                hx = max(1, min(hx, sh - 2))
                hy = max(1, min(hy, sw - 2))
                snake[0] = (hx, hy)
        elif key == ord('+') or key == ord('='):
            speed = max(0, speed - 1)
            stdscr.timeout(speed)
        elif key == ord('-') or key == ord('_'):
            speed = speed + 1
            stdscr.timeout(speed)
        elif not auto_pilot:
            if key == curses.KEY_UP and dx != 1:
                dx, dy = -1, 0
            elif key == curses.KEY_DOWN and dx != -1:
                dx, dy = 1, 0
            elif key == curses.KEY_LEFT and dy != 1:
                dx, dy = 0, -1
            elif key == curses.KEY_RIGHT and dy != -1:
                dx, dy = 0, 1

        if auto_pilot and food:
            hx, hy = snake[0]
            fx, fy = food
            if hx < fx and dx != 1:
                dx, dy = 1, 0
            elif hx > fx and dx != -1:
                dx, dy = -1, 0
            elif hy < fy and dy != 1:
                dx, dy = 0, 1
            elif hy > fy and dy != -1:
                dx, dy = 0, -1

        head = (snake[0][0] + dx, snake[0][1] + dy)

        if not auto_pilot:
            if (head[0] <= 0 or head[0] >= sh - 1 or
                head[1] <= 0 or head[1] >= sw - 1 or
                head in snake):
                break

        snake.insert(0, head)

        if head == food:
            food = None
            old_tail = None
        else:
            old_tail = snake.pop()

        for i, (cy, cx) in enumerate(snake):
            try:
                if i == 0:
                    stdscr.addch(cy, cx, ord('@'))
                else:
                    stdscr.addch(cy, cx, ord('#'))
            except curses.error:
                pass

        if old_tail:
            try:
                stdscr.addch(old_tail[0], old_tail[1], ord(' '))
            except curses.error:
                pass

        if cn:
            status = f" 得分: {len(snake)-3} | 速度: {speed}ms | 自动: {'开' if auto_pilot else '关'} "
        else:
            status = f" Score: {len(snake)-3} | Speed: {speed}ms | Auto: {'ON' if auto_pilot else 'OFF'} "
        try:
            stdscr.addstr(sh - 1, 1, status[:sw - 2])
        except curses.error:
            pass
        stdscr.refresh()

    stdscr.border(0)
    if cn:
        msg = f"游戏结束！得分: {len(snake)}"
    else:
        msg = f"Game Over! Score: {len(snake)}"
    try:
        stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg)
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)