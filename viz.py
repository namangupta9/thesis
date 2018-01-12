"""handles the creation of an interactive data visualization page for thesis"""

# Naman Gupta
# namangupta.co
# 2018

# coding: utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html

# start
app = dash.Dash()

# css
app.css.append_css({
        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
        })

# generate html layout
app.layout = html.Div(children=[
    html.H1(children='Senior Thesis - Visualization'),

    html.Div(children='''
        EPL Analytics: Exploring how different match events affect
        normalized Google search activity levels.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3],
                 'y': [4, 1, 2],
                 'type': 'bar',
                 'name': 'SF'},
                {'x': [1, 2, 3],
                 'y': [2, 4, 5],
                 'type': 'bar',
                 'name': u'Montreal'},
                 ],
            'layout': {
                'title': 'Dash Data Visualization'
                }
            }
        )
    ]
)

# execution
if __name__ == '__main__':
    app.run_server(debug=False)
