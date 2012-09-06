drop table if exists tritina;
create table games (
  id integer primary key autoincrement,
  board string not null,
);