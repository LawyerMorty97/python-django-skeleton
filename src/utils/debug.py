import json
from django.db import connection


class QueryCounter:
    def __init__(self, name=None, print=False, write_file=None):
        # Keep track of the number of queries executed
        # before initializing `self`.
        self._num_queries_before_self = len(connection.queries or [])
        self.name = name or "QueryCounter"
        self.print = print
        self.write_file = write_file

    def __enter__(self):
        return self

    def __exit__(self, *exec):
        self.query_count = (
            len(connection.queries) - self._num_queries_before_self
        )  # noqa
        self.queries = connection.queries[self._num_queries_before_self :]
        self.elapsed = sum([float(c["time"]) for c in self.queries])
        if self.write_file:
            with open(f"{self.name}.txt", "w") as f:
                json.dump(self.queries, f, indent=2)
        if self.print:
            print(f"{self.name}> {self.query_count} queries, {self.elapsed}s")

        return None
