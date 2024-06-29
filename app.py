from flask import Flask, render_template, jsonify, request
import database

app = Flask(__name__)


@app.route("/")
def hello_world():
    jobs = database.load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

@app.route("/jobs")
def display_jobs():
    jobs = database.load_jobs_from_db()
    return render_template('pages/jobs_page.html', jobs=jobs)


@app.route("/overview")
def get_overview():
    return render_template('pages/overview.html')

@app.route("/faqs")
def get_faqs():
    faqs = database.get_faqs_from_db()
    return render_template('pages/faqs.html', faqs=faqs)
    
##############################################################################
# Api's 
##############################################################################
@app.route("/api/job")
def load_job():
    job_id = request.args['job_id']
    job_details = database.get_job_details(job_id)
    return jsonify(job_details)


@app.route("/api/jobs")
def list_jobs():
    jobs = database.load_jobs_from_db()
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
