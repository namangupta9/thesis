"""helper functions for the creation of interactive viz website."""

# Naman Gupta
# namangupta.co
# 2018

import plotly.graph_objs as go
import sys


def get_club_dropdowns():
    """Return a list of dicts of dropdown options, one for each club."""
    dropdowns = []

    # iterate through file, create new dropdown option for each club
    with open("../teams.txt", 'r') as file:
        for c in file:
            names = c.split(", ")
            dropdowns.append({'label': names[1],
                              'value': names[0]})

    return dropdowns


def get_relevant_data(search_vol_df, match_dropdown):
    """Return a list of scatter plot objects to visualize search volumes."""
    data = []

    match_searches = search_vol_df.loc[search_vol_df["date"] == match_dropdown]

    data.append(go.Scatter(
                    x=match_searches.time,
                    y=match_searches.iloc[:, 1],
                    name="Official Name, Unscaled",
                    line=dict(color='#c9c7c7'),
                    opacity=0.8))

    data.append(go.Scatter(
                    x=match_searches.time,
                    y=match_searches.iloc[:, 2],
                    name="Shorthand",
                    line=dict(color='#7F7F7F'),
                    opacity=0.8))

    return data


def get_match_event_lines(match_info_df, m_drop):
    """Return a list of line objects to mark individual match events."""
    lines = []

    # relevant_match_info
    relevant_match_info = match_info_df[match_info_df["date"] == m_drop]

    # for debugging purposes
    sys.stderr.write("GETTING MATCH EVENTS:" + '\n')

    # kickoff time & estimated end time
    # end time estimated as:
    # (kickoff + 90' + 6' est. total stoppage time + 15' Halftime)
    #  / 8 (graph scale)
    sys.stderr.write("..GETTING KICKOFF TIME" + '\n')
    kt = relevant_match_info["kickoff_time"].iloc[0]
    kt_float = float((int(kt[0:2]) * 60) + (int(kt[3:5])) - 64) / 8
    lines.append({
            'type': 'rect',
            'x0': kt_float,
            'y0': 0,
            'x1': kt_float + 13.875,
            'y1': 100,
            'fillcolor': 'rgb(55, 128, 191)',
            'opacity': 0.1,
            'line': {'width': 0}
            })

    # home goals
    sys.stderr.write("..GETTING HOME GOALS" + '\n')
    for goal in relevant_match_info["home_goals"].iloc[0]:
        hg_float = float((int(goal[0:2]) * 60) + (int(goal[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': hg_float,
                'y0': 0,
                'x1': hg_float,
                'y1': 100,
                'line': {
                    'color': '#50f441',
                    'width': 2}
                })

    # away goals
    sys.stderr.write("..GETTING AWAY GOALS" + '\n')
    for goal in relevant_match_info["away_goals"].iloc[0]:
        ag_float = float((int(goal[0:2]) * 60) + (int(goal[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': ag_float,
                'y0': 0,
                'x1': ag_float,
                'y1': 100,
                'line': {
                    'color': '#4158f4',
                    'width': 2}
                })

    # home red cards
    sys.stderr.write("..GETTING HOME REDS" + '\n')
    for card in relevant_match_info["home_reds"].iloc[0]:
        hr_float = float((int(card[0:2]) * 60) + (int(card[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': hr_float,
                'y0': 0,
                'x1': hr_float,
                'y1': 100,
                'line': {
                    'color': 'red',
                    'width': 1}
                })

    # home yellow cards
    sys.stderr.write("..GETTING HOME YELLOWS" + '\n')
    for card in relevant_match_info["home_yellows"].iloc[0]:
        hy_float = float((int(card[0:2]) * 60) + (int(card[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': hy_float,
                'y0': 0,
                'x1': hy_float,
                'y1': 100,
                'line': {
                    'color': 'yellow',
                    'width': 1}
                })

    # away red cards
    sys.stderr.write("..GETTING AWAY REDS" + '\n')
    for card in relevant_match_info["away_reds"].iloc[0]:
        ar_float = float((int(card[0:2]) * 60) + (int(card[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': ar_float,
                'y0': 0,
                'x1': ar_float,
                'y1': 100,
                'line': {
                    'color': 'red',
                    'width': 1}
                })

    # away yellow cards
    sys.stderr.write("..GETTING AWAY YELLOWS" + '\n')
    for card in relevant_match_info["away_yellows"].iloc[0]:
        ay_float = float((int(card[0:2]) * 60) + (int(card[3:5])) - 64) / 8
        lines.append({
                'type': 'line',
                'x0': ay_float,
                'y0': 0,
                'x1': ay_float,
                'y1': 100,
                'line': {
                    'color': 'yellow',
                    'width': 1}
                })

    return lines
