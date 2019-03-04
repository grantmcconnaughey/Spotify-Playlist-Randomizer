# Spotify Playlist Randomizer

Takes 100 random tracks from a source playlist, shuffles them, and adds them to a new destination playlist.

Fixes two annoying things about the Spotify/Alexa integration:

1. [Spotify will only shuffle the first 100 songs of a playlist.](https://community.spotify.com/t5/Ongoing-Issues/Connect-only-plays-100-song-chunks-of-playlists/idi-p/1284690)
2. [Alexa does not know how to shuffle songs when played from a routine.](https://community.spotify.com/t5/Live-Ideas/echo-Playlists-Alexa-shuffle-command-for-routines/idi-p/4604442)

## Usage

First, create a [Spotify application](https://developer.spotify.com/dashboard/applications).

Next, export the following environment variables:

```bash
export SPOTIPY_CLIENT_ID='<Your Spotify application client ID>'
export SPOTIPY_CLIENT_SECRET='<Your Spotify application client secret>'
export SPOTIPY_REDIRECT_URI='http://localhost/callback/'
```

Finally, run `python main.py`. Every morning at 7:00 am you'll have a fresh playlist called "Working Today." This playlist will contain 100 songs, all of which are pre-shuffled.