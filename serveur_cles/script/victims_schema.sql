drop table if exists decrypted;
drop table if exists encrypted;
drop table if exists states;
drop table if exists victims;

CREATE TABLE victims(
    id_victim INTEGER PRIMARY KEY ,
    os VARCHAR ,
    hash VARCHAR ,
    disks VARCHAR ,
    key VARCHAR
);

CREATE TABLE decrypted(
    id_decrypted INTEGER PRIMARY KEY ,
    id_victim INTEGER ,
    datetime timestamp ,
    nb_files INTEGER ,
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE states(
    id_states INTEGER PRIMARY KEY ,
    id_victim INTEGER ,
    datetime timestamp ,
    state VARCHAR ,
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE encrypted(
    id_encrypted INTEGER PRIMARY KEY ,
    id_victim INTEGER ,
    datetime timestamp ,
    nb_files INTEGER ,
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);


