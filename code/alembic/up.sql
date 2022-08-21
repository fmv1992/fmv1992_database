BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 7e64e2a8f778

INSERT INTO alembic_version (version_num) VALUES ('7e64e2a8f778') RETURNING alembic_version.version_num;

COMMIT;

