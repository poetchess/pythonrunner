import warnings
import inspect

import osconfeed

DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'

class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

# Custom exceptions are usually marker classes, with no body.
# A docstring explaining the usage of the exception is better than
#   a mere pass statement
class MissingDatabaseError(RuntimeError):
   """Raised when a database is required but was not set."""

class DbRecord(Record):
    # The __db class attribute will hold a reference to the opened
    # shelve.Shelf database.
    __db = None

    # set_db is a staticmethod to make it explicit that its effect is always
    # exactly the same, no matter how it's called.
    # Even if this method can be invoked as Event.set_db(my_db), the __db
    # attribute will be set in the DbRecord class.
    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    # get_db is also a staticmethod because it will always return the object
    # referenced by DbRecord.__db, no matter how it's invoked.
    @staticmethod
    def get_db():
        return DbRecord.__db

    # fetch is a class method so that its behavior is easier to customize in
    # subclasses.
    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            # re-raise the exception since we don't know how to handle it.
            else:
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()


class Event(DbRecord):

    # venue is a property, it builds a key from the venue_serial attribute, and
    # passes it to the fetch class method, inherited from DbRecord. We should not
    # use self.fetch(key) because if even a single event record had a key named
    # 'fetch', then within that specific Event instance, the referenced self.fetch
    # would retrieve the value of that field, instead of the 'fetch' class method,
    # which is a subtle bug.
    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            # 'speakers' attribute is retrieved directly from the instance
            #  __dict__ to aviod an infinite recursion, because the public
            # name of this property is also 'speakers'.
            spkr_serials = self.__dict__['speakers']

            # Do not use self.fetch, due to the reason above.
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]
            return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        # Get an object by name from the module global scope; get 'DbRecord' if
        # there's no such object.
        cls = globals().get(cls_name, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)


if __name__ == '__main__':
    import shelve
    db = shelve.open(DB_NAME)
    if CONFERENCE not in db:
        load_db(db)

    DbRecord.set_db(db)
    event = DbRecord.fetch('event.33950')
    print(event)
    print(event.venue)
    print(event.venue.name)
    for spkr in event.speakers:
        print('{0.serial}: {0.name}'.format(spkr))

    db.close()
