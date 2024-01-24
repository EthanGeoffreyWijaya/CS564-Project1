drop table if exists Items;
drop table if exists Bids;
drop table if exists Categories;
drop table if exists Users;

create table Items(
    ItemID integer,
    Name varchar(255),
    Currently double,
    Buy_Price double,
    First_Bid double,
    Number_of_Bids integer,
    Started datetime,
    Ends datetime,
    UserID varchar(255),
    Description varchar(1000),
    primary key (ItemID),
    foreign key (UserID) references Users
);

create table Bids(
    ItemID integer,
    UserID varchar(255),
    Time  datetime,
    Amount double,
    primary key (ItemID, UserID, Time),
    foreign key (ItemID) references Items,
    foreign key (UserID) references Users
);

create table Categories(
    ItemID integer,    
    Category varchar(255),
    primary key (ItemID, Category),
    foreign key (ItemID) references Items
);

create table Users(
    UserID varchar(255),
    Rating integer,
    Location varchar(255),
    Country varchar(255),
    primary key (UserID)
);