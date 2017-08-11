CREATE TABLE datum(
       id serial primary key,
       name varchar(200),
       rate integer default 1,
       monad text,
       entangle varchar(200),
       is_stem boolean default False,
       is_spout boolean default False,
       flying boolean default True,
       store boolean default True,
       created_at timestamp default now(),
       comment text
);

CREATE TABLE states(
       id serial,
       ts timestamp default now(),
       qubit integer,
       index text default '',
       datum json default '{}',
       tags text default '',
       primary key (qubit, ts)
);
