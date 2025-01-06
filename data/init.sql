CREATE TABLE education_types (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(256)
);

INSERT INTO education_types (name) VALUES
    ('подготовка'),
    ('переподготовка'),
    ('повышение квалификации'),
    ('инструктаж');

CREATE TABLE educations (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(256)
);

INSERT INTO educations (name) VALUES
    ('среднее'),
    ('средне-специальное'),
    ('профессиональное-техническое'),
    ('высшее');

CREATE TABLE students (
    "id" SERIAL PRIMARY KEY,
    "referrer_organization" VARCHAR(256),
    "group" VARCHAR(10),
    "full_name" VARCHAR(128),
    "term" DOUBLE PRECISION,
    "start_date" DATE,
    "theory_end_date" DATE,
    "practice_start_date" DATE,
    "practice_end_date" DATE,
    "end_date" DATE,
    "exam_date" DATE,
    "profession" VARCHAR(256),
    "degree" INTEGER,
    "education_type_id" INTEGER REFERENCES education_types(id),
    "login" VARCHAR(128),
    "email" VARCHAR(128),
    "birth_date" DATE,
    "education_id" INTEGER REFERENCES educations(id),
    "previous_profession" VARCHAR(256),
    "payment" DOUBLE PRECISION,
    "organization" VARCHAR(256),
    "protocol_number" VARCHAR(20),
    "certificate_number" VARCHAR(20),
    "grad_id" INTEGER,
    "theory_hours" INTEGER,
    "practice_hours" INTEGER,
    "practice_organization" VARCHAR(256),
    "status" INTEGER,
    "payments" JSONB[],
    "comments" VARCHAR(256),
    "graduation_date" DATE,
    "grade_1" INTEGER,
    "grade_2" INTEGER,
    "full_name_bel" VARCHAR(128),
    "profession_bel" VARCHAR(256)
);

COPY students(referrer_organization,full_name,term,profession,education_type_id,login,birth_date,education_id,previous_profession,payment,organization,protocol_number,certificate_number,grad_id,theory_hours,practice_hours,practice_organization,status,comments)
FROM '/docker-entrypoint-initdb.d/students.csv'
DELIMITER ','
CSV HEADER;
