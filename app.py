from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(".env")


def create_app():
    app = Flask(__name__)

    client = MongoClient(
        os.getenv("MONGO_URL")
    )

    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entery_content = request.form.get("content")
            formated_datetime = datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one(
                {"content": entery_content, "date": formated_datetime}
            )

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)

    return app
