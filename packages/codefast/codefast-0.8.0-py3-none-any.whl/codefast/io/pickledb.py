#!/usr/bin/env python
import os
import pickle


try:
    import expiringdict
except ImportError:
    print('install expiringdict ...')
    os.system('pip install expiringdict')


class PickleDB(object):
    """ simple key-value database 
    """

    def __init__(self,
                 db_file: str = '/tmp/pickle.db',
                 max_len: int = 1000,
                 max_age_seconds: int = 86400 * 30) -> None:
        self.db_file = db_file
        self.db = expiringdict.ExpiringDict(max_len=max_len,
                                            max_age_seconds=max_age_seconds)
        if os.path.exists(db_file):
            _db = pickle.load(open(db_file, 'rb'))
            for k, v in _db.items():
                self.db[k] = v

    def set(self, foo: str, bar: str) -> bool:
        self.db[foo] = bar
        pickle.dump(self.db, open(self.db_file, 'wb'))

    def get(self, foo: str) -> str:
        return self.db.get(foo, None)
