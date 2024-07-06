from flask import Flask, render_template, jsonify, request, session,redirect, url_for
import database
import secrets
from datetime import timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/loginPage")
def login_page():
    return render_template("loginPage.html")

@app.route("/signUpPage")
def sign_up_page():
    return render_template("signUpPage.html")


@app.route("/logout")
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home_page'))
    
@app.route("/validateUser", methods=['post'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    session.permanent = True
    session['user_name'] = username
    return redirect(url_for('home_page'))
    # user = database.get_user_by_username(username)
    # if user and user["password"] == password:
    #     session["user_id"] = user["id"]
    #     return jsonify({"success": True})
    # else:
    #     return jsonify({"success": False, "message": "Invalid username or password"})


@app.route("/")
def home_page():
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

@app.route("/api/users/<user_name>")
def list_users(user_name):
    user_details = database.get_user_details(user_name)
    return jsonify(user_details)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
