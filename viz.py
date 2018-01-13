"""handles creation of an interactive data visualization page for thesis."""

# Naman Gupta
# namangupta.co
# 2018

import pandas as pd

# coding: utf-8
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# start
app = dash.Dash()


def get_club_dropdowns():
    """Return a list of dicts of dropdown options, one for each club."""
    dropdowns = []

    # iterate through file, create new dropdown option for each club
    with open("teams.txt", 'r') as file:
        for c in file:
            names = c.split(", ")
            dropdowns.append({'label': names[1],
                              'value': names[0]})

    return dropdowns


# css; use rawgit.com to serve raw files directly from github repo
# dash only allows the usage of externally-hosted css & javascript for now
my_css_url = "https://rawgit.com/namangupta9/thesis/master/viz_css.css"
app.css.append_css({"external_url": my_css_url})

# generate html layout
app.layout = html.Div(children=[

    # heading
    html.H1(children='Senior Thesis: EPL Analytics'),
    html.Div(children='Naman Gupta, Eric Schwartz', id="authors"),
    html.Div(children='''
        How might various match events in the English Premier League affect
        normalized Google search activity?''', id="description"),

    # dropdown to select club
    html.Div([
        dcc.Dropdown(
            id='club-dropdown',
            options=get_club_dropdowns(),
        ),
    ], style={'width': '500'}),

    # another dropdown to select match from club's fixture list
    html.Div([
        dcc.Dropdown(
            id='match-dropdown',
            ),
    ], style={'width': '500'}),

    # graph to display match chart
    dcc.Graph()
    ]
)


@app.callback(Output('match-dropdown', 'options'),
              [Input('club-dropdown', 'value')])
def get_match_dropdowns(input_value):
    """Return a list of dicts of dropdown options, one for each match."""
    dropdowns = []

    # load club's match information
    info_filepath = "Match Information/" + input_value + "_matches_2016.csv"
    df = pd.read_csv(info_filepath)

    # iterate through dates to create dropdown options
    dates = df["date"]
    for date in dates:
        dropdowns.append({'label': date,
                          'value': date})

    return dropdowns


# @app.callback(Output('match-chart', 'figure'),
#               [Input('club-dropdown', 'value'),
#                Input('match-dropdown', 'value')])
# def get_match_chart(club_dropdown, match_dropdown):
#     """Plot a figure based on the selected club & match."""
#
#     # load search volume data frame & select relevant area TODO
#
#     # load match information data frame & select relevant area TODO
#
#     # using search volume & match information data, plot! TODO


# execution
if __name__ == '__main__':
    app.run_server(debug=False)
