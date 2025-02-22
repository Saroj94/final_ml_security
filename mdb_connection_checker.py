from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure
import certifi
import ssl 

url="mongodb+srv://sarojrailive:25Raimongo@cluster0.fb7cg.mongodb.net/admin?retryWrites=true&w=majority"

# Create a new client and connect to the server with SSL certificate verification disabled
client = MongoClient(url, tls=True, tlsAllowInvalidCertificates=True)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")