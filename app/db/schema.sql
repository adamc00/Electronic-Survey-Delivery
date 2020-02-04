CREATE TABLE Login (
  ID              INTEGER PRIMARY KEY,
  Password        TEXT,
  UserID          TEXT,
  gender          TEXT, -- M/F
  age             INTEGER,
  working_years   INTEGER,
  working_months  INTEGER,
  job_years       INTEGER,
  job_months      INTEGER,
  emp_stat        INTEGER -- full/part/casual/contract
);

.mode csv
.headers on
.import Login.csv Login

CREATE TABLE Questions (
  ID              INTEGER PRIMARY KEY,
  Scale_min       INTEGER,
  Scale_no        INTEGER,
  Question        TEXT,
  Scale_min_label TEXT,
  Scale_max_label TEXT,
  Item            TEXT,
  QuestOrder      INTEGER,
  Section         TEXT,
  Question_no     INTEGER,
  Blurb           TEXT
);

.mode csv
.headers on
.import Questions.csv Questions

CREATE TABLE Data (
  ID            INTEGER PRIMARY KEY,
  UserID        INTEGER,
  Item          TEXT,
  StoredValue   INTEGER
);

.mode csv
.headers on
.import Data.csv Data
