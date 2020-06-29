create database "Prod.Filed.Facebook.Potter.Accounts";
create table BusinessOwners (
    id int identity (1,1),
	facebook_id varchar(255) not null,
	name varchar(255),
	email varchar(255),
    token varchar(255) not null,
    page_id varchar(255) not null,
    created_at datetime not null,
    updated_at datetime not null
	primary key (id)
);