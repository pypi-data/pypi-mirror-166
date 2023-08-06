from pymongo.database import Database

from .collections.cboe import CBOEQueries

class QueryManager:
    def __init__(self, db: Database):
        self.db = db
        self.cboe_queries = CBOEQueries(db=db)