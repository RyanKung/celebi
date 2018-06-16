CREATE TABLE ts_data(
       id serial primary key,
       name varchar(200),
       created_at timestamp default now(),
       comment text
);

CREATE TABLE ts_datum(
       id serial,
       ts timestamp default now(),
       datum json default '{}',
       dataset integer,
       primary key (dataset, ts)
);


CREATE TABLE ts_tag_of_datum(
       ts_datum integer,
       ts_tag integer
)

CREATE TABLE ts_tag_of_data(
       ts_data integer,
       ts_tag integer
);

CREATE TABLE ts_tag(
       id serial,
       comment text,
       name varchar(200)
);

CREATE TABLE ts_label(
       id serial,
       comment text,
       name varchar(200)
);

