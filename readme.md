# `fmv1992_backup_system`

???.

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

## v0.0.0 - 2022-07-24

*   Added this changelog.

## TODO
