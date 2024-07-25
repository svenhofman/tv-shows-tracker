import argparse

from .commands import search_show, show_new_releases, list_shows


def create_arg_parser():
    parser = argparse.ArgumentParser(description="TV show releases tracker")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for a show")
    search_parser.add_argument("query", type=str, help="Query string to search for")
    search_parser.set_defaults(func=search_show)

    # Show command
    show_parser = subparsers.add_parser("new", help="Show new releases of watchlist shows")
    show_parser.set_defaults(func=show_new_releases)

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List all shows on watchlist",
    )
    list_parser.set_defaults(func=list_shows)

    return [parser.parse_args(), parser.print_help]
