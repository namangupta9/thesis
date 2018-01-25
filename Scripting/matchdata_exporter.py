# Import Necessary Modules & Libraries
import pandas as pd
import os
import datetime
import pandas as pd
import json

# Final Dict; Basic Identifying Info + Match Event TIMES


def export_match_data(teams, season_in):

    os.chdir("/Users/namangupta/Documents/[2014-2018] Michigan/Thesis/Codebase/Match Information")

    for team in teams:

        # Initialize Values
        filename = team.file_name + str("_matches_") + str(season_in[5:]) + str(".csv")
        fix_data = []

        # Massive Logic Branch, Open At Your Own Risk
        for fix in team.fixtures:

            # Parse KickOff DateTime
            kt = datetime.datetime.strptime(fix.time, "%H:%M:%S")

            fixture_final_data = {
                "date": fix.date,
                "home_side": fix.home_api_id,
                "away_side": fix.away_api_id,
                "avg_h_odds": fix.average_odds.home,
                "avg_d_odds": fix.average_odds.draw,
                "avg_a_odds": fix.average_odds.away,
                "kickoff_time": kt.time(),
                "home_goals": [],
                "away_goals": [],
                "disallowed_goals": [],
                "home_reds": [],
                "home_yellows": [],
                "away_reds": [],
                "away_yellows": []
            }

            # Split Event Lists into 1st Half & 2nd Half
            home_first_half_goals = [goal for goal in fix.home_goal_times if goal <= 45]
            home_second_half_goals = [goal for goal in fix.home_goal_times if (goal <= 90 and goal > 45)]

            away_first_half_goals = [goal for goal in fix.away_goal_times if goal <= 45]
            away_second_half_goals = [goal for goal in fix.away_goal_times if (goal <= 90 and goal > 45)]

            disallowed_first_half_goals = [goal for goal in fix.disallowed_goals if goal <= 45]
            disallowed_second_half_goals = [goal for goal in fix.disallowed_goals if (goal <= 90 and goal > 45)]

            home_yc_first = [yc for yc in fix.home_yc_times if yc <= 45]
            home_rc_first = [rc for rc in fix.home_rc_times if rc <= 45]
            away_yc_first = [yc for yc in fix.away_yc_times if yc <= 45]
            away_rc_first = [rc for rc in fix.away_rc_times if rc <= 45]

            home_yc_second = [yc for yc in fix.home_yc_times if (yc <= 90 and yc > 45)]
            home_rc_second = [rc for rc in fix.home_rc_times if (rc <= 90 and rc > 45)]
            away_yc_second = [yc for yc in fix.away_yc_times if (yc <= 90 and yc > 45)]
            away_rc_second = [rc for rc in fix.away_rc_times if (rc <= 90 and rc > 45)]

            # HOME TEAM - FIRST HALF GOALS
            for goal in home_first_half_goals:
                gt = kt + datetime.timedelta(minutes=goal)
                fixture_final_data["home_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.home_ht_stoppage_goals:
                fixture_final_data["home_goals"] = fixture_final_data["home_goals"][:-1]

            #  Add Them Back In
            for goal in fix.home_ht_stoppage_goals:
                gt = kt + datetime.timedelta(minutes=(45 + goal))
                fixture_final_data["home_goals"].append(str(gt.time()))

            # AWAY TEAM - FIRST HALF GOALS
            for goal in away_first_half_goals:
                gt = kt + datetime.timedelta(minutes=goal)
                fixture_final_data["away_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.away_ht_stoppage_goals:
                fixture_final_data["away_goals"] = fixture_final_data["away_goals"][:-1]

            #  Add Them Back In
            for goal in fix.away_ht_stoppage_goals:
                gt = kt + datetime.timedelta(minutes=(45 + goal))
                fixture_final_data["away_goals"].append(str(gt.time()))

            # DISALLOWED - FIRST HALF GOALS
            for goal in disallowed_first_half_goals:
                gt = kt + datetime.timedelta(minutes=goal)
                fixture_final_data["disallowed_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.disallowed_goals_ht_stoppage:
                fixture_final_data["disallowed_goals"] = fixture_final_data["disallowed_goals"][:-1]

            #  Add Them Back In
            for goal in fix.disallowed_goals_ht_stoppage:
                gt = kt + datetime.timedelta(minutes=(45 + goal))
                fixture_final_data["disallowed_goals"].append(str(gt.time()))

            # BOOKINGS
            for c in home_yc_first:
                gt = kt + datetime.timedelta(minutes=c)
                fixture_final_data["home_yellows"].append(str(gt.time()))

            for c in away_yc_first:
                gt = kt + datetime.timedelta(minutes=c)
                fixture_final_data["away_yellows"].append(str(gt.time()))

            for c in home_rc_first:
                gt = kt + datetime.timedelta(minutes=c)
                fixture_final_data["home_reds"].append(str(gt.time()))

            for c in away_rc_first:
                gt = kt + datetime.timedelta(minutes=c)
                fixture_final_data["away_reds"].append(str(gt.time()))

            # Calculate Estimated Start of 2nd Half
            ht = kt + datetime.timedelta(minutes=45)
            ht += datetime.timedelta(minutes=3)            #TO BE SCRAPED...
            ht += datetime.timedelta(minutes=15)

            # HOME TEAM - SECOND HALF GOALS
            for goal in home_second_half_goals:
                adjusted_goal_time = goal - 45
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["home_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.home_ft_stoppage_goals:
                fixture_final_data["home_goals"] = fixture_final_data["home_goals"][:-1]

            #  Add Them Back In
            for goal in fix.home_ft_stoppage_goals:
                adjusted_goal_time = goal - 45 + 90
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["home_goals"].append(str(gt.time()))

            # AWAY TEAM - SECOND HALF GOALS
            for goal in away_second_half_goals:
                adjusted_goal_time = goal - 45
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["away_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.away_ft_stoppage_goals:
                fixture_final_data["away_goals"] = fixture_final_data["away_goals"][:-1]

            #  Add Them Back In
            for goal in fix.away_ft_stoppage_goals:
                adjusted_goal_time = goal - 45 + 90
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["away_goals"].append(str(gt.time()))

            # DISALLOWED - SECOND HALF GOALS
            for goal in disallowed_second_half_goals:
                adjusted_goal_time = goal - 45
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["disallowed_goals"].append(str(gt.time()))

            #  Remove Goals Scored in Stoppage Time
            for goal in fix.disallowed_goals_ft_stoppage:
                fixture_final_data["disallowed_goals"] = fixture_final_data["disallowed_goals"][:-1]

            #  Add Them Back In
            for goal in fix.disallowed_goals_ft_stoppage:
                adjusted_goal_time = goal - 45 + 90
                gt = ht + datetime.timedelta(minutes=adjusted_goal_time)
                fixture_final_data["disallowed_goals"].append(str(gt.time()))

            # BOOKINGS
            for c in home_yc_second:
                adjusted_card_time = c - 45
                gt = ht + datetime.timedelta(minutes=adjusted_card_time)
                fixture_final_data["home_yellows"].append(str(gt.time()))

            for c in away_yc_second:
                adjusted_card_time = c - 45
                gt = ht + datetime.timedelta(minutes=adjusted_card_time)
                fixture_final_data["away_yellows"].append(str(gt.time()))

            for c in home_rc_second:
                adjusted_card_time = c - 45
                gt = ht + datetime.timedelta(minutes=adjusted_card_time)
                fixture_final_data["home_reds"].append(str(gt.time()))

            for c in away_rc_second:
                adjusted_card_time = c - 45
                gt = ht + datetime.timedelta(minutes=adjusted_card_time)
                fixture_final_data["away_reds"].append(str(gt.time()))


            # Convert Lists of Datetime.Time Objects to Strings

            # Finally Done w/ This Fixture
            fix_data.append(fixture_final_data)

        # Export
        df = pd.DataFrame(fix_data)
        df.to_csv(filename)

        print "Exported Match Data: " + filename

    os.chdir("/Users/namangupta/Documents/[2014-2018] Michigan/Thesis/Codebase")
