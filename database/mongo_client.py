import os
import pymongo
from utils import logger

class MongoDBConnector:

    def __init__(self):
        # Connection settings
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.database_name = str(os.getenv("database_name"))
        self.collection_name = "engagements" #os.getenv("collection_name")

        # MongoDB URI
        self.mongo_uri = f"mongodb://localhost:27017/"

        self.client = pymongo.MongoClient(self.mongo_uri)

        self.database = self.client["chat_connector"]

        # Create the "engagements" collection if it doesn't exist
        self.create_collection()

    def create_collection(self):
        if self.collection_name not in self.database.list_collection_names():
            self.database.create_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' created.")


    def insert_or_update_message(self, message):
        # Check if a document with the same session_id exists
        existing_document = self.database[self.collection_name].find_one({'session_id': message['session_id']})

        if existing_document:
            # Update operation
            filter_query = {'session_id': message['session_id']}
            update_query = {'$set': {'content': message['content'],
                                     'message_id': message['message_id'],
                                     'correlation_id': message['correlation_id'],
                                     'timestamp': message["timestamp"]}}
            try:
                self.database[self.collection_name].update_one(filter_query, update_query)
                logger.info("Update operation successful.")
            except Exception as e:
                logger.error(f"Update operation failed: {e}")
        else:
            # Insert operation
            try:
                self.database[self.collection_name].insert_one(message)
                logger.info("Insert operation successful.")
            except Exception as e:
                logger.error(f"Insert operation failed: {e}")


    def find_content_by_session_id(self, session_id):
        try:
            document = self.database[self.collection_name].find_one({'session_id': session_id})
            if document:
                content = document.get('content')
                return content
            else:
                logger.info(f"No document found with session_id: {session_id}")
                return None
        except Exception as e:
            logger.error(f"Error while querying for session_id {session_id}: {e}")
            return None


    def insert_or_update_sid_dict(self,session_id):
        pass

    def __del__(self):
        # Close the connection when the instance is destroyed
        self.client.close()


# Create an instance of MongoDBConnector
mongo_connector = MongoDBConnector()


