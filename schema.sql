drop table if exists games;
create table games (
  id integer primary key autoincrement,
  board string not null,
  text string not null
);