import dash_core_components as dcc 
import dash_html_components as html

#footer
def footer():
    return html.Footer([
            html.Div([
                html.P([
                    'ELEC 498 Capstone Project 2020 - Team 2',
                ])
            ],
            className='footer-area')
        ])