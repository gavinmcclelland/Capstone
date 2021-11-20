import dash_core_components as dcc
import dash_html_components as html
from components import header,footer,test_figure

# ================== DEFINE HOME LAYOUT ================== #
layout_home = html.Div([
    # Wrapper Div
    html.Div([
        # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),

        # Content
        html.Div([
            html.Div([
                html.Div([
                    #Facts area
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Bain Lab'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('2,315')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg1')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'ILC Atrium'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('3,984')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg2')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'The Cluster'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('1,234')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg4')
                                ],
                                className='card')
                            ],
                            className='col-md-6'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Apple Orchard'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('567')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg3')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mb-3 mb-lg-0'
                            ),
                            #Line Chart
                            html.Div([
                                html.Div([
                                    html.Div([html.H5('Wi-Wait Test'),
                                                dcc.Graph(id='live-graph', animate=True),
                                                dcc.Interval(
                                                    id='update-interval',
                                                    interval=10000
                                                )
                                    ],  
                                    className='card-body')
                                ],
                                className='card')
                            ],
                            className='col-lg-12 mt-5'
                            )

                        ],
                        className='row',
                        style={
                            'alignItems': 'center'
                        })
                    ],
                    className='col-lg-12'
                    ),
                    
                    #Bar chart
                    # html.Div([
                    #     html.Div([
                    #         html.Div([
                    #             html.H4(
                    #                 'Bar Charts',
                    #                 className='header-title'
                    #             ),
                    #             html.Div(children=[
                    #                 html.H5('Wi-Wait Test'),
                    #                 dcc.Graph(id='test',
                    #                 figure = {
                    #                     'data': [
                    #                                 {'x' : [1,2,3,4,5], 'y':[5,6,7,2,1], 'type':'line', 'name':'object1'},
                    #                                 {'x' : [1,2,3,4,5], 'y':[8,4,6,2,9], 'type':'bar', 'name':'object2'},
                    #                             ],
                    #                     'layout': {
                    #                         'title':'Bar Chart'
                    #                                 }
                    #                         })
                    #             ])
                    #         ],
                    #         className='card-body pb-0')
                    #     ],
                    #     className='card')
                    # ],
                    # className='col-lg-4 mt-5'
                    # ),

                    #Pie Chart
                    # html.Div([
                    #     html.Div([
                    #         html.Div([
                    #             html.H4(
                    #                 'Pie Chart',
                    #                 className='header-title'
                    #             ),
                    #             html.H6('Graph Here...')
                    #         ],
                    #         className='card-body')
                    #     ],
                    #     className='card')
                    # ],
                    # className='col-lg-4 mt-5'
                    # ),

                    #Scatter Plot
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H4(
                                    'Scatter Plot Chart',
                                    className='header-title'
                                ),
                                html.Div('Graph Here...')
                            ],
                            className='card-body')
                        ],
                        className='card')
                    ],
                    className='col-xl-8 col-lg-8 mt-5'
                    ),

                    #map
                    html.Div([
                        html.Div([
                            html.A([
                                        html.Img(
                                            src='assets/img/map.png',
                                            alt='logo'
                                        )
                                    ],
                                        href='#'
                                    )
                        ],
                        className='card')
                    ],
                    className='col-lg-6 mt-5')

                ],
                className='row')
            ],
            className='container')
        ],
        className='main-content-inner'),

    footer.footer()
    ],
    className='horizontal-main-wrapper')
],
className='body-bg')

# ================== END HOME LAYOUT ================== #




# ================== DEFINE BAIN LAYOUT ================== #
layout_bain = html.Div([

    #main wrapper
    html.Div([
         # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),

        #main content area
        html.Div([
            html.Div([
                html.Div([
                    #Facts area
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Bain Lab'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('2,315')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg1')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'ILC Atrium'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('3,984')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg2')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'The Cluster'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('1,234')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg4')
                                ],
                                className='card')
                            ],
                            className='col-md-6'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Apple Orchard'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('567')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg3')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mb-3 mb-lg-0'
                            ),

                        ],
                        className='row',
                        style={
                            'alignItems': 'center'
                        })
                    ],
                    className='col-lg-12'
                    ),

                ],
                className='row')
            ],
            className='container')
        ],
        className='main-content-inner'),

        #footer
        footer.footer()
    ],
    className='horizontal-main-wrapper')
],
className='body-bg')
# ================== END BAIN LAYOUT ================== #

# ================== DEFINE ILC LAYOUT ================== #
layout_ILC = html.Div([

    #main wrapper
    html.Div([
         # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),
        #main content area
        html.Div([
            html.Div([
                html.Div([
                    #Facts area
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Bain Lab'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('2,315')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg1')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'ILC Atrium'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('3,984')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg2')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'The Cluster'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('1,234')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg4')
                                ],
                                className='card')
                            ],
                            className='col-md-6'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Apple Orchard'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('567')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg3')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mb-3 mb-lg-0'
                            ),

                        ],
                        className='row',
                        style={
                            'alignItems': 'center'
                        })
                    ],
                    className='col-lg-12'
                    ),

                ],
                className='row')
            ],
            className='container')
        ],
        className='main-content-inner'),

        #footer
        footer.footer()
    ],
    className='horizontal-main-wrapper')
],
className='body-bg')
# ================== END ILC LAYOUT ================== #

