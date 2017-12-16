import trends_scraper
from trends_scraper import Club

import matchdata_exporter

# MAIN PROGRAM DRIVER
def main(season_in) :

    # Declare Teams
    # [Official Name, Shorthand (Taken from Google's EPL Tables)]
    teams = []
    teams.append(Club("afc_bournemouth", "Bournemouth", ["Association Football Club Bournemouth", "Bournemouth"]))
    teams.append(Club("arsenal", "Arsenal", ["Arsenal Football Club", "Arsenal"]))
    teams.append(Club("aston_villa", "Aston Villa", ["Aston Villa Football Club", "Aston Villa"]))
    teams.append(Club("chelsea", "Chelsea", ["Chelsea Football Club", "Chelsea"]))
    teams.append(Club("crystal_palace", "Crystal Palace", ["Crystal Palace Football Club", "Crystal Palace"]))
    teams.append(Club("everton", "Everton", ["Everton Football Club", "Everton"]))
    teams.append(Club("leicester_city", "Leicester", ["Leicester City Football Club", "Leicester City"]))
    teams.append(Club("liverpool", "Liverpool", ["Liverpool Football Club", "Liverpool"]))
    teams.append(Club("manchester_city", "Manchester City", ["Manchester City Football Club", "Man City"]))
    teams.append(Club("manchester_united", "Manchester United", ["Manchester United Football Clubs", "Man United"]))
    teams.append(Club("newcastle_united", "Newcastle United", ["Newcastle United Football Club", "Newcastle"]))
    teams.append(Club("norwich_city", "Norwich", ["Norwich City Football Club", "Norwich City"]))
    teams.append(Club("southampton", "Southampton", ["Southampton Football Club", "Southampton"]))
    teams.append(Club("stoke_city", "Stoke", ["Stoke City Football Club", "Stoke City"]))
    teams.append(Club("sunderland", "Sunderland", ["Sunderland Football Club", "Sunderland"]))
    teams.append(Club("swansea_city", "Swansea", ["Swansea City Football Club", "Swansea City"]))
    teams.append(Club("tottenham", "Tottenham", ["Tottenham Hotspur Football Club", "Tottenham"]))
    teams.append(Club("watford", "Watford", ["Watford Football Club", "Watford"]))
    teams.append(Club("west_brom", "West Bromwich Albion", ["West Bromwich Albion Football Club", "West Brom"]))
    teams.append(Club("west_ham", "West Ham", ["West Ham Football Club", "West Ham"]))

    # Scrape Match Data
    trends_scraper.scrape_match_data(season_in, teams)

    # Export Match Data
    matchdata_exporter.export_match_data(teams, season_in)

    # # Search & Export Volume Data (Needs to be done after match data scraped!)
    # trends_scraper.scrape_volume_data(season_in, "matchday", teams)
    # trends_scraper.scrape_volume_data(season_in, "match", teams)
    # trends_scraper.scrape_volume_data(season_in, "matchweekend", teams)

    print "Finished Execution."

# EXECUTION
main("2015/2016")
