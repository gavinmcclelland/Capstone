import dash_core_components as dcc 
import dash_html_components as html
import base64

def header():
   return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(src='https://i.gyazo.com/bd68f51d0a2d7d3fc23ef5a4ea189a7a.png')
                        ],
                        className='logo')
                    ],
                    className='col-md-3'
                    )
                ],
                className='row align-items-center'),
                
            ],
            className='container')
        ],
        className='mainheader-area'
        )

def nav():
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Nav([
                                html.Ul([
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-dashboard'),
                                            html.Span('Home')
                                        ],
                                        href='/wi-wait/'
                                        ),
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-pin'),
                                            html.Span('Bain Lab')
                                        ],
                                        href='/wi-wait/bain/'
                                        ),
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-pin'),
                                            html.Span('ILC Atrium')
                                        ],
                                        href='/wi-wait/ILC/'
                                        ),
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-pin'),
                                            html.Span('Cluster')
                                        ],
                                        href='/wi-wait/cluster/'
                                        ),
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-pin'),
                                            html.Span('Orchard')
                                        ],
                                        href='/wi-wait/orchard/')
                                    ]),
                                    html.Li([
                                        html.A([
                                            html.I(className='ti-info'),
                                            html.Span('About')
                                        ],
                                        href='/wi-wait/about/')
                                    ])
                                ],
                                id='nav_menu')
                            ])
                        ],
                        className='horizontal-menu')
                    ],
                    className='col-lg-12'
                    ),
                ],
                className='row align-items-center')
            ],
            className='container', style={'display': 'inline-block', 'float': 'none', 'text-align':'center'})
        ],
        className='header-area header-bottom'
        )
