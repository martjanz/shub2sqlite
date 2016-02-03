CREATE TABLE "shub_projects" ("id" INTEGER PRIMARY KEY  NOT NULL , "shub_id" INTEGER);
CREATE TABLE "shub_jobs" ("id" INTEGER PRIMARY KEY  NOT NULL , "shub_id" TEXT, "raw_json" JSON);
CREATE TABLE "shub_items" ("id" INTEGER PRIMARY KEY  NOT NULL , "raw_json" JSON, "shub_job_id" TEXT);
