from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from fomo_gunbot_plus.title import show_title
from fomo_gunbot_plus.watch_configuration import watch_configuration_folder
from fomo_gunbot_plus.gunbot_interface import GunBotConfigInterface

import sys
import multiprocessing
from time import sleep

from fomo_superfilter.interface import BinanceDataFrameCreator
from fomo_superfilter.interface import BittrexDataFrameCreator
from fomo_superfilter.superfilter import SuperFilter

import plotly
from plotly.offline import plot
import plotly.graph_objs as go

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html


def chart():
    trace = go.Scatter(
        name='curve',
        x=[x for x in range(100)],
        y=[y*y for y in range(100)]
    )
    fig = go.Figure(data=[trace])

    app = Dash(__name__)
    app.layout = html.Div(children=[html.H1('equity-curve'),
                                    dcc.Graph(id='equity-curve', figure=fig)])
    app.run_server(debug=False)


def run():

    GBI = GunBotConfigInterface()  # TODO: Logging
    GBI.update_config_from_toml()
    GBI.write_to_gunbot_config()

    while True:
        print('Looking for a hot coins...')

        binance_data = BinanceDataFrameCreator.prepare_dataframes()
        binance_btc = binance_data['BTC']
        binance_filtered = SuperFilter.filter(binance_btc)
        print('FOUND:', binance_filtered)
        print('Equity Curve Running on...')
        print('* Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)')

        sleep(30)


def run_command():

    BASEPATH = Path(__file__).parent / 'gunbot' / 'gunthy-linx64'
    assert BASEPATH.exists()
    cmd = str(BASEPATH.absolute())
    cwd = str(BASEPATH.parent)

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
    sleep(2.5)

    one = multiprocessing.Process(target=run)
    two = multiprocessing.Process(target=run_command)
    three = multiprocessing.Process(target=watch_configuration_folder)

    one.start()
    two.start()
    three.start()
    chart()

    one.join()
    two.join()
    three.join()


if __name__ == '__main__':
    main()
