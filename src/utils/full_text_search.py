from itertools import chain

from psycopg2.extensions import adapt
from django.contrib.postgres.search import SearchQuery


class PrefixedSearchQuery(SearchQuery):
    def as_sql(self, compiler, connection):
        terms = chain.from_iterable(
            expr.value.split() for expr in self.source_expressions
        )

        value = adapt("%s:*" % " & ".join(terms)).getquoted().decode("iso-8859-1")

        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = "to_tsquery({}::regconfig, {})\
				.format(config_sql, value)"
            params = config_params
        else:
            template = "to_tsquery({})".format(value)
            params = []

        if self.invert:
            template = "!!({})".format(template)

        return template, params
