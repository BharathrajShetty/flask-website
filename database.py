import pymysql
import os


def load_jobs_from_db():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_NAME'],
        host=os.environ['HOST'],
        password=os.environ['PASSWORD'],
        read_timeout=timeout,
        port=int(os.environ['PORT']),
        user= os.environ['USER'],
        write_timeout=timeout,
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM jobs")
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        connection.close()

if __name__ == "__main__":
    print(load_jobs_from_db())