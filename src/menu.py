import re
from simple_term_menu import TerminalMenu
from .config import get_auth_key
from .fetching import fetch_show
from datetime import datetime

def is_not_numeric(string):
    return not bool(re.search(r'\d', string))

def get_episode(show, which):
    episode = f'{which}_episode_to_air'
    if show[episode] == None:
        return None
    
    episode_season = show[episode]['season_number']
    if episode_season < 10: 
        episode_season = '0' + str(episode_season)
    episode_number = show[episode]['episode_number']
    if episode_number < 10: 
        episode_number = '0' + str(episode_number)

    if which == 'next':
        air_date = datetime.strptime(show[episode]['air_date'], "%Y-%m-%d")
        return f'S{episode_season}E{episode_number} on {air_date.strftime("%d-%m-%Y")}'

    return f'S{episode_season}E{episode_number}'


def preview_command(selected_show, show_string):
    # Extract preview string
    preview_info = show_string.split("|", 1)[-1]
    if is_not_numeric(preview_info):
        return preview_info

    show = fetch_show(preview_info, get_auth_key())
    last_episode = get_episode(show, 'last')
    next_episode = get_episode(show, 'next')  

    # Set selected show so it can be used by callee
    selected_show[0] = show
    
    return (f"{"name:":{' '}<{16}}{show["original_name"]}\n"
            f"{"overview:":{' '}<{16}}{show["overview"]}\n"
            f"{"origin country:":{' '}<{16}}{show["origin_country"]}\n"
            f"{"last episode:":{' '}<{16}}{last_episode}\n"
            f"{"next episode:":{' '}<{16}}{next_episode if next_episode != None else "unknown"}\n"
            f"{"id:":{' '}<{16}}{show["id"]}"
            )
    

def display_menu(shows, title='', preview_function=None):
    # Create a TerminalMenu object
    terminal_menu = TerminalMenu(shows, title=title + '\n', preview_command=preview_function, preview_size=0.75)
    # Display the menu and get the selected option index
    selected_option_index = terminal_menu.show()
        
    return selected_option_index
