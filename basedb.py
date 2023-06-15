from json import load, dump

class BaseDB:
    def __init__(self, dbfile):
        self.data = None
        self.dbfile = dbfile
        self.load()

    def load(self):
        with open(self.dbfile, "r+") as db:
            self.data = load(db)

    def _serialize(self):
        with open(self.dbfile, "w") as db:
            dump(self.data, db)

