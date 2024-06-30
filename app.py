from flask import Flask, render_template, jsonify, request, session
import database
import secrets
from datetime import timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/loginPage")
def login_page():
    return render_template("loginPage.html")


@app.route("/user", methods=['post'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    session.permanent = True
    session['user_name'] = username
    return {'status': 'success', 'user': username}
    # user = database.get_user_by_username(username)
    # if user and user["password"] == password:
    #     session["user_id"] = user["id"]
    #     return jsonify({"success": True})
    # else:
    #     return jsonify({"success": False, "message": "Invalid username or password"})


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


@app.route("/jobs/<job_id>")
def get_job_details(job_id):
    job_details = database.get_job_details(job_id)
    if len(job_details) != 0:
        return render_template('pages/job_details.html',
                               job_details=job_details)
    else:
        return "Job Not Found", 404


@app.route("/jobs/<job_id>/apply", methods=['post'])
def apply_to_job(job_id):
    data = request.form
    return data


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
