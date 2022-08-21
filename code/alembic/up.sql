BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 7e64e2a8f778

INSERT INTO alembic_version (version_num) VALUES ('7e64e2a8f778') RETURNING alembic_version.version_num;

-- Running upgrade 7e64e2a8f778 -> aaaaaaaaaaaa

create schema "fmv1992_backup_system";;

UPDATE alembic_version SET version_num='aaaaaaaaaaaa' WHERE alembic_version.version_num = '7e64e2a8f778';

COMMIT;

BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 7e64e2a8f778

INSERT INTO alembic_version (version_num) VALUES ('7e64e2a8f778') RETURNING alembic_version.version_num;

-- Running upgrade 7e64e2a8f778 -> aaaaaaaaaaaa

create schema "fmv1992_backup_system";;

UPDATE alembic_version SET version_num='aaaaaaaaaaaa' WHERE alembic_version.version_num = '7e64e2a8f778';

-- Running upgrade aaaaaaaaaaaa -> e78e293854a8

CREATE TABLE fmv1992_backup_system.id_to_binary (
    id VARCHAR(32) NOT NULL, 
    is_compressed BOOLEAN NOT NULL, 
    comment VARCHAR DEFAULT '' NOT NULL, 
    "binary" OID NOT NULL, 
    PRIMARY KEY (id)
);

COMMENT ON COLUMN fmv1992_backup_system.id_to_binary.id IS 'Unique ID of every primary blob.

I decided to use `xxHash` for its collision resistance and speed.

Hash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).

# Related links:

1.  <https://github.com/Cyan4973/xxHash>.';

COMMENT ON COLUMN fmv1992_backup_system.id_to_binary.is_compressed IS 'Tells whether the `binary` column is compressed or not.

If it is not compressed then `id = hash(binary)`. If it is compressed then `id = hash(uncompressed(binary))`.';

COMMENT ON COLUMN fmv1992_backup_system.id_to_binary.comment IS 'Comment associated with the binary.';

COMMENT ON COLUMN fmv1992_backup_system.id_to_binary."binary" IS 'Sequence of bytes uniquely associated with an `id`.

This is the heart of the `fmv1992_backup_system` schema.

# Relevant extracts of the documentation:

*   "Client applications cannot use these functions while a libpq connection is in pipeline mode.".

*   How to import and export:

    ```
    Oid lo_import(PGconn *conn, const char *filename);
    ```

    ```
    int lo_export(PGconn *conn, Oid lobjId, const char *filename);
    ```

# References:

*   [Chapter 35. Large Objects](https://www.postgresql.org/docs/14/largeobjects.html).

*   [F.20. lo](https://www.postgresql.org/docs/14/lo.html): `lo` stands for "Large Object".';

CREATE TABLE fmv1992_backup_system.access_record (
    id VARCHAR(32) NOT NULL, 
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL, 
    PRIMARY KEY (id, timestamp), 
    FOREIGN KEY(id) REFERENCES fmv1992_backup_system.id_to_binary (id)
);

COMMENT ON COLUMN fmv1992_backup_system.access_record.id IS 'Unique ID of every primary blob.

I decided to use `xxHash` for its collision resistance and speed.

Hash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).

# Related links:

1.  <https://github.com/Cyan4973/xxHash>.';

COMMENT ON COLUMN fmv1992_backup_system.access_record.timestamp IS 'Timestamp associated with the backed up file/binary blob.';

CREATE TABLE fmv1992_backup_system.backups (
    id VARCHAR(32) NOT NULL, 
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL, 
    path VARCHAR NOT NULL, 
    is_symlink BOOLEAN NOT NULL, 
    PRIMARY KEY (id, timestamp, path), 
    FOREIGN KEY(id) REFERENCES fmv1992_backup_system.id_to_binary (id)
);

COMMENT ON COLUMN fmv1992_backup_system.backups.id IS 'Unique ID of every primary blob.

I decided to use `xxHash` for its collision resistance and speed.

Hash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).

# Related links:

1.  <https://github.com/Cyan4973/xxHash>.';

COMMENT ON COLUMN fmv1992_backup_system.backups.timestamp IS 'Timestamp associated with the backed up file/binary blob.';

UPDATE alembic_version SET version_num='e78e293854a8' WHERE alembic_version.version_num = 'aaaaaaaaaaaa';

COMMIT;

