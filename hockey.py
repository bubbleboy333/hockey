import sys
from yattag import Doc

# volokit link format template
# http://www.volokit.com/all-games/nhl/Detroit.php

# all NHL teams -> cities -> volokit key
### Eastern Conference
## Atlantic Division
# Boston Bruins -> Boston, Massachusetts -> Boston
# Buffalo Sabres -> Buffalo, New York -> Buffalo
# Detroit Red Wings -> Detroit, Michigan -> Detroit
# Florida Panthers -> Sunrise, Florida -> Florida
# Montreal Canadiens -> Montreal, Quebec -> Montreal
# Ottawa Senators -> Ottawa, Ontario -> Ottawa
# Tampa Bay Lightning -> Tampa, Florida ->
# Toronto Maple Leafs -> Toronto, Ontario -> Toronto
##  Metropolitan Division
# Carolina Hurricanes -> Raleigh, North Carolina ->
# Columbus Blue Jackets -> Columbus, Ohio ->
# New Jersey Devils -> Newark, New Jersey ->
# New York Islanders -> New York City, New York ->
# Philadelphia Flyers -> Philadelphia, Pennsylvania ->
# Pittsburgh Penguins -> Pittsburgh, Pennsylvania ->
# Washington Capitals -> Washington, D.C. ->
### Western Conference
## Central
# Chicago Blackhawks -> Chicago, Illinois ->
# Colorado Avalanche -> Denver, Colorado ->
# Dallas Stars -> Dallas, Texas ->
# Minnesota Wild -> Saint Paul, Minnesota ->
# Nashville Predators -> Nashville, Tennessee ->
# St. Louis Blues -> St. Louis, Missouri ->
# Winnipeg Jets -> Winnipeg, Manitoba ->
## Pacific
# Anaheim Ducks -> Anaheim, California ->
# Arizona Coyotes -> Glendale, Arizona ->
# Calgary Flames -> Calgary, Alberta ->
# Edmonton Oilers -> Edmonton, Alberta ->
# Los Angeles Kings -> Los Angeles, California ->
# San Jose Sharks -> San Jose, California ->
# Vancouver Canucks -> Vancouver, British Columbia ->
# Vegas Golden Knights -> Paradise, Nevada ->
# Seattle -> Seattle, Washington ->

team_names = {
    "": "",
    "boston": "Boston",
    "bruins": "Boston",
    "buffalo": "Buffalo",
    "sabres": "Buffalo",
    "red wings": "Detroit",
    "redwings": "Detroit",
    "detroit": "Detroit",
    "florida": "Florida",
    "panthers": "Florida",
    "montreal": "Montreal",
    "canadiens": "Montreal",
}
# number of arguments on CLI before team names
num_pre_team_args = 1
link_template = "http://www.volokit.com/all-games/nhl/{}.php"

output_filename = "hockey.html"
doc, tag, text = Doc().tagtext()

def get_scrubbed_team_name(rough_name):
    return team_names[rough_name.lower()]

def build_team_list(num_teams):
    teams = []
    for i in range(0, num_teams):
        teams.append(get_scrubbed_team_name(sys.argv[i+num_pre_team_args]))
    return teams

def format_link(team):
    return link_template.format(team)

def build_one_team(teams):
    for team in teams:
        with tag('h4', style="margin:0px;height:4%"):
            text(team)
        with tag('iframe', src=format_link(team), style="height:95%;width:100%"):
            text("")

def build_two_team(teams):
    with tag('div', style="display:table;height:100%;width:100%"):
        with tag('div', style="display:table-row"):
            for team in teams:
                with tag('div', style="display:table-cell"):
                    with tag('h4', style="margin:0px;height:4%"):
                        text(team)
                    with tag('iframe', src=format_link(team), style="height:90%;width:100%"):
                        text("")

def build_four_team(teams):
    with tag('div', style="display:table;height:100%;width:100%"):
        team_index = 0
        for row in range(0,2):
            with tag('div', style="display:table-row"):
                for col in range(0,2):
                    with tag('div', style="display:table-cell"):
                        with tag('h4', style="margin:0px;height:4%"):
                            text(teams[team_index])
                        with tag('iframe', src=format_link(teams[team_index]), style="height:90%;width:100%"):
                            text("")
                    team_index += 1

def build_document(teams):
    num_teams = len(teams)
    if num_teams == 1:
        build_one_team(teams)
    elif num_teams == 2:
        build_two_team(teams)
    elif num_teams == 4:
        build_four_team(teams)


### Main
# sys.argv[0] hockey.py
team_count = len(sys.argv) - num_pre_team_args # subtract out program name
# only support 4 streams/windows at a time
if team_count > 4:
    raise Exception("too many games at a time. max 4")
teams = build_team_list(team_count)
print(teams)

# building document
build_document(teams)

print(doc.getvalue())
file = open(output_filename, "w")
file.write(doc.getvalue())
file.close()
