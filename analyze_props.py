from draftkings import main as get_draftkings_props
from fanduel import main as get_fanduel_props
from prizepicks import main as get_prizepicks_props
from underdog import main as get_underdog_props
from datetime import datetime
import db

def main():
    prizepicks_props = get_prizepicks_props()
    draftkings_props = get_draftkings_props()
    fanduel_props = get_fanduel_props()
    underdog_props = get_underdog_props()
    return_props = []
    if prizepicks_props:
        for prop in prizepicks_props:
            """
            For each available PrizePicks bet, attempt to find it in stores of props from other sites.
            If found, look for discripencies in line or heavy favorites. Default values to -1 if not
            found in other dictionaries. Returns dictionary of 'good' bets. Includes timestamp.
            """
            player = prop
            prizepicks_prop_dict = prizepicks_props[prop]
            for stat in prizepicks_prop_dict:
                prizepicks_line = prizepicks_prop_dict[stat]
                num_lines_different = 0
                try:
                    underdog_line = underdog_props[player][stat]
                    if abs((underdog_line - prizepicks_line) >= 1):
                        num_lines_different += 1
                except:
                    underdog_line = -1
                try:
                    draftkings_line = draftkings_props[player][stat]['line']
                    draftkings_over = draftkings_props[player][stat]['over']
                    draftkings_under= draftkings_props[player][stat]['under']
                    if abs((draftkings_line - prizepicks_line) >= 1):
                        num_lines_different += 1
                    elif abs(int(draftkings_over >= 135)) or abs(int(draftkings_under >= 135)):
                        num_lines_different += 1
                except:
                    draftkings_line, draftkings_over, draftkings_under = -1, -1, -1
                try:
                    fanduel_line = fanduel_props[player][stat]['line']
                    fanduel_over = fanduel_props[player][stat]['over']
                    fanduel_under = fanduel_props[player][stat]['under']
                    if abs((fanduel_line - prizepicks_line) >= 1):
                        num_lines_different += 1
                    elif abs(int(fanduel_over >= 135)) or abs(int(fanduel_under >= 135)):
                        num_lines_different += 1
                except:
                    fanduel_line, fanduel_over, fanduel_under = -1, -1, -1
                if num_lines_different >= 0:
                    prop_item = {
                        "player": player,
                        "stat": stat,
                        "prizepicks_line": str(prizepicks_line),
                        "underdog_line": str(underdog_line),
                        "draftkings_line": str(draftkings_line),
                        "draftkings_over": str(draftkings_over),
                        "draftkings_under": str(draftkings_under),
                        "fanduel_line": str(fanduel_line),
                        "fanduel_over": str(fanduel_over),
                        "fanduel_under": str(fanduel_under),
                    }
                    return_props.append(prop_item)
    return return_props

if __name__ == '__main__':
    # props = main()
    # props = json.dumps(props)
    # print(props)
    props = main()
    db.create_table()
    for prop in props:
        db.add_prop_to_table(prop)
    
    