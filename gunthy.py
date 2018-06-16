from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from title import show_title
from fomo_gunbot_plus.title import show_title
import sys
import multiprocessing
from time import sleep

BASEPATH = Path(__file__).parent / 'gunbot' / 'gunthy-linx64'
assert BASEPATH.exists()


def run():
    n = 1
    while True:
        print('#' * n)
        print('New Coin Found')
        print('#' * n)
        sleep(n)
        n += 1


cmd = str(BASEPATH.absolute())
cwd = str(BASEPATH.parent)


def run_command():
    process = Popen(cmd, shell=False, cwd=cwd)
    while True:
        try:
            output = process.stdout.readline()
            if output:
                print(str(output.strip(), 'utf-8'))
        except AttributeError:
            break
    rc = process.poll()


show_title()
sleep(2.5)
    show_title()
    sleep(2.5)

one = multiprocessing.Process(target=run)
two = multiprocessing.Process(target=run_command)

one.start()
two.start()

one.join()
two.join()
