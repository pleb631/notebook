import sys
import time
from rich.console import Console
from rich.text import Text

levels = {
    0: ('ERROR', 'bold red'),
    1: ('WARNING', 'bold yellow'),
    2: ('INFO', 'bold green'),
    3: ('DEBUG', 'bold cyan'),
}

log_level = 2
console = Console()

def log(level=2, message=""):
    if log_level < level:
        return

    level_name, level_style = levels.get(level, ('INFO', 'bold green'))
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 构建一行文字，带颜色但不换行
    text = Text()
    text.append(f"{current_time} ", style="dim")                         # 时间灰色
    text.append(f"[{level_name:<7}] ", style=level_style)               # 等宽格式对齐
    text.append(message, style="white")                                  # 正文白色（可调）

    console.print(text, highlight=False, soft_wrap=False, overflow="ignore", end="")
    console.print("")  # 手动换行（避免 rich 自动多段输出换行）
    sys.stdout.flush()

def debug(message=""):
    log(level=3, message=message)


def info(message=""):
    log(level=2, message=message)


def warning(message=""):
    log(level=1, message=message)


def error(message=""):
    log(level=0, message=message)
