from sqlite3 import Row


class DictRow(Row):
    def __getattr__(self, name):
        return self[name]
