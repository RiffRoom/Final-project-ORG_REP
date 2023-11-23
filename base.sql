drop table if exists  user_table cascade ;

create table user_table (
    id serial primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    user_name varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null,
    private boolean null default FALSE,
    phone int not null,
    prof_pic bytea null
);
insert into user_table(first_name, last_name, user_name, password, email, phone) values
('James', 'Bond', 'usern', 'psswd', 'jb@email.com', 1234567890); -- host id 1
insert into user_table(first_name, last_name, user_name, password, email, phone) values
('Jack', 'Daniel', 'usern2', 'psswd2', 'jd@email.com', 1234567777); -- host id 2
insert into user_table (first_name, last_name, user_name, password, email, phone)
values ('Todd', 'Mclovin', 'us3', 'p3', 'Mc@gmail.com', 1453456788); -- user 3

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
-- 35.30559659944004, -80.73257422631464
insert into sessions(host_name, title, message, date, date_posted, lat, long, host_id) values
('James Bond', 'Atkins slam', 'Crazy session at Atkins', '2023-03-01 14:12:00', '2023-02-14 14:12:00',35.30559659944004, -80.73257422631464, 1); -- sesh 1
-- 35.30752138310208, -80.73403424319967
insert into sessions(host_name, title, message, date, date_posted, lat, long, host_id) values
('Jack Daniel', 'whats up cato', 'Crazy educational session', '2023-03-01 09:15:00', '2023-01-12 14:12:00', 35.30752138310208, -80.73403424319967, 2);-- sesh 2

insert into sessions(host_name, title, message, date, date_posted, lat, long, host_id) values
('Todd Mclovin', 'MCLOVIN', 'Come on down', '2023-04-16 17:30:00', '2023-03-01 14:12:00', 35.30356435381034, -80.73075445239294, 3); -- sesh 3
insert into sessions(host_name, title, message, date, date_posted, lat, long, host_id) values
('Todd Mclovin', 'MCLOVIN PART 2', 'Come on down AGAIN', '2023-04-25 17:30:00', '2023-03-19 14:12:00', 35.30394085324328, -80.73147328440633, 3); -- sesh 3

drop table if exists party cascade ;
create table party(
    party_id serial primary key,
    session_id int not null,
    user_id int not null,
    user_name varchar(255) not null,
    foreign key (session_id) references sessions(id),
    foreign key (user_id) references user_table(id)
);

insert  into party(session_id, user_id, user_name) values (1, 2, 'Jack Daniel'); -- jack daniel is in james bond's party
insert  into party(session_id, user_id, user_name) values (2, 1, 'James Bond'); -- james bond is in jack daniel's party
insert into party(session_id, user_id, user_name) values (1, 3, 'Todd Mclovin'); -- Todd is now in James bond's party

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