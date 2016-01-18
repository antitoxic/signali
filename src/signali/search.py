from watson.backends import PostgresSearchBackend, escape_query

class SignaliPostgresBackend(PostgresSearchBackend):
    def escape_postgres_query(self, text):
        """Escapes the given text to become a valid ts_query."""
        return " | ".join(
            "$${0}$$:*".format(word) for word in escape_query(text).split()
        )
