from datetime import datetime

from .config import get_auth_key
from .menu import display_menu, preview_command
from .database import (
    get_all_shows,
    get_running_shows,
    add_shows,
    delete_show,
    update_ended_shows,
    update_last_watched,
)
from .fetching import fetch_search_results, fetch_show

ENDED = "Ended"


def search_show(args):
    try:
        shows = fetch_search_results(args.query, get_auth_key())
    except Exception as err:
        print("Error:", err)
        return

    if len(shows) == 0:
        print("No shows found.")
        return

    # Extract show names and define preview data
    shows_menu_info = [
        *[f"{show['original_name']}|{show['id']}" for show in shows],
        "[e] exit|exit search",
    ]

    # To simulate pass by reference, will be set in preview_command
    selected_show_ref = [None]

    selected_index = display_menu(
        shows_menu_info,
        title="Press return/enter to add show, E to exit",
        preview_function=lambda show_string: preview_command(selected_show_ref, show_string),
    )

    # Exit is last option, None is returned when Escape is pressed
    if selected_index in (len(shows_menu_info) - 1, None):
        return

    # Add selected show
    show = selected_show_ref[0]
    response = add_shows(
        [
            {
                "name": show["original_name"],
                "id": show["id"],
                "last_watched": datetime.today(),
                "has_ended": show["status"] == ENDED,
            }
        ]
    )
    print(response)


def show_new_releases(args):
    releases = []
    has_ended = []

    shows = get_running_shows()
    for show in shows:
        try:
            fetched_show = fetch_show(show["id"], get_auth_key())
        except Exception as err:
            print("Error:", err)
            continue

        if fetched_show["status"] != ENDED:
            last_air_date = datetime.strptime(fetched_show["last_air_date"], "%Y-%m-%d")
            if last_air_date > show["last_watched"]:
                releases.append(fetched_show)
        else:
            has_ended.append(show["id"])

    if len(releases) == 0:
        print("No new releases.")
        return

    # Extract show names
    shows_menu_info = [
        *[f"{show['original_name']}|" for show in releases],
        "[e] exit|exit search",
    ]
    selected_index = display_menu(
        shows_menu_info, title="Press return/enter to update watch date, E to exit"
    )

    # Exit is last option, None is returned when Escape is pressed
    if selected_index in (len(shows_menu_info) - 1, None):
        return

    # Update last watched date to now
    show_id = releases[selected_index]["id"]
    update_last_watched(show_id, datetime.today())

    # Update shows that have ended
    update_ended_shows(has_ended)


def list_shows(args):
    shows = get_all_shows()

    # Extract show names
    shows_menu_info = [*[f"{show['name']}|" for show in shows], "[e] exit|exit search"]
    selected_index = display_menu(
        shows_menu_info, title="Press return/enter to remove show or E to exit"
    )

    # Exit is last option, None is returned when Escape is pressed
    if selected_index in (len(shows_menu_info) - 1, None):
        return

    # Remove show
    show_id = shows[selected_index]["id"]
    response = delete_show(show_id)
    print(response)
