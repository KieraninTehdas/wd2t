from pprint import pprint

from flask.helpers import url_for
from wd2t.forms import NewDecisionForm
from wd2t.repositories import TagRepository
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect

import wd2t.config

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret yo"

tag_repository = TagRepository(wd2t.config.get_database())


decision1 = {
    "title": "A very important decision",
    "id": "1",
    "description": "This was a very difficult decision to make",
    "tags": [{"key": "service_name", "value": "ABB"}],
}
decision2 = {
    "title": "Another important decision",
    "id": "2",
    "description": "This decision was easy",
}


@app.route("/decisions")
def render_decisions():
    decisions = [decision1, decision2]
    return render_template("index.html", decisions=decisions)


@app.route("/decisions/<decision_id>")
def render_decision(decision_id):
    decision = None
    if decision_id == decision1["id"]:
        decision = decision1
    elif decision_id == decision2["id"]:
        decision = decision2

    return render_template("decision.html", decision=decision)


@app.route("/decisions/new", methods=["GET", "POST"])
def render_new_decision_form():
    form = NewDecisionForm()
    if form.validate_on_submit():
        pprint(form)
        return redirect(url_for("render_decisions"))
    else:
        pprint(form.errors)
    return render_template("new_decision_form.html", form=form)