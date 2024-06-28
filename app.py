from flask import Flask, render_template, jsonify
import database 

app = Flask(__name__)


@app.route("/")
def hello_world():
    jobs = database.load_jobs_from_db()
    return render_template('home.html', jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
    jobs = database.load_jobs_from_db()
    return jsonify(jobs)


@app.route("/overview")
def get_overview():
    return render_template('overview.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
