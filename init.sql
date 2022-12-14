BEGIN;

CREATE DOMAIN email AS text -- un domaine (type de donnée) permettant de vérifier la validiter d'une adresse email via une regex

	--CHECK (VALUE ~* '^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'

	CHECK (

		VALUE ~* '^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'
	);


CREATE TABLE "user"(
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username text NOT NULL,
    email email NOT NULL UNIQUE,
    "password" text NOT NULL
);

CREATE TABLE "history"(
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    image text NOT NULL,
    emotion text NOT NULL,
    user_id int NOT NULL REFERENCES "user"(id)
);

COMMIT;