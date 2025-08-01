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

CREATE TABLE student_statuses (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(256)
);

INSERT INTO student_statuses (name) VALUES
    ('учится'),
    ('отчислен'),
    ('выпущен');

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
    "exam_date" VARCHAR(256),
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
    "status" INTEGER REFERENCES student_statuses(id),
    "payments" JSONB[],
    "comments" VARCHAR(256),
    "graduation_date" DATE,
    "grade_1" INTEGER,
    "grade_2" INTEGER,
    "full_name_bel" VARCHAR(128),
    "profession_bel" VARCHAR(256)
);

CREATE TABLE professions (
    id SERIAL PRIMARY KEY,
    code VARCHAR,
    name VARCHAR,
    etks VARCHAR,
    education_durations VARCHAR[] NULL,
    education_categories VARCHAR[] NOT NULL,
    retraining_only BOOLEAN DEFAULT FALSE,
    advance_duration DOUBLE PRECISION NULL,
    bondarenko VARCHAR NULL,
    name_bel VARCHAR NULL,
    has_google_link BOOLEAN DEFAULT FALSE,
    has_grades BOOLEAN DEFAULT FALSE,
    has_diary BOOLEAN DEFAULT FALSE
);

CREATE TABLE professions_hours (
    id SERIAL PRIMARY KEY,
    duration DOUBLE PRECISION,
    theory_hours INTEGER,
    practice_hours INTEGER
);

COPY students(referrer_organization,"group",full_name,term,start_date,theory_end_date,practice_start_date,practice_end_date,end_date,profession,degree,education_type_id,"login",email,birth_date,education_id,previous_profession,payment,organization,theory_hours,practice_hours,practice_organization,status,comments)
FROM '/docker-entrypoint-initdb.d/students.csv'
DELIMITER ','
CSV HEADER;
