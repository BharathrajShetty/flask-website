import pymysql
import os


def db_connection():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_NAME'],
        host=os.environ['HOST'],
        password=os.environ['PASSWORD'],
        read_timeout=timeout,
        port=int(os.environ['DB_PORT']),
        user=os.environ['USER'],
        write_timeout=timeout,
    )
    return connection


def exec_simple_db_queries(query):
    connection = db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        connection.close()


def exec_write_db_queries(query):
    connection = db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return {"status": 'Success', "message": "Successfully executetd query"}
    except Exception as e:
        return {"status": 'Failed', "message": str(e)}
    finally:
        connection.close()


def addUser(fname, lname, phone, email, password):
    query = f"INSERT INTO users (fname, lname, user_phone, user_email, user_password) VALUES ('{fname}', '{lname}', '{phone}', '{email}', '{password}');"
    return exec_write_db_queries(query)


def load_jobs_from_db():
    query = "SELECT * FROM jobs"
    return exec_simple_db_queries(query)


def get_user_details(email):
    query = f"SELECT * FROM users where user_email = '{email}'"
    return exec_simple_db_queries(query)


def get_user_details_for_phone(phone):
    query = f"SELECT * FROM users where user_phone = '{phone}'"
    return exec_simple_db_queries(query)


def get_job_details(job_id):
    query = f"SELECT * FROM jobs where id = {job_id}"
    return exec_simple_db_queries(query)


def get_faqs_from_db():
    query = "SELECT * FROM faqs"
    return exec_simple_db_queries(query)


if __name__ == "__main__":
    job_details = get_job_details(2)
    print(len(job_details))
