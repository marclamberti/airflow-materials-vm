CREATE TABLE sources(
    name VARCHAR(60),
    activated BOOLEAN
);

INSERT INTO sources(name, activated) VALUES('MySQL', true);
INSERT INTO sources(name, activated) VALUES('S3', false);
INSERT INTO sources(name, activated) VALUES('Mongo', false);
INSERT INTO sources(name, activated) VALUES('PostgreSQL', false);