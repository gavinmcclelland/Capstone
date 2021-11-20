import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import server
from app import app

from layouts import layout_home, layout_bain, layout_ILC, layout_cluster, layout_orchard, layout_about

# from test import layout_home

import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

''' Update page '''
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/wi-wait/' or pathname == '/wi-wait/home/':
        return layout_home
    elif pathname == '/wi-wait/bain/':
        return layout_bain
    elif pathname == '/wi-wait/ILC/':
        return layout_ILC
    elif pathname == '/wi-wait/cluster/':
        return layout_cluster
    elif pathname == '/wi-wait/orchard/':
        return layout_orchard
    elif pathname == '/wi-wait/about/':
        return layout_about
    else:
        return noPage

if __name__ == '__main__':
    app.run_server(debug=True)