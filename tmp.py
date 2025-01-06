import requests
i = 3
if i == 0:
    url = "http://localhost:8000/students/"
    payload = {
        "name": "Ivan",
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

    some_query = """
    SELECT
        table_schema,
        table_name,
        column_name,
        data_type
    FROM
        information_schema.columns
    WHERE
        table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY
        table_schema,
        table_name,
        ordinal_position;
    """

    cur.execute("SELECT * FROM students")
    # cur.execute(some_query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()
elif i == 2:

    url = "http://localhost:8002/login"
    payload = {
        "username": "Ivan",
        "password" : "5432"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if response.status_code == 200:
        print("current_user:", response.json().get("access_token"))
    else:
        print("Failed to enter:", response.status_code, response.text)
elif i == 3:

    # URL для аутентификации
    auth_url = "http://localhost:8002/login"
    auth_payload = {
        "username": "Ivan",
        "password": "5432"
    }
    auth_headers = {
        "Content-Type": "application/json"
    }

    # Отправка запроса на аутентификацию
    auth_response = requests.post(auth_url, json=auth_payload, headers=auth_headers)

    # Проверка ответа
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data.get("access_token")
        print(f"Token: {token}")
elif i == 4:
    url = "http://localhost:8000/students/"
    payload = {
        "referrer_organization": "ural govno zavod",
        "age": 22,
        "education_type": 1,
        "profession_id": 101
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Student created successfully:", response.json())
    else:
        print("Failed to create student:", response.status_code, response.text)