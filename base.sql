drop table if exists  user_table cascade ;
create table user_table (
    id serial primary key,
    first_name varchar(255) null,
    last_name varchar(255) null,
    user_name varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null,
    private boolean null default FALSE,
    phone varchar(20) null,
    prof_pic varchar(255)
);

ALTER TABLE user_table
ADD COLUMN bio TEXT;

drop table if exists sessions cascade ;
create table sessions (
    id serial primary key,
    host_name varchar(255) not null,
    title varchar(255) not null,
    message varchar(255) not null,
    date timestamp not null,
    date_posted timestamp null,
    lat double precision not null,
    long double precision not null,
    host_id int not null,
    foreign key (host_id) references user_table(id)
);

drop table if exists party cascade ;
create table party(
    party_id serial primary key,
    session_id int not null,
    user_id int not null,
    foreign key (session_id) references sessions(id),
    foreign key (user_id) references user_table(id)
);

drop table if exists post cascade;
create table post(
    id serial primary key,
    video_id varchar(255) not null,
    title varchar(255) not null,
    msg varchar(255) null,
    ratio int not null,
    date_posted timestamp not null,
    user_id int not null,
    user_name varchar(255)    
);

drop table if exists comment_section cascade ;
create table comment_section(
    id serial primary key,
    post_id int not null,
    foreign key (post_id) references post(id)
);

insert into comment_section(post_id) values (1);

drop table if exists comments cascade ;
create table comments(
    id serial primary key,
    comment_section_id int not null,
    commenter_id int not null,
    commenter_name varchar(255) not null,
    message varchar(255) not null,
    post_time timestamp null,
    foreign key (comment_section_id) references  comment_section(id),
    foreign key (commenter_id) references user_table(id)
);

