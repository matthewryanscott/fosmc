import os

import yaml


def load_data(path):
    db = dict(
        city={},
        dj={},
        event={},
        genre={},
        recording={},
    )
    # Load data in the order of most authoritative to least authoritative
    # (regarding spelling of names and mapping of names to slugs).
    load_cities(path, db)
    load_genres(path, db)
    load_djs(path, db)
    load_events(path, db)
    load_recordings(path, db)
    return db


def load_cities(path, db):
    filename = os.path.join(path, 'cities.yaml')


def load_genres(path, db):
    filename = os.path.join(path, 'genres.yaml')


def load_djs(path, db):
    filename = os.path.join(path, 'djs.yaml')


def load_events(path, db):
    filename = os.path.join(path, 'events.yaml')


def load_recordings(path, db):
    filename = os.path.join(path, 'recordings.yaml')
