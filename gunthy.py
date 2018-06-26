# SYSTEM IMPORTS
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from time import sleep
import multiprocessing
import os
import shlex
import sys
import threading
import webbrowser

# THIRD PARTY IMPORTS
from dash import Dash
from plotly.offline import plot
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

# LOCAL IMPORTS
from fomo_gunbot_plus.view import Chart
from fomo_gunbot_plus.systemcheck import SystemCheck
from fomo_gunbot_plus.title import show_title
from fomo_gunbot_plus.watch_configuration import watch_configuration_folder
from fomo_gunbot_plus.core import Core


def run_chart():

    url = 'http://127.0.0.1:8050/'
    app = Chart.get_chart()

    threading.Timer(2.5, lambda: webbrowser.open(url)).start()

    app.run_server(debug=False)  # debug=TRUE Conflicts with gunbot


def run_gunthy():

    BASEPATH = Path(__file__).parent / 'gunbot' / 'gunthy-linx64'
    assert BASEPATH.exists()

    cmd = str(BASEPATH.absolute())
    cwd = str(BASEPATH.parent)

    os.chmod(cmd, 0o755)

    process = Popen(cmd, shell=False, cwd=cwd)

    while True:
        try:
            output = process.stdout.readline()
            if output:
                print(str(output.strip(), 'utf-8'))
        except AttributeError:
            break
    rc = process.poll()


def main():

    show_title()
    sleep(2)

    one = multiprocessing.Process(target=Core.run)
    two = multiprocessing.Process(target=run_gunthy)
    three = multiprocessing.Process(target=watch_configuration_folder)

    one.start()
    two.start()
    three.start()

    run_chart()

    one.join()
    two.join()
    three.join()


if __name__ == '__main__':
    if SystemCheck.run() == True:
        main()
    else:
        print('System Check did not pass. Gunbot will not run.')
