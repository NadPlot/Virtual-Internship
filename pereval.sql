CREATE SEQUENCE IF NOT EXISTS coord_id_seq;
CREATE TABLE "public"."pereval_coords"(
    "id" int4 NOT NULL DEFAULT nextval('coord_id_seq'::regclass),
    "latitude" numeric,
    "longitude" numeric,
    "height" int,
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS level_id_seq;
CREATE TABLE "public"."pereval_level"(
    "id" int4 NOT NULL DEFAULT nextval('level_id_seq'::regclass),
    "winter" text,
    "summer" text,
    "autumn" text,
    "spring" text,
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS user_id_seq;
CREATE TABLE "public"."pereval_users"(
    "id" int4 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    "email" varchar(80),
    "fam" varchar(80),
    "name" varchar(80),
    "otc" varchar(80),
    "phone" varchar,
    PRIMARY KEY ("id"),
    CONSTRAINT email_unique UNIQUE ("email")
);

CREATE SEQUENCE IF NOT EXISTS pereval_areas_id_seq;
CREATE TABLE "public"."pereval_areas"(
    "id" int8 NOT NULL DEFAULT nextval('pereval_areas_id_seq'::regclass),
    "id_parent" int8 NOT NULL,
    "title" text,
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS pereval_foto_id_seq;
CREATE TABLE "public"."pereval_foto"(
    "id" int4 NOT NULL DEFAULT nextval('pereval_foto_id_seq'::regclass),
    "date_added" timestamp DEFAULT now(),
    "title" text,
    "img" bytea,
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS pereval_id_seq;
CREATE TABLE "public"."pereval_added"(
    "id" int4 NOT NULL DEFAULT nextval('pereval_id_seq'::regclass),
    "add_time" timestamp,
    "beauty_title" text,
    "title" text,
    "other_titles" text,
    "connect" text,
    "user_id" int4 NOT NULL,
    "coords_id" int4 NOT NULL,
    "level_id" int4 NOT NULL,
    FOREIGN KEY ("user_id")  REFERENCES "pereval_users" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("coords_id") REFERENCES "pereval_coords" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("level_id") REFERENCES "pereval_level" ("id") ON DELETE CASCADE,
    PRIMARY KEY ("id")
);
ALTER TABLE "pereval_added" ADD COLUMN "status" text;

CREATE SEQUENCE IF NOT EXISTS pereval_images_id_seq;
CREATE TABLE "public"."pereval_images"(
    "id" int4 NOT NULL DEFAULT nextval('pereval_images_id_seq'::regclass), 
    "pereval_id" int4, 
    "foto_id" int4, 
    FOREIGN KEY ("pereval_id") REFERENCES "pereval_added" ("id") ON DELETE CASCADE, 
    FOREIGN KEY ("foto_id") REFERENCES "pereval_foto" ("id") ON DELETE CASCADE, 
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS untitled_table_200_id_seq;
CREATE TABLE "public"."spr_activities_types" (
    "id" int4 NOT NULL DEFAULT nextval('untitled_table_200_id_seq'::regclass),
    "title" text,
    PRIMARY KEY ("id")
);


INSERT INTO "public"."pereval_users" ("email", "fam", "name", "otc", "phone") VALUES ('user@email.ltd', 'Пупкин', 'Василий', 'Иванович', '79031234567');
INSERT INTO "public"."pereval_coords" ("latitude", "longitude", "height") VALUES (45.3842, 7.1525, 1200);
INSERT INTO "public"."pereval_level" ("winter", "summer", "autumn", "spring") VALUES ('', '1A', '1A', '');
INSERT INTO "public"."pereval_added" ("add_time", "beauty_title", "title", "other_titles", "user_id", "coords_id", "level_id", "status") 
    VALUES ('2021-09-22 13:18:13', 'пер.', 'Пхия', 'Триев', 1, 1, 1, 'pending');
INSERT INTO "public"."pereval_foto" ("date_added", "title", "img") VALUES ('2021-09-22 13:18:13', 'some title', 'some img');
INSERT INTO "public"."pereval_images" ("pereval_id", "foto_id") VALUES (1, 1);

