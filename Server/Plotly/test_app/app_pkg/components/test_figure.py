import sys
sys.path.insert(1, '/home/wi-wait/database')
import DBPull
# from home.wi-wait.database.DBPull import getdata()
import dash_core_components as dcc 
import dash_html_components as html

def get_test_figure():
    df = DBPull.real_count()
    df2 = DBPull.type4()
    df3 = DBPull.type0()
    # test = str(df.real_count)
    # testsplit = test.splitlines()
    return html.Div([
        # html.Plaintext(str(x)) for x in testsplit
        dcc.Graph(
        id='test-graph',
        figure = {
            'data': [
                {'x' : df.timestamp, 'y':df.real_count, 'type':'line', 'name':'Total Count'},
                {'x' : df2.timestamp, 'y':df2.NumPeople, 'type':'line', 'name':'Reassociation Count'},
                {'x' : df3.timestamp, 'y':df3.NumPeople, 'type':'line', 'name':'All Devices'},
            ],
            'layout': {
                'title': 'Bain Foot Traffic'
            }
        })
    ])
