from bson.objectid import ObjectId
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

mongo_username = "wd2t_app"
mongo_password = "something very secure"

mongo_client = MongoClient(
    "localhost",
    username=mongo_username,
    password=mongo_password,
    authSource="wd2t",
)

db = mongo_client.wd2t


@app.route("/")
@app.route("/<name>")
def hello_world(name=None):
    if name:
        new_doc_id = db.tags.insert_one(
            {"name": "service", "value": "HALS"}
        ).inserted_id
    return render_template("index.html", name=name, inserted_id=new_doc_id)


@app.route("/document/<_id>")
def get_document_by_id(_id):
    doc = db.tags.find_one({"_id": ObjectId(_id)})
    print(doc)
    return render_template("index.html", doc=doc)
