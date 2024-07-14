from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import database
import secrets
from datetime import timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/loginPage")
def login_page():
    email = request.args.get('email')
    if email is None:
        email = ""
    return render_template("loginPage.html", email=email)


@app.route("/signUpPage")
def sign_up_page():
    return render_template("signUpPage.html")


@app.route("/signUpWithAdmin")
def sign_up_with_admin():
    return render_template("pages/adminSignUp.html")


@app.route("/signInWithAdmin")
def sign_in_with_admin():
    return render_template("pages/adminSignIn.html")


@app.route("/createUser", methods=["POST"])
def create_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    new_user_status = database.addUser(fname, lname, phone, email, password)
    user = database.get_user_details(email)
    if new_user_status["status"] == "Success":
        session["email"] = email
        session["user_fname"] = fname
        session["user_lname"] = lname
        session["user_phone"] = phone
        session["user_id"] = user[0]["user_id"]
        return redirect(url_for("home_page"))
    else:
        flash(new_user_status["message"], "danger")
        return redirect(url_for("sign_up_page"))


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    session.pop('user_fname', None)
    session.pop('user_lname', None)
    session.pop('user_phone', None)
    return redirect(url_for('home_page'))


@app.route("/myProfile")
def my_profile():
    return render_template("pages/myProfile.html")


@app.route("/validateUser", methods=['post'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = database.get_user_details(email)
    if password == user[0]["user_password"]:
        session.permanent = True
        session["email"] = email
        session["user_fname"] = user[0]["fname"]
        session["user_lname"] = user[0]["lname"]
        session["user_phone"] = user[0]["user_phone"]
        session["user_id"] = user[0]["user_id"]
        return redirect(url_for("home_page"))
    else:
        flash("Invalid password", "danger")
        return redirect(url_for("login_page", email=email))


@app.route("/")
def home_page():
    jobs = database.load_jobs_from_db()
    return render_template('home.html', jobs=jobs)


@app.route("/jobs")
def display_jobs():
    jobs = database.load_jobs_from_db()
    return render_template('pages/jobs_page.html', jobs=jobs)


@app.route("/myDeals")
def display_my_deals():
    return render_template('pages/myDealsPage.html')


@app.route("/overview")
def get_overview():
    return render_template('pages/overview.html')


@app.route("/jobs/<job_id>")
def get_job_details(job_id):
    job_details = database.get_job_details(job_id)
    if len(job_details) != 0:
        job_status = ""
        if "user_id" in list(session.keys()):
            user_id = session["user_id"]
            job_status = database.get_job_status_for_user(user_id, job_id)
            print(job_status)
            if len(job_status) != 0:
                job_status = job_status[0]["application_status"]
            else:
                job_status = ""
        return render_template('pages/job_details.html',
                               job_details=job_details,
                               job_status=job_status)
    else:
        return "Job Not Found", 404


@app.route("/jobs/<job_id>/apply", methods=["POST"])
def apply_to_job(job_id):
    data = request.form
    e_email = data['email']
    e_name = data['name']
    e_experience = data['experience']
    e_notice_period = data['notice_period']
    e_phone = data['phone']
    e_qualification = data['qualification']
    e_skills = data['skills']
    user_email = session["email"]
    user = database.get_user_details(user_email)

    if len(user) != 0:
        try:
            user_id = user[0]["user_id"]
            job_statuses = database.get_job_status_for_user(user_id, job_id)
            if len(job_statuses) == 0:
                application_status = database.add_application(
                    user_id, job_id, e_email, e_name, e_experience,
                    e_notice_period, e_phone, e_qualification, e_skills)
                if application_status['status'] == 'Success':
                    flash('Successfully sent the application', 'success')
                else:
                    flash('Failed to send the application...Please try again',
                          'error')
                return redirect(url_for("get_job_details", job_id=job_id))
            else:
                for job_status in job_statuses:
                    if job_status['application_status'] == "Applied":
                        flash("You have already applied for this job",
                              "success")
                        return redirect(
                            url_for("get_job_details", job_id=job_id))
                    elif job_status['application_status'] == "Selected":
                        flash("You are application was already shortlisted",
                              "success")
                        return redirect(
                            url_for("get_job_details", job_id=job_id))
                    else:
                        flash("You are application was rejected", "error")
                        return redirect(
                            url_for("get_job_details", job_id=job_id))

        except Exception as e:
            flash('Some internal error..Please try again later', 'error')
            return redirect(url_for("get_job_details", job_id=job_id))
    else:
        flash('Please Re-login and try again', 'error')
        return redirect(url_for("get_job_details", job_id=job_id))


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


@app.route("/api/<job_id>/status")
def get_job_status_for_user(job_id):
    user_id = request.args.get('user_id')
    job_status = database.get_job_status_for_user(user_id, job_id)
    return jsonify(job_status)


@app.route("/api/users/<email>")
def list_users(email):
    user_details = database.get_user_details(email)
    return jsonify(user_details)


@app.route("/api/users/byPyhone/<phone>")
def list_users_by_phone(phone):
    try:
        user_details = database.get_user_details_for_phone(phone)
        return jsonify(user_details)
    except:
        return []


@app.route("/api/application/<application_id>/<status>")
def update_application_status(application_id, status):
    if status == "Selected" or status == "Rejected" or status == "Applied":
        try:
            application_details = database.get_application_details(application_id)
            if(len(application_details) !=0 ):
                user_details = database.update_application_status(
                    application_id, status)
                print(user_details)
                return jsonify(user_details)
            else:
                return {"status": "Failed", "message": "Application not found"}
        except Exception as e:
            return {"satus": "Failed", "message": str(e)}
    else:
        return {"status": "Failed", "message": "Invalid status"}


@app.route("/api/createSession", methods=['POST'])
def create_session():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = database.get_user_details(email)
    if password == user[0]["user_password"]:
        session.permanent = True
        session["email"] = email
        session["user_fname"] = user[0]["fname"]
        session["user_lname"] = user[0]["lname"]
        session["user_phone"] = user[0]["user_phone"]
        session["user_id"] = user[0]["user_id"]
        print(session)
        return {"status": 'Success', "message": "Successfully created session"}
    else:
        return {"satus": 'Failed', "message": "Invalid password"}


@app.route("/api/myDeals", methods=["GET"])
def get_my_deals():
    status = request.args.get('status', default="All")
    if session.get('user_id') is not None:
        my_applications = database.load_my_deals_from_db(session['user_id'])
        my_deals = []
        for application in my_applications:
            job_details = database.get_job_details(application["job_id"])
            if application["application_status"] == status or status == "All":
                my_deals.append({
                    "application_id": application["application_id"],
                    "job_id": application["job_id"],
                    "job_title": job_details[0]["job_title"],
                    "location": job_details[0]["location"],
                    "job_company": job_details[0]["company"],
                    "salary": job_details[0]["salary"],
                    "job_status": application["application_status"]
                })
        if len(my_deals) != 0:
            return {
                "status": "Success",
                "message": "Successfully fetched",
                "data": my_deals
            }
        else:
            return {
                "status": "Failed",
                "message": "No applications found",
                "data": []
            }
    else:
        return {
            "staus": "Failed",
            "message": "Authentication Required",
            "data": []
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
