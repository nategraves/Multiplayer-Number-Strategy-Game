drop table if exists games;
create table games (
  id integer primary key autoincrement,
  board blob not null
);