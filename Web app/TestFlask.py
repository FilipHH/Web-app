#Den importerer funksjonen som skal brukes fra flask
from flask import Flask, render_template, request, redirect, jsonify
import pymongo, json
import uuid
import datetime

#Kobler sammen database og server
client = pymongo.MongoClient("mongodb+srv://Admin:7W93HOyo58vdV0dW@notebook-egkxy.gcp.mongodb.net/test?retryWrites=true")
db = client.Notebook

# /notes/CreateNote
# /notes/UpdateNote
# /notes/GetNote

#Det starter opp serveren
app = Flask(__name__)
# Finner alle notatene i databasen
def get_notes():
	notes = []
	for note in db.note.find({}):
		print(note["title"])
		notes.append(note)
	return notes

#@app.route("/hjem")
#def hjem():
#    return redirect("localhost:5000/home", code=302)


@app.route("/home", methods=["GET"])
def home():
	return render_template("Test.html")

@app.route("/notater", methods=["GET"])
def notater():
	return render_template("notater.html", notes=get_notes())

#Lager ny fil og gir den id
@app.route("/api/notes/CreateNote", methods=["POST"])
def new_note():
	noteid = str(uuid.uuid4())
	db.note.insert_one({
		"noteid": noteid,
		"date": datetime.datetime.now(),
		"title": "Unnamed",
		"content": ""
	})
	return jsonify({"id": noteid})

#Oppdaterer databasen med et nytt notat med nytt innhold
@app.route("/api/notes/UpdateNote/<id>", methods=["PATCH"])
def create(id):
	data = request.form
	#noteid = request.args["id"]
	noteid = id;
	print(data);
	title = data["title"]
	content = data["content"]
	print(title, content, noteid)
	db.note.update_one({"noteid": noteid},{
		"$set": {
			"title": title,
			"content": content,
		}
	})
	return json.dumps({"status": 200})
#Henter fil fra databsen med id som blir spurt om.
@app.route("/api/notes/GetNote/<id>")
def getNote(id):
	#Henter notat med spesifisert id i database og puter noteid, title og content inn i en dictionary
	note = db.note.find_one({"noteid": id}, {"noteid": 1, "_id": 0, "title": 1, "content": 1})
	#returnerer notatet til klienten
	return json.dumps({"status": 200, "data": note})

#passord admin bruker: 7W93HOyo58vdV0dW

