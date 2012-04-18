import os

from slugify import slugify
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
    with open(os.path.join(path, 'cities.yaml')) as f:
        for city in yaml.load_all(f):
            _populate_slug_and_name(city)
            _store_replacement(db['city'], city)
            db['city'][city['slug']] = city

def load_genres(path, db):
    aliases = set()
    with open(os.path.join(path, 'genres.yaml')) as f:
        for genre in yaml.load_all(f):
            _populate_slug_and_name(genre)
            _store_replacement(db['genre'], genre)
            db['genre'][genre['slug']] = genre
            aliases.update(slugify(alias.decode('utf8')) for alias in genre.get('aliases', []))
    for genre in db['genre'].values():
        if genre['slug'] in aliases:
            # Name of one genre is alias of another; tag for lint.
            genre['lint_is_also_alias'] = True


def load_djs(path, db):
    with open(os.path.join(path, 'djs.yaml')) as f:
        for dj in yaml.load_all(f):
            _populate_slug_and_name(dj)
            _store_replacement(db['dj'], dj)
            db['dj'][dj['slug']] = dj
            if 'city' in dj:
                city = dj['city']
                cityslug = slugify(city.decode('utf8'))
                if cityslug not in db['city']:
                    db['city'][cityslug] = dict(
                        name=city,
                        slug=cityslug,
                        lint_created_by_dj=dj['slug'],
                    )
                dj['city'] = cityslug
                city_djs = db['city'][cityslug].setdefault('djs', [])
                city_djs.append(dj['slug'])
            # Normalize 'genre' to 'genres'.
            genres = dj.setdefault('genres', [])
            if 'genre' in dj:
                genres.append(dj.pop('genre'))
            genreslugs = []
            for genre in genres:
                genreslug = slugify(genre.decode('utf8'))
                if genreslug not in db['genre']:
                    db['genre'][genreslug] = dict(
                        name=genre,
                        slug=genreslug,
                        lint_created_by_dj=dj['slug'],
                    )
                genreslugs.append(genreslug)
                genredjs = db['genre'][genreslug].setdefault('djs', [])
                genredjs.append(dj['slug'])
            dj['genres'] = genreslugs


def load_events(path, db):
    with open(os.path.join(path, 'events.yaml')) as f:
        for event in yaml.load_all(f):
            _populate_slug_and_name(event)
            _store_replacement(db['event'], event)
            db['event'][event['slug']] = event
            if 'city' in event:
                city = event['city']
                cityslug = slugify(city.decode('utf8'))
                if cityslug not in db['city']:
                    db['city'][cityslug] = dict(
                        name=city,
                        slug=cityslug,
                        lint_created_by_event=event['slug'],
                    )
                event['city'] = cityslug
                city_events = db['city'][cityslug].setdefault('events', [])
                city_events.append(event['slug'])


def load_recordings(path, db):
    with open(os.path.join(path, 'recordings.yaml')) as f:
        for recording in yaml.load_all(f):
            recording.setdefault('name', 'Recording')
            recording.setdefault('date', None)
            # Convert single DJ to list of one DJ.
            djs = recording.setdefault('djs', [])
            if 'dj' in recording:
                djs.append(recording.pop('dj'))
            # Generate slug if not present.
            if 'slug' not in recording:
                slugs = []
                if 'event' in recording:
                    slugs.append(slugify(recording['event'].decode('utf8')))
                if len(djs) == 1:
                    slugs.append(slugify(recording['djs'][0].decode('utf8')))
                elif len(djs) > 1:
                    slugs.append('multiple')
                slugs.append(slugify(recording['name'].decode('utf8')))
                if recording['date']:
                    slugs.append(recording['date'].strftime('%Y-%m-%d'))
                recording['slug'] = '_'.join(slugs)
            _store_replacement(db['recording'], recording)
            db['recording'][recording['slug']] = recording
            # Auto-create other objects based on information present.
            # Normalize references to other objects to slugs.
            for dj in djs:
                djslug = slugify(dj.decode('utf8'))
                if djslug not in db['dj']:
                    db['dj'][djslug] = dict(
                        name=dj,
                        slug=djslug,
                        lint_created_by_recording=recording['slug'],
                    )
                dj_recordings = db['dj'][djslug].setdefault('recordings', [])
                dj_recordings.append(recording['slug'])
            recording['djs'] = [slugify(dj.decode('utf8')) for dj in recording['djs']]
            if 'city' in recording:
                city = recording['city']
                cityslug = slugify(city.decode('utf8'))
                if cityslug not in db['city']:
                    db['city'][cityslug] = dict(
                        name=city,
                        slug=cityslug,
                        lint_created_by_recording=recording['slug'],
                    )
                recording['city'] = cityslug
                city_recordings = db['city'][cityslug].setdefault('recordings', [])
                city_recordings.append(recording['slug'])
            if 'event' in recording:
                event = recording['event']
                eventslug = slugify(event.decode('utf8'))
                if eventslug not in db['event']:
                    db['event'][eventslug] = dict(
                        name=event,
                        slug=eventslug,
                        lint_created_by_recording=recording['slug'],
                    )
                recording['event'] = eventslug
                event_recordings = db['event'][eventslug].setdefault('recordings', [])
                event_recordings.append(recording['slug'])
            if 'genre' in recording:
                genre = recording['genre']
                genreslug = slugify(genre.decode('utf8'))
                if genreslug not in db['genre']:
                    db['genre'][genreslug] = dict(
                        name=genre,
                        slug=genreslug,
                        lint_created_by_recording=recording['slug'],
                    )
                recording['genre'] = genreslug
                genre_recordings = db['genre'][genreslug].setdefault('recordings', [])
                genre_recordings.append(recording['slug'])


def _populate_slug_and_name(obj):
    if 'slug' not in obj:
        # Generate slug from name if slug not present.
        obj['slug'] = slugify(obj['name'].decode('utf8'))
    elif 'name' not in obj:
        # Name not given, only slug; copy slug into name and tag for lint.
        obj['name'] = obj['slug']
        obj['lint_name_from_slug'] = True


def _store_replacement(obj_dict, obj):
    if obj['slug'] in obj_dict:
        obj['lint_replaces'] = obj_dict[obj['slug']]  # Tag for lint.
