CREATE TABLE users
(
    user_id bigint NOT NULL PRIMARY KEY,
    username CHARACTER varying(30) NOT NULL,
    language CHARACTER varying(10),
    id SERIAL NOT NULL
);

ALTER TABLE users
    OWNER TO postgres;

CREATE UNIQUE INDEX users_id_uindex
    on users (id);

CREATE TABLE daily_stats
(
    id SERIAL NOT NULL,
    day DATE NOT NULL PRIMARY KEY,
    users_count INTEGER DEFAULT 0 NOT NULL
);

ALTER TABLE daily_stats
    OWNER TO postgres;

CREATE UNIQUE INDEX daily_stats_id_uindex
    on daily_stats (id);