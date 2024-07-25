import re
from simple_term_menu import TerminalMenu
from .config import get_auth_key
from .fetching import fetch_show

def is_not_numeric(string):
    return not bool(re.search(r'\d', string))

def get_last_episode(show):
    last_episode_season = show['last_episode_to_air']['season_number']
    if last_episode_season < 10: 
        last_episode_season = '0' + str(last_episode_season)
    last_episode_number = show['last_episode_to_air']['episode_number']
    if last_episode_number < 10: 
        last_episode_number = '0' + str(last_episode_number)
    return f'S{last_episode_season}E{last_episode_number}'

def preview_command(show_string):
    # Extract preview string
    preview_info = show_string.split("|", 1)[-1]
    if is_not_numeric(preview_info):
        return preview_info

    show = fetch_show(preview_info, get_auth_key())
    last_episode = get_last_episode(show)

    return (f"{"name:":{' '}<{16}}{show["original_name"]}\n"
            f"{"overview:":{' '}<{16}}{show["overview"]}\n"
            f"{"origin country:":{' '}<{16}}{show["origin_country"]}\n"
            f"{"last episode:":{' '}<{16}}{last_episode}\n"
            f"{"id:":{' '}<{16}}{show["id"]}"
            )
    

def display_menu(shows, title='', preview_function=None):
    # Create a TerminalMenu object
    terminal_menu = TerminalMenu(shows, title=title + '\n', preview_command=preview_function, preview_size=0.75)
    # Display the menu and get the selected option index
    selected_option_index = terminal_menu.show()
        
    return selected_option_index
