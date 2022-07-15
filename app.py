from flask import Flask , jsonify, request, render_template, redirect, url_for
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/')))
from src.load_validate_preprocess import preprocess_validated_data
from src.prediction_service import get_recommendation
from src.web_scraper.scraper import scraper
from src.functions import get_stats, dump_json, load_json


config_path = "params.yaml"

webapp_root = "webapp"
template_dir = os.path.join(webapp_root, "templates")
static_dir = os.path.join(webapp_root, "static")


app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        args_dict = {}
        input_imt_dict = request.form

        args_dict["category"] = input_imt_dict.getlist("category")
        if "wfh" in input_imt_dict.keys():
            args_dict["wfh"] = "yes"
        else:
            args_dict["wfh"] = "no"
        args_dict["location"] = input_imt_dict.getlist("location")
        if args_dict["location"] == [""]:
            args_dict["location"] = []
        print(args_dict)
        scraper(args_dict)
        preprocess_validated_data(config_path)
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():

    if request.method == "POST":
        input_dict = {}
        input_dict["skills"] = request.form.get("skills").split(", ")
        input_dict["duration"] = request.form.get("duration")
        dump_json("user_input_dict.json", input_dict)
        print(request.form)
        print(input_dict)
        return redirect(url_for("recommend"))

    prp_data_path = "data/processed/prp_data.csv"
    stats_dict = get_stats(prp_data_path)
    return render_template(
        "dashboard.html",
        avg_dur = stats_dict["avg_dur"],
        min_dur = stats_dict["min_dur"],
        max_dur = stats_dict["max_dur"],
        st_avg = stats_dict["st_avg"],
        st_max = stats_dict["st_max"],
        least_count = stats_dict["least_count"],
        eas = stats_dict["eas"],
        tplus = stats_dict["tplus"],
        appl_avg = stats_dict["appl_avg"],
        avg_opn = stats_dict["avg_opn"],
        max_opn = stats_dict["max_opn"],
        all_skills = stats_dict["all_skills"]
    )

@app.route("/recommend")
def recommend():
    prp_data_path = "data/processed/prp_data.csv"
    user_input_dict = load_json("user_input_dict.json")
    rdf_table = get_recommendation(user_input_dict, prp_data_path).to_json(orient="records")
    data=[]
    data= json.loads(rdf_table)
    return render_template("recommend.html", d=data)





if __name__ == "__main__":
    app.run()