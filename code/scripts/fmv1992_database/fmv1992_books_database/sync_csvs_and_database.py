"""Sync CSV files and `fmv1992_database.fmv1992_books`.

See how to use `sqlalchemy` in the most forward compatible way here:
<https://docs.sqlalchemy.org/en/14/changelog/migration_20.html>.
"""
import os

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import engine_from_config

import fmv1992_books_database
from fmv1992_database.lib import get_fmv1992_database_engine


def get_df_path_from_table_name(table):
    return os.path.join(
        "data", "database", "fmv1992_books_database", table.name + ".csv"
    )


def copy_df_structure(df, **kwargs):
    return pd.DataFrame(
        data=None, index=df.index, columns=df.columns, **kwargs
    )


def main():
    # Load all tables from the `???` schema.
    df_db_dict = {}

    with get_fmv1992_database_engine().begin() as connection:
        for table in fmv1992_books_database.Base.metadata.sorted_tables:
            select_statement = (
                # Use `String()` objects; `pandas` is "smartly" casting things.
                sa.select([sa.cast(x, sa.types.String()) for x in table.c])
                .select_from(table)
                .order_by(*list(table.primary_key))
                .compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={"literal_binds": True},
                )
                .string
            )
            pk = list(map(lambda x: x.name, table.primary_key))
            df_db_dict[table.name] = pd.read_sql(
                select_statement,
                connection,
                index_col=pk,
            )

    # Load all data already stored in the CSVs.
    df_csv_dict = {}
    with get_fmv1992_database_engine().begin() as connection:
        for table in fmv1992_books_database.Base.metadata.sorted_tables:
            csv_path = get_df_path_from_table_name(table)
            if os.path.exists(csv_path):
                df_csv_dict[table.name] = pd.read_csv(
                    csv_path,
                    dtype=str,
                    sep="\t",
                )
                pk = list(map(lambda x: x.name, table.primary_key))
                df_csv_dict[table.name] = df_csv_dict[table.name].set_index(pk)
            else:
                df_csv_dict[table.name] = copy_df_structure(
                    df_db_dict[table.name],
                    # index_col="isbn13"
                )

    # pass
    # import ipdb
    # ipdb.set_trace()
    # pass

    # Merge the information. Give precedence to what is specified in the CSV files.
    df_merged_dict = {}
    for table in fmv1992_books_database.Base.metadata.sorted_tables:
        df_csv = df_csv_dict[table.name]
        df_db = df_db_dict[table.name]
        df_union = pd.concat(
            (df_csv, df_db), axis=0, ignore_index=False
        ).reset_index()
        pk = list(map(lambda x: x.name, table.primary_key))
        df_union = df_union.drop_duplicates(subset=pk, keep="first")
        df_union = df_union.set_index(pk, verify_integrity=True)
        df_union = df_union.sort_index()
        df_merged_dict[table.name] = df_union

    # Re insert them back into the database.
    with get_fmv1992_database_engine().begin() as connection:
        for table in fmv1992_books_database.Base.metadata.sorted_tables:
            df_merged_dict[table.name].to_sql(
                table.name,
                connection,
                schema=fmv1992_books_database.SCHEMA,
                if_exists="replace",
                index=True,
            )

    # Re write the CSVs.
    for table in fmv1992_books_database.Base.metadata.sorted_tables:
        df_merged_dict[table.name].to_csv(
            get_df_path_from_table_name(table), sep="\t", index=True
        )


if __name__ == "__main__":
    main()