# ================== DEFINE CLUSTER LAYOUT ================== #
layout_cluster = html.Div([

    #main wrapper
    html.Div([
         # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),
        #main content area
        html.Div([
            html.Div([
                html.Div([
                    #Facts area
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Bain Lab'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('2,315')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg1')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'ILC Atrium'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('3,984')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg2')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'The Cluster'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('1,234')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg4')
                                ],
                                className='card')
                            ],
                            className='col-md-6'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Apple Orchard'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('567')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg3')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mb-3 mb-lg-0'
                            ),

                        ],
                        className='row',
                        style={
                            'alignItems': 'center'
                        })
                    ],
                    className='col-lg-12'
                    ),

                ],
                className='row')
            ],
            className='container')
        ],
        className='main-content-inner'),

        #footer
        footer.footer()
    ],
    className='horizontal-main-wrapper')
],
className='body-bg')
# ================== END CLUSTER LAYOUT ================== #

# ================== DEFINE ORCHARD LAYOUT ================== #
layout_orchard = html.Div([

    #main wrapper
    html.Div([
         # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),
        #main content area
        html.Div([
            html.Div([
                html.Div([
                    #Facts area
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Bain Lab'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('2,315')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg1')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'ILC Atrium'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('3,984')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg2')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mt-5 mb-3'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'The Cluster'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('1,234')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg4')
                                ],
                                className='card')
                            ],
                            className='col-md-6'
                            ),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                'Apple Orchard'
                                            ],
                                            className='seofct-icon'),
                                            html.H2('567')
                                        ],
                                        className='p-4 d-flex justify-content-between align-items-center')
                                    ],
                                    className='seo-fact sbg3')
                                ],
                                className='card')
                            ],
                            className='col-md-6 mb-3 mb-lg-0'
                            ),

                        ],
                        className='row',
                        style={
                            'alignItems': 'center'
                        })
                    ],
                    className='col-lg-12'
                    ),

                ],
                className='row')
            ],
            className='container')
        ],
        className='main-content-inner'),

        #footer
        footer.footer()
    ],
    className='horizontal-main-wrapper')
],
className='body-bg')
# ================== END ORCHARD LAYOUT ================== #

# ================== DEFINE ABOUT LAYOUT ================== #
layout_about = html.Div([

    #main wrapper
    html.Div([
         # Header Image
        header.header(),
        # Navigation Bar
        header.nav(),
        #main content area
        html.Div([
            html.Div([
                html.Div([
                    # Facts area
                    # html.Div([
                    #     html.Div([
                    #         html.Plaintext("                                                                                                                                   "),
                    #         html.Plaintext("                                                                                                                                   "),
                    #         html.Plaintext("Wi-Wait is an occupancy tracking tool created to help students find open places to study on Queenâ€™s campus."),
                    #         html.Plaintext("Want to avoid wasting time travelling from building to building looking for an open space to study? Simply pull"),
                    #         html.Plaintext("out your phone, tablet, or laptop and visit our website to see how busy your favourite study spaces are. "),
                    #         html.Plaintext("Occupancy is measured in percentage, with a percentage of under 40% meaning there is plenty of space, 40-70%"),
                    #         html.Plaintext("meaning there is ample space, and above 70% meaning the study space is relatively full."),
                    #         html.Plaintext("                                                                                                                                   "),
                    #         html.Plaintext("                                                                                                                                   "),
                    #         html.Plaintext("Wi-Wait was created as a fourth year Capstone project by four Electrical and Computer Engineering students in "),
                    #         html.Plaintext("the 2019-2020 academic year. It measures the occupancy level of a given area by measuring Wi-Fi traffic on the "),
                    #         html.Plaintext("Queenâ€™s enterprise network for a given router and uses an algorithm to convert number of devices to an occupancy "),
                    #         html.Plaintext("percentage. No identifying or personal data is stored or transmitted by Wi-Wait, ensuring that studentsâ€™ privacy "),
                    #         html.Plaintext("is always maintained."),

                    #     ],
                    #     className='row',
                    #     style={
                    #         'alignItems': 'center'
                    #     })
                    # ],
                    # className='col-lg-9'
                    # ), 
                    test_figure.get_test_figure()
                ],
                    className='row')
            ],
                className='container')
        ],
            className='main-content-inner'),
        # html.Div([
        #     html.Div([
        #         html.A([
        #             html.Img(src='https://i.gyazo.com/ddeb81c9645852e6d93fb49d9679b3e8.png')
        #         ])
        #     ])
        # ], className='col-lg-12'),
    ],
    className='horizontal-main-wrapper'),
    #footer
    footer.footer()
],
className='body-bg')
# ================== END ABOUT LAYOUT ================== #