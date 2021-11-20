import dash_core_components as dcc
import dash_html_components as html
from components import header,footer

layout_home = html.Div([ 
    # Wrapper
    html.Div([
        # Header
        header.header(),
        header.nav(),
        footer.footer()
    ])
])
