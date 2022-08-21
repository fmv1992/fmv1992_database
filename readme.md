# `fmv1992_database`

???.

*   How do we want to handle symlinks?

* * *

```

cdp fmv1992_database
make docker_down
docker volume rm fmv1992_backup_system_fmv1992_backup_system_volume
docker volume rm fmv1992_database_fmv1992_database_volume
make docker_up
ALEMBIC_TARGET_ID='head' make docker_build alembic_upgrade
rm **/*create_the_idtoblob_table*
rm ./code/alembic/up.sql
ALEMBIC_MESSAGE='Create the `IdToBlob` table.' make docker_build alembic_autogenerate_upgrade
```

* * *

See <http://localhost:1993/project/1/task/177#comments>.

Features:

1.  Fully fledged backup.

    1.  Is able to restore the files everything that makes files operational:

        *   Contents.

        *   Permissions.

        *   Paths (absolute; `backup`s (e.g. `tar://` ?)).

    1.  Avoids redundancy. Assume that we will backup the same data a lot of times, so we must be smart about it.

1.  Support existing `backup`'s output (`.tar.gz` files). Decompress them as needed.

## API

## Quality standards

*   <https://keepachangelog.com/en/1.0.0/>.

    *   Sample project: `download_website_as_txt`.

*   <https://semver.org/spec/v2.0.0.html>.

    *   Sample project: `download_website_as_txt`.

## Changelog

<!-- `comm3ab5c17`: For a full changelog example. -->

## Unreleased

*   Add a database migration.

*   [Repurpose this to be my multipurpose database](http://localhost:1993/project/1/task/178#comment-175).

## v0.0.0 - 2022-07-24

*   Added this changelog.

## TODO
