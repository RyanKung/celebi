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
       tags text default '',
       dataset integer,
       primary key (dataset, ts)
);
