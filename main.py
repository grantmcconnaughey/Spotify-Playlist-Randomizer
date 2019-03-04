import logging
import os
import random
import time

import schedule
import spotipy
import spotipy.util as util


logger = logging.getLogger('spotify_playlist_randomizer')
current_directory = os.path.dirname(os.path.abspath(__file__))


class SpotifyPlaylistRandomizer(object):

    def __init__(self, username):
        self.username = username
        self.client = spotipy.Spotify(auth=self._get_token())

    def randomize_playlist(self, source_playlist_id, destination_playlist_id=None):
        if destination_playlist_id is None:
            logger.info('Creating a new destination playlist')
            new_playlist = self.client.user_playlist_create(
                self.username,
                name='Working Today',
                public=False
            )
            destination_playlist_id = new_playlist['id']

        logger.info('Clearing tracks from the destination playlist')
        self._clear_tracks_from_playlist(destination_playlist_id)

        # Get 100 source playlist tracks, randomize them, and shuffle them
        logger.info('Getting a fresh set of 100 tracks from the source playlist')
        track_ids = self._get_playlist_track_ids(source_playlist_id)
        random_track_ids = self._randomize_tracks(track_ids)

        # Add the new random tracks to the playlist
        logger.info('Adding tracks to the destination playlist')
        self.client.user_playlist_add_tracks(
            self.username,
            destination_playlist_id,
            random_track_ids
        )

    def _get_token(self):
        scope = 'playlist-modify-private'
        cached_creds_file = os.path.join(current_directory, '.creds.json')
        return util.prompt_for_user_token(
            self.username,
            scope,
            cache_path=cached_creds_file
        )

    def _get_playlist_track_ids(self, playlist_id):
        track_ids = []
        number_of_tracks_in_playlist = self.client.user_playlist_tracks(
            self.username,
            playlist_id=playlist_id,
            fields='total')['total']

        logger.info('{} tracks in the source playlist'.format(
            number_of_tracks_in_playlist))

        offset = 0
        while number_of_tracks_in_playlist > len(track_ids):
            limit = 100
            result = self.client.user_playlist_tracks(
                self.username,
                playlist_id=playlist_id,
                fields='items(track(id))',
                limit=limit,
                offset=offset
            )
            track_ids.extend(t['track']['id'] for t in result['items'])
            offset += limit

        # Make sure there are no duplicates
        track_ids = list(set(track_ids))

        # Sanity check
        assert len(track_ids) == number_of_tracks_in_playlist

        return track_ids

    def _randomize_tracks(self, track_ids, number_of_tracks=100):
        random_track_ids = random.sample(track_ids, number_of_tracks)
        random.shuffle(random_track_ids)
        return random_track_ids

    def _clear_tracks_from_playlist(self, playlist_id):
        track_ids = self._get_playlist_track_ids(playlist_id)
        self.client.user_playlist_remove_all_occurrences_of_tracks(
            self.username,
            playlist_id,
            tracks=track_ids
        )


def main():
    logging.basicConfig(
        filename='debug.log',
        level=logging.INFO
    )

    def job():
        randomizer = SpotifyPlaylistRandomizer(username='1239650')
        randomizer.randomize_playlist(
            source_playlist_id='1mFpgFtuH3LpoR6kHphjQv',
            destination_playlist_id='3mpw6jMmqCBKtfZvAQFFtD'
        )

    schedule.every().day.at('07:00').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
