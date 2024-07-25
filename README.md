# TV Shows Tracker

TV Shows Tracker is a Python-based command-line tool to track the TV shows you are watching and get informed about new releases. The tool uses [TMDB](https://www.themoviedb.org) to get information on new releases. Information about registering for an API key can be found [here](https://developer.themoviedb.org/docs/getting-started). Additionally, the tool uses MongoDB to store the TV shows, so a MongoDB server should be running either locally or remotely.

## Features

- Add/remove TV shows to your watchlist
- List all TV shows in your watchlist
- List all TV shows with new releases in your watchlist

## Installation

You can install the package using `pipx`:

### Clone the Repository

```sh
git clone https://github.com/svenhofman/tv-shows-tracker.git
cd tv-shows-tracker
pipx install .
```

### Database configuration
By default, the application tries to connect to a MongoDB server running on `localhost` on port `27017`. This can be changed in `src/database.py`.

## Usage

After installation, you can use the `tv-shows-tracker` command in your terminal. On the first run, it will ask for the API key.

### Search for a TV show

```sh
tv-shows-tracker search 'Breaking'
```

### List all TV shows on watchlist
```sh
tv-shows-tracker list
```
TV shows can be removed using the interactive menu that appears

### List all TV shows with new releases
```sh
tv-shows-tracker new
```
The last watched date can be updated using the interactive menu that appears

## Status
This project is a work in progress.
