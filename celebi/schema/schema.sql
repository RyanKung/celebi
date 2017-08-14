CREATE TABLE datum(
       id serial primary key,
       name varchar(200),
       rate integer default 1,
       generator text,
       is_spout boolean default False,
       flying boolean default True,
       created_at timestamp default now(),
       comment text
);

CREATE TABLE datum(
       id serial,
       ts timestamp default now(),
       dataset integer,
       index text default '',
       datum json default '{}',
       tags text default '',
       primary key (qubit, ts)
);
