# Import Necessary Modules & Libraries
import pandas as pd
from pytrends.request import TrendReq
import sqlite3
import anymarkup
import csv
import os
import datetime

print "-----------------------------------------------"
print "Senior Thesis - Google Trends Script"
print "By: Naman Gupta"
print "Advisor: Professor Eric Schwartz"
print "-----------------------------------------------"


# CLASS DECLARATIONS
class Odds:
    home = None
    draw = None
    away = None

    def __init__(self, home_in, draw_in, away_in):
        self.home = home_in
        self.draw = draw_in
        self.away = away_in

class Fixture :

    # Basic Fixture Data
    date = None
    time = None
    fixture_api_id = None
    home_api_id = None
    away_api_id = None

    # Home & Away Goals (& Stoppage Time Additions)
    home_goal_times = None
    away_goal_times = None
    home_ht_stoppage_goals = None
    away_ht_stoppage_goals = None
    home_ft_stoppage_goals = None
    away_ft_stoppage_goals = None

    # Disallowed Goals
    disallowed_goals = None
    disallowed_goals_ht_stoppage = None
    disallowed_goals_ft_stoppage = None

    # Bookings
    home_rc_times = None
    away_rc_times = None
    home_yc_times = None
    away_yc_times = None

    # Betting Odds: Bet 365 & Ladbrokes
    bet_365_odds = None
    ladbrokes_odds = None
    betway_odds = None
    william_hill_odds = None
    paddy_odds = None
    average_odds = None

    def __init__(self, date_and_time, fixture_api_id_in, home_api_id_in, away_api_id_in):
        self.fixture_api_id = fixture_api_id_in
        self.home_api_id = home_api_id_in
        self.away_api_id = away_api_id_in
        self.date, self.time = parse_date_time(date_and_time)

class Club :
    # Output-Related
    file_name = None

    # SQL-Database Related
    api_id = None
    api_name = None
    fixtures = []

    # Google Trends-Related
    keywords = []

    def __init__(self, file_name_in, api_name_in, keywords_in):
        self.file_name = file_name_in
        self.api_name = api_name_in
        self.keywords = keywords_in


# HELPER FUNCTION IMPLEMENTATIONS
def get_api_ids(db, teams):

    # Loop Through All EPL Teams
    for team in teams:
        t = team.api_name
        t = (t,)
        db.execute("SELECT team_api_id, team_long_name FROM Team WHERE team_long_name=?", t)
        team.api_id = db.fetchone()[0]


