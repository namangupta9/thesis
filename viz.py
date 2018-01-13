"""handles creation of an interactive data visualization page for thesis."""

# Naman Gupta
# namangupta.co
# 2018

import pandas as pd
from ast import literal_eval
from viz_helpers import get_club_dropdowns
from viz_helpers import get_relevant_data
from viz_helpers import get_match_event_lines

# coding: utf-8
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

# start
app = dash.Dash()

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
            value="Chelsea"
        ),
    ], style={'width': '500'}),

    # another dropdown to select match from club's fixture list
    html.Div([
        dcc.Dropdown(
            id='match-dropdown',
            ),
    ], style={'width': '500'}),

    # graph to display match chart
    html.Div([
        dcc.Graph(
            id='match-chart',
            ),
    ], style={'width': '500'})]
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


@app.callback(Output('match-chart', 'figure'),
              [Input('club-dropdown', 'value'),
               Input('match-dropdown', 'value')])
def get_match_chart(club_dropdown, match_dropdown):
    """Plot a figure based on the selected club & match."""
    # load search volume & match information data frames
    search_file = club_dropdown + "_match_2016.csv"
    info_file = club_dropdown + "_matches_2016.csv"
    search_df = pd.read_csv("Matchday Volumes/" + search_file)
    info_df = pd.read_csv("Match Information/" + info_file)

    # some preliminary data formatting
    search_df['time'] = search_df.apply(lambda row: row.date[-8:], axis=1)
    search_df['date'] = search_df.apply(lambda row: row.date[:-9], axis=1)
    search_df = search_df[search_df.time != "00:00:00"]

    # format match event timestamps
    info_df["away_goals"] = info_df["away_goals"].apply(
                            lambda x: literal_eval(x))
    info_df["home_goals"] = info_df["home_goals"].apply(
                            lambda x: literal_eval(x))
    info_df["disallowed_goals"] = info_df["disallowed_goals"].apply(
                                  lambda x: literal_eval(x))
    info_df["home_reds"] = info_df["home_reds"].apply(
                           lambda x: literal_eval(x))
    info_df["away_reds"] = info_df["away_reds"].apply(
                           lambda x: literal_eval(x))
    info_df["home_yellows"] = info_df["home_yellows"].apply(
                              lambda x: literal_eval(x))
    info_df["away_yellows"] = info_df["away_yellows"].apply(
                              lambda x: literal_eval(x))

    # using search volume & match information data, plot!
    layout = go.Layout(
        xaxis=dict(showgrid=True, zeroline=False, showline=True),
        yaxis=dict(showgrid=True, zeroline=False, showline=True),
        shapes=get_match_event_lines(info_df, match_dropdown)
    )

    fig = plotly.graph_objs.Figure(data=get_relevant_data(search_df,
                                                          match_dropdown),
                                   layout=layout)
    plotly.offline.iplot(fig)


# execution
if __name__ == '__main__':
    app.run_server(debug=False)
