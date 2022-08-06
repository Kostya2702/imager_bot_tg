CREATE TABLE users
(
    user_id bigint not null primary key,
    username character varying(30),
    territory character varying(30),
    language character varying(10),
    id serial not null
);

alter TABLE users
    owner to postgres;

CREATE unique index users_id_uindex
    on users (id);