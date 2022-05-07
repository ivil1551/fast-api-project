CREATE DATABASE testDB;
USE testDB;
CREATE TABLE user_table
(
user_id int auto_increment,
user_name varchar(10) not null,
created_time bigint not null,
primary key (user_id),
unique (user_name)
);

-- created tweets_table as tweet_table, tweet_table1 ........upto  tweet_table9:
CREATE TABLE tweets_table
(
tweet_id int auto_increment,
user_id int not null,
created_time bigint not null,
tweet varchar(140) not null,
primary key (tweet_id),
foreign key (user_id) references user_table(user_id)
);

CREATE TABLE tweets_table1
(
tweet_id int auto_increment,
user_id int not null,
created_time bigint not null,
tweet varchar(140) not null,
primary key (tweet_id),
foreign key (user_id) references user_table(user_id)
);

show tables;

SELECT tweets_table.*
FROM tweets_table
LEFT JOIN user_table
ON tweets_table.user_id = user_table.user_id where user_table.user_name like 'testuser1' and tweets_table.created_time >=1651904727;