def average_odds(odds_list_in):

    count = 0
    sum_home = 0
    sum_draw = 0
    sum_away = 0

    for odd in odds_list_in:
        try:
            sum_home += odd.home
            sum_draw += odd.draw
            sum_away += odd.away
            count += 1

        except:
            donothing = 'a'

    if (count > 0):
        avg = Odds((float(sum_home) / count), (float(sum_draw) / count), (float(sum_away) // count))
        return avg
    else:
        avg = Odds(-1, -1, -1)
        return avg


def get_fixtures(db, season_in, teams):

    # Invariant: By this point, every Team object will have a valid api_id member
    for team in teams:
        team.fixtures = []
        p = (team.api_id, team.api_id, season_in)

        statement = "SELECT date, match_api_id, home_team_api_id, away_team_api_id"
        statement += (", B365H, B365D, B365A, LBH, LBD, LBA, BWH, BWD, BWA, WHH, WHD, WHA, PSH, PSD, PSA ")
        statement += ("FROM Match ")
        statement += ("WHERE (home_team_api_id=? or away_team_api_id=?) and season=?  ")
        statement += ("ORDER BY date ")

        db.execute(statement, p)

        for r in db.fetchall():
            f = Fixture(r[0], r[1], r[2], r[3])                 # Basic Fixture Data

            f.bet_365_odds = Odds(r[4], r[5], r[6])             # Bet 365 Fixture Odds
            f.ladbrokes_odds = Odds(r[7], r[8], r[9])           # Ladbrokes Fixture Odds
            f.betway_odds = Odds(r[10], r[11], r[12])           # Betway Fixture Odds
            f.william_hill_odds = Odds(r[13], r[14], r[15])     # William Hill Fixture Odds
            f.paddy_odds = Odds(r[16], r[17], r[18])            # Paddypower Sport Fixture Odds

            f.average_odds = average_odds([f.bet_365_odds, f.ladbrokes_odds, f.betway_odds,
                                           f.william_hill_odds, f.paddy_odds])
            team.fixtures.append(f)


def get_match_events(db, teams):

    for team in teams:
        for fixture in team.fixtures:

            # Initialize Member Variables
            fixture.home_goal_times = []
            fixture.away_goal_times = []
            fixture.home_ht_stoppage_goals = []
            fixture.away_ht_stoppage_goals = []
            fixture.home_ft_stoppage_goals = []
            fixture.away_ft_stoppage_goals = []
            fixture.disallowed_goals = []
            fixture.disallowed_goals_ht_stoppage = []
            fixture.disallowed_goals_ft_stoppage = []
            fixture.home_rc_times = []
            fixture.away_rc_times = []
            fixture.away_yc_times = []
            fixture.home_yc_times = []

            statement = "SELECT goal "
            statement += ("FROM Match ")
            statement += ("WHERE match_api_id=? ")

            fixture_id = (fixture.fixture_api_id,)
            db.execute(statement, fixture_id)
            res = db.fetchone()

            # Only Proceed If There's Goals
            if (len(str(res[0])) > 8):

                goals = anymarkup.parse(str(res)[3:-3])['goal']['value']

                # If One Goal
                try:

                    # Disallowed Goal
                    if (goals['goal_type'] == 'dg'):
                        fixture.disallowed_goals.append(goals['elapsed'])

                        if (goals['elapsed'] == 45):
                            if 'elapsed_plus' in goals.keys():
                                fixture.disallowed_goals_ht_stoppage.append(goals['elapsed_plus'])
                        elif (goals['elapsed'] == 90):
                            if 'elapsed_plus' in goals.keys():
                                fixture.disallowed_goals_ft_stoppage.append(goals['elapsed_plus'])

                    # Home Team Scored
                    elif (goals['team'] == fixture.home_api_id):
                        fixture.home_goal_times.append(goals['elapsed'])

                        if (goals['elapsed'] == 45):
                            if 'elapsed_plus' in goals.keys():
                                fixture.home_ht_stoppage_goals.append(goals['elapsed_plus'])
                        elif (goals['elapsed'] == 90):
                            if 'elapsed_plus' in goals.keys():
                                fixture.home_ft_stoppage_goals.append(goals['elapsed_plus'])

                    # Away Team Scored
                    else:
                        fixture.away_goal_times.append(goals['elapsed'])

                        if (goals['elapsed'] == 45):
                            if 'elapsed_plus' in goals.keys():
                                fixture.away_ht_stoppage_goals.append(goals['elapsed_plus'])
                        elif (goals['elapsed'] == 90):
                            if 'elapsed_plus' in goals.keys():
                                fixture.away_ft_stoppage_goals.append(goals['elapsed_plus'])

                # Multiple Goals
                except:
                    for goal in goals:

                        # Disallowed Goal
                        if (goal['goal_type'] == 'dg'):
                            fixture.disallowed_goals.append(goal['elapsed'])

                            if (goal['elapsed'] == 45):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.disallowed_goals_ht_stoppage.append(goal['elapsed_plus'])
                            elif (goal['elapsed'] == 90):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.disallowed_goals_ft_stoppage.append(goal['elapsed_plus'])

                        # Home Team Scored
                        elif (goal['team'] == fixture.home_api_id):
                            fixture.home_goal_times.append(goal['elapsed'])

                            if (goal['elapsed'] == 45):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.home_ht_stoppage_goals.append(goal['elapsed_plus'])
                            elif (goal['elapsed'] == 90):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.home_ft_stoppage_goals.append(goal['elapsed_plus'])

                        # Away Team Scored
                        else:
                            fixture.away_goal_times.append(goal['elapsed'])

                            if (goal['elapsed'] == 45):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.away_ht_stoppage_goals.append(goal['elapsed_plus'])

                            elif (goal['elapsed'] == 90):
                                if 'elapsed_plus' in goal.keys():
                                    fixture.away_ft_stoppage_goals.append(goal['elapsed_plus'])


            statement = "SELECT card "
            statement += ("FROM Match ")
            statement += ("WHERE match_api_id=? ")

            db.execute(statement, fixture_id)
            res = db.fetchone()

            # Only Proceed If There's Bookings in Match
            if (len(str(res[0])) > 8):

                cards = anymarkup.parse(str(res)[3:-3])['card']['value']

                # If One Booking
                try:
                    if (cards['team'] == fixture.home_api_id):
                        if (cards['card_type'] == 'y'):
                            fixture.home_yc_times.append(cards['elapsed'])
                        else:
                            fixture.home_rc_times.append(cards['elapsed'])
                    else:
                        if (cards['card_type'] == 'y'):
                            fixture.away_yc_times.append(cards['elapsed'])
                        else:
                            fixture.away_rc_times.append(cards['elapsed'])

                # Multiple Goals
                except:
                    for card in cards:

                        try:
                            team_id = card['team'] # If this doesn't work, it means it's a dummy card in database. Skip.
                            if (team_id == fixture.home_api_id):
                                if (card['card_type'] == 'y'):
                                    fixture.home_yc_times.append(card['elapsed'])
                                else:
                                    fixture.home_rc_times.append(card['elapsed'])
                            else:
                                if (card['card_type'] == 'y'):
                                    fixture.away_yc_times.append(card['elapsed'])
                                else:
                                    fixture.away_rc_times.append(card['elapsed'])

                        except:
                            donothing = "a"


def parse_date_time(date_and_time_in):
    date = date_and_time_in[0:10]
    time = date_and_time_in[11:]
    return (date, time)


def assign_timestamps(mode_in, fixture_list_in):

    trends_timestamps = []

    if (mode_in == "matchday"):
        for fixture in fixture_list_in:
            date_timestamp = str(fixture.date) + "T01 " + str(fixture.date) + "T23"
            trends_timestamps.append(date_timestamp)

    if (mode_in == "match"):
        for fixture in fixture_list_in:

            start = int(fixture.time[:2]) - 2
            end = int(fixture.time[:2]) + 4

            date_timestamp = str(fixture.date) + "T" + str(start) + " " + str(fixture.date) + "T" + str(end)

            # Edge Case: Switch to Next Day T0 if at T24
            if (end == 24):

                og_date = datetime.datetime.strptime(str(fixture.date), "%Y-%m-%d")
                new_date = og_date + datetime.timedelta(days=1)

                date_timestamp = str(fixture.date) + "T" + str(start) + " " + str(new_date)[:10] + "T0"

            trends_timestamps.append(date_timestamp)

    return trends_timestamps


def scrape_match_data(season_in, teams):

    # Initialize Database Connection
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    # Scrape Match Data
    get_api_ids(c, teams)
    get_fixtures(c, season_in, teams)
    get_matchtimes(teams)
    get_match_events(c, teams)

    print "Scraped Match Data for All Teams."


def scrape_volume_data(season_in, mode_in, teams):

    # Create Pytrends Instance; Timezone 0 indicates GMT
    pytrend = TrendReq(hl='en-US', tz=0)

    # Collect & Concatenate Search Volume Data For All Teams
    for team in teams:

        # List to Store Fixture DataFrames
        dataframes = []

        # Ping API For Each Fixture
        api_fixture_list = assign_timestamps(mode_in, team.fixtures)
        counter = 0
        for fixture in api_fixture_list:
            pytrend.build_payload(kw_list=team.keywords, timeframe=fixture)
            interest_over_time_df = pytrend.interest_over_time()
            dataframes.append(interest_over_time_df)
            counter += 1

            print "Scraped Match " + str(counter)

        # Concatenate All Fixtures' Data
        season_df = pd.concat(dataframes)

        # Export Team's Data to CSV
        filename = str(team.file_name) + "_" + str(mode_in) + "_" + str(season_in[5:]) + ".csv"
        season_df.to_csv(filename)

        print "Exported " + str(team.file_name) + " Data" + "\n"


def get_matchtimes(teams):

    os.chdir("/Users/namangupta/Documents/[2014-2018] Michigan/Thesis/Codebase/Matchtimes")

    for c in teams:

        # Iterate Through All Teams
        fn = c.file_name + "_matchtimes.csv"
        with open(fn, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            count = 0

            # Iterate Through All Fixtures
            for row in reader:
                c.fixtures[count].time = str(row[0])
                count += 1

    print "Scraped Match Times for All Fixtures."

    # Revert Back to Original WD
    os.chdir("/Users/namangupta/Documents/[2014-2018] Michigan/Thesis/Codebase")
