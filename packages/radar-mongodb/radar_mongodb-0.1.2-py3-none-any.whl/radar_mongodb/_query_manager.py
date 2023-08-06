from pymongo.database import Database

from .collections.cboe import CBOEQueries


class QueryManager:
    def __init__(self, db: Database, cboe_collection_name: str):
        self.db = db
        self.cboe_queries = CBOEQueries(db=db, collection_name=cboe_collection_name)
