#DROP TABLE IF EXISTS user;

create table user(
	id int(11) not null,
	name varchar(25),
	depid int(11),
	salary float
)ENGINE=InnoDB DEFAULT CHARSET=utf8

create table school(
    id int(11) not null auto_increment,
    school_name varchar(255),
    lectures_num int(11),
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8