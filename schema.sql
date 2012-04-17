drop table if exists entries;

create table board (
	id integer primary key,
);

create table person (
	id integer primary key autoincrement,
	name text,
	score integer default 0,
	personboard integer,
	foreign key(personboard) references board(id)
);

create table tile (
	id integer autoincrement,
	value integer default 0,
	tileboard integer,
	foreign key(tileboard) references board(id)
);