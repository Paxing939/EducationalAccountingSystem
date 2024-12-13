i = 2
if i == 0:
    import requests

    url = "http://localhost:8000/students/"
    payload = {
        "name": "John Doe",
        "age": 22,
        "education_type": 1,
        "profession_id": 101
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Student created successfully:", response.json())
    else:
        print("Failed to create student:", response.status_code, response.text)
elif i == 1:
    import psycopg2

    DATABASE_URL = "postgresql://user:password@localhost:5443/students_db"

    conn = psycopg2.connect(DATABASE_URL)

    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()
elif i == 2:
    import requests

    url = "http://localhost:8002/login"
    payload = {
        "username": "Denis",
        "password" : "123456"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Student created successfully:", response.json())
    else:
        print("Failed to create student:", response.status_code, response.text)