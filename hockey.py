import sys
from yattag import Doc, indent

# volokit link format template
# http://www.volokit.com/all-games/nhl/Detroit.php

# all NHL teams -> cities -> volokit key
### Eastern Conference
## Atlantic Division
# Boston Bruins -> Boston, Massachusetts -> Boston
boston_link_value = "Boston"
# Buffalo Sabres -> Buffalo, New York -> Buffalo
buffalo_link_value = "Buffalo"
# Detroit Red Wings -> Detroit, Michigan -> Detroit
detroit_link_value = "Detroit"
# Florida Panthers -> Sunrise, Florida -> Florida
florida_link_value = "Florida"
# Montreal Canadiens -> Montreal, Quebec -> Montreal
montreal_link_value = "Montreal"
# Ottawa Senators -> Ottawa, Ontario -> Ottawa
ottawa_link_value = "Ottawa"
# Tampa Bay Lightning -> Tampa, Florida ->
# Toronto Maple Leafs -> Toronto, Ontario -> Toronto
toronto_link_value = "Toronto"
##  Metropolitan Division
# Carolina Hurricanes -> Raleigh, North Carolina ->
# Columbus Blue Jackets -> Columbus, Ohio ->
# New Jersey Devils -> Newark, New Jersey ->
# New York Islanders -> New York City, New York ->
# Philadelphia Flyers -> Philadelphia, Pennsylvania -> Philadelphia
philadelphia_link_value = "Philadelphia"
# Pittsburgh Penguins -> Pittsburgh, Pennsylvania ->
# Washington Capitals -> Washington, D.C. ->
### Western Conference
## Central Division
# Chicago Blackhawks -> Chicago, Illinois -> Chicago
chicago_link_value = "Chicago"
# Colorado Avalanche -> Denver, Colorado ->
# Dallas Stars -> Dallas, Texas ->
# Minnesota Wild -> Saint Paul, Minnesota -> Minnesota
minnesota_link_value = "Minnesota"
# Nashville Predators -> Nashville, Tennessee ->
# St. Louis Blues -> St. Louis, Missouri ->
# Winnipeg Jets -> Winnipeg, Manitoba -> Winnipeg
winnipeg_link_value = "Winnipeg"
## Pacific Division
# Anaheim Ducks -> Anaheim, California ->
# Arizona Coyotes -> Glendale, Arizona ->
# Calgary Flames -> Calgary, Alberta ->
# Edmonton Oilers -> Edmonton, Alberta ->
# Los Angeles Kings -> Los Angeles, California -> Los-Angeles
los_angeles_link_value = "Los-Angeles"
# San Jose Sharks -> San Jose, California ->
# Vancouver Canucks -> Vancouver, British Columbia -> Vancouver
vancouver_link_value = "Vancouver"
# Vegas Golden Knights -> Paradise, Nevada -> Vegas
vegas_link_value = "Vegas"
# Seattle -> Seattle, Washington ->

team_names = {
    # Atlantic Division
    "boston": boston_link_value, "bruins": boston_link_value,
    "buffalo": buffalo_link_value, "sabres": buffalo_link_value,
    "detroit": detroit_link_value, "wings": detroit_link_value, "redwings": detroit_link_value,
    "florida": florida_link_value, "panthers": florida_link_value,
    "montreal": montreal_link_value, "canadiens": montreal_link_value,
    "ottawa": ottawa_link_value, "senators": ottawa_link_value,
    "tampabay": "", "tampa": "", "lightning": "",
    "toronto": toronto_link_value, "mapleleafs": toronto_link_value, "leafs": toronto_link_value,
    # Metropolitan Division
    "carolina": "", "hurricanes": "",
    "columbus": "", "bluejackets": "", "jackets": "",
    "newjersey": "", "jersey": "", "devils": "",
    "newyork": "", "islanders": "",
    "philadelphia": philadelphia_link_value, "philly": philadelphia_link_value, "flyers": philadelphia_link_value,
    "pittsburgh": "", "penguins": "",
    "washington": "", "capitals": "",
    # Central Division
    "chicago": chicago_link_value, "blackhawks": chicago_link_value,
    "colorado": "", "avalanche": "",
    "dallas": "", "stars": "",
    "minnesota": minnesota_link_value, "wild": minnesota_link_value,
    "nashville": "", "predators": "",
    "stlouis": "", "louis": "", "blues": "",
    "winnipeg": winnipeg_link_value, "jets": winnipeg_link_value,
    # Pacific Division
    "anaheim": "", "ducks": "",
    "arizona": "", "coyotes": "",
    "calgary": "", "flames": "",
    "edmonton": "", "oilers": "",
    "losangeles": los_angeles_link_value, "angeles": los_angeles_link_value, "kings": los_angeles_link_value,
    "sanjose": "", "jose": "", "sharks": "",
    "vancouver": vancouver_link_value, "canucks": vancouver_link_value,
    "vegas": vegas_link_value, "lasvegas": vegas_link_value, "goldenknights": vegas_link_value, "knights": vegas_link_value,
    "seattle": "", "": "",
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
        team_link = format_link(team)
        with tag('h4', style="margin:0px;height:4%"):
            with tag('a', href=team_link):
                text(team)
        with tag('iframe', src=team_link, style="height:95%;width:100%"):
            text("")

def build_two_team(teams):
    with tag('div', style="display:table;height:100%;width:100%"):
        with tag('div', style="display:table-row"):
            for team in teams:
                team_link = format_link(team)
                with tag('div', style="display:table-cell"):
                    with tag('h4', style="margin:0px;height:4%"):
                        with tag('a', href=team_link):
                            text(team)
                    with tag('iframe', src=team_link, style="height:95%;width:100%"):
                        text("")

def build_four_team(teams):
    with tag('div', style="display:table;height:100%;width:100%"):
        team_index = 0
        for row in range(0,2):
            with tag('div', style="display:table-row"):
                for col in range(0,2):
                    with tag('div', style="display:table-cell"):
                        team_link = format_link(teams[team_index])
                        with tag('h4', style="margin:0px;height:4%"):
                            with tag('a', href=team_link):
                                text(teams[team_index])
                        with tag('iframe', src=team_link, style="height:95%;width:100%"):
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

file = open(output_filename, "w")
file.write(indent(doc.getvalue()))
file.close()
