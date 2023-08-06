import argparse
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from appdirs import user_cache_dir
from bs4 import BeautifulSoup
from joblib import Memory
from markdownify import markdownify as md
from rich.console import Console
from rich.markdown import Markdown

appname = "Notes50"
appauthor = "Zed"
memory = Memory(user_cache_dir(appname, appauthor),
                verbose=0, bytes_limit=10485760)
Memory.reduce_size(memory)

notes = {
    "x": f"https://cs50.harvard.edu/x/2022/notes/",
    "p": f"https://cs50.harvard.edu/python/2022/notes/",
    "w": f"https://cs50.harvard.edu/web/2020/notes/",
    "a": f"https://cs50.harvard.edu/ai/2020/notes/",
    "g": f"https://cs50.harvard.edu/games/2018/notes/"
}

psets = {
    "x": f"https://cs50.harvard.edu/x/2022/psets/",
    "p": f"https://cs50.harvard.edu/python/2022/psets/",
    "w": f"https://cs50.harvard.edu/web/2020/projects/",
    "a": f"https://cs50.harvard.edu/ai/2020/projects/",
    "g": f"https://cs50.harvard.edu/games/2018/projects/"
}

projects = {
    "x": f"https://cs50.harvard.edu/x/2022/project",
    "p": f"https://cs50.harvard.edu/python/2022/project",
    "w": f"https://cs50.harvard.edu/web/2020/projects/final/capstone/",
    "g": f"https://cs50.harvard.edu/games/2018/projects/final/final/"
}


def main():
    args = parse_args(sys.argv[1:])
    for i in vars(args):
        if f"{getattr(args, i)}".isnumeric():
            print(note(args, i))
        elif getattr(args, i):
            print(pset(args, i))


@memory.cache
def note(args, i):
    url = f"{notes[i]}{getattr(args, i)}"
    try:
        return get(url)
    except HTTPError:
        print("Url Not A Found Please Check Your Argument")
        sys.exit(1)


@memory.cache
def pset(args, i):
    if getattr(args, i) == "project":
        url = f"{projects[i]}"
    else:
        url = f"{psets[i]}{getattr(args, i)}"
    try:
        return get(url)
    except HTTPError:
        print("Url Not Found Please Check Your Argumnet")
        sys.exit(1)


@memory.cache
def get(url):
    con = Console(record=True)
    html = urlopen(Request(url)).read().decode()
    main = BeautifulSoup(html, "lxml")
    main = main.main
    markdown = md(main.prettify())
    ri = Markdown(markdown)
    with con.capture() as capture:
        con.print(ri)
    return capture.get()


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="CS50 Notes And Problem Sets Reader In Terminal",
        epilog=help(),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", metavar="Week, Week/PSet",
                        help="CS50 AI Week Notes or Week/PSet Name (No Final Project)")
    parser.add_argument("-g", metavar="Week, Week/PSet",
                        help="CS50 Games Week Notes or Week/PSet Name")
    parser.add_argument("-p", metavar="Week, Week/PSet",
                        help="CS50 Python Week Notes or Week/PSet Name")
    parser.add_argument("-w", metavar="Week, Week/PSet",
                        help="CS50 Web Week Notes or Week/PSet Name")
    parser.add_argument("-x", metavar="Week, Week/PSet",
                        help="CS50x Week Notes or Week/PSet Name")

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args(args)


def help():
    return """
Examples:
    For Week Notes:
        python notes50.py -x 0
        python notes50.py -p 0
    For Week Pset:
        python notes50.py -x 0/scratch
        python notes50.py -p 0/indoor
    For Final Project:
        python notes50.py -x project
        python notes50.py -p project

Note:- First Time Maybe Slow Because Of Caching It Will be Faster From The Next Time
"""


if __name__ == "__main__":
    main()
