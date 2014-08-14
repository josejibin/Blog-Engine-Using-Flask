drop table if exists posts;
create table posts(
  id integer primary key autoincrement,
  title text not null,
  catogory text,
  t_comments integer,
  p_date date,
  post text not null
);
drop table if exists comments;
create table comments(
 c_id text not null,
 c_name text,
 comment text,
 FOREIGN KEY(c_id) REFERENCES posts(title)
)