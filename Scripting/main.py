import trends_scraper
from trends_scraper import Club

import matchdata_exporter

# MAIN PROGRAM DRIVER
def main(season_in) :

    # Load Teams
    # [Official Name, Shorthand (Taken from Google's EPL Tables)]
    teams = []
    with open("teams.txt", 'r') as file:
        for c in file:
            names = c.split(', ')
            teams.append(Club(names[0], names[1], names[2:]))

    # Scrape Match Data
    trends_scraper.scrape_match_data(season_in, teams)

    # Export Match Data
    matchdata_exporter.export_match_data(teams, season_in)

    # # Search & Export Volume Data (Needs to be done after match data scraped!)
    # trends_scraper.scrape_volume_data(season_in, "matchday", teams)
    trends_scraper.scrape_volume_data(season_in, "match", teams)
    # trends_scraper.scrape_volume_data(season_in, "matchweekend", teams)

    print "Finished Execution."

# EXECUTION
main("2015/2016")
