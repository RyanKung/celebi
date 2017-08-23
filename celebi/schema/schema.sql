CREATE TABLE ts_data(
       id serial primary key,
       name varchar(200),
       rate integer default 1,
       generator text,
       is_spout boolean default False,
       flying boolean default True,
       created_at timestamp default now(),
       comment text
);

CREATE TABLE ts_datum(
       id serial,
       ts timestamp default now(),
       index text default '',
       datum json default '{}',
       tags text default '',
       dataset integer,
       primary key (dataset, ts)
);
