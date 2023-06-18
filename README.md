# Attendance-System-using-Face-Recognition-with-MongoDB
We are using face recognition for attendance system. We are using MongoDB server for the database purposes.
## Description


# Connecting to MongoDB Server
### Local connection
You can use localhost connection to connect to the mongodb with the MongoDBCompass App.
For windows, you can download and install this app.
Then, in the new connection, you will see a connection string in URI Format.
This string can be used to connect to the local host.

### Connecting to Server
You will have a mongodb atlas where you can create a database with the default options. 
Then you can click connect in it.
You will have a url something like this.

```
mongodb+srv://<username>:<password>@cluster0.n0kingo.mongodb.net/test
```
You can use this in your MongoClient (in python) to connect to the database in the server.
