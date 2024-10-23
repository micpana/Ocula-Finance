from mongoengine import connect, get_connection
import mongoengine

def init_db():
    # get the MongoDB client from the MongoEngine connection
    try:
        # client
        client = get_connection()
        
        # check if the connection is already established
        if client is None:
            print("No client connection available. Attempting to connect...")
            connect(host="your_mongodb_atlas_connection_string")
            print("New database connection established.")
        else:
            print("Client connection retrieved.")

            # if client is not None, check if it's primary
            if client.is_primary:
                print("Already connected to the primary database.")
            else:
                print("Connected to a secondary node.")

    except mongoengine.connection.ConnectionFailure as e:
        print(f'Connection failed: {e}')
        print('Establishing new database connection.')
        connect(host="your_mongodb_atlas_connection_string")
        print("New database connection established.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Initialize the database connection
init_db()
