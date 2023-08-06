import logging
from contextlib import asynccontextmanager
from typing import AsyncIterable

from aioch import Client
from clickhouse_driver import errors

from tesseract_olap.backend import Backend
from tesseract_olap.backend.exceptions import UpstreamInternalError
from tesseract_olap.common import AnyDict
from tesseract_olap.query import DataQuery, MembersQuery
from tesseract_olap.schema import Schema

from .sqlbuild import dataquery_sql, membersquery_sql

logger = logging.getLogger("tesseract_olap.backend.clickhouse")


class ClickhouseBackend(Backend):
    """Clickhouse Backend class

    This is the main implementation for Clickhouse of the core :class:`Backend`
    class.

    Must be initialized with a connection string with the parameters for the
    Clickhouse database. Then must be connected before used to execute queries,
    and must be closed after finishing use.
    """

    connection_string: str

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def __repr__(self) -> str:
        return f"ClickhouseBackend('{self.connection_string}')"

    @asynccontextmanager
    async def _acquire(self):
        client = Client.from_url(self.connection_string)
        try:
            yield client
        except errors.ServerException as exc:
            raise UpstreamInternalError(str(exc)) from None
        finally:
            await client.disconnect()

    async def connect(self):
        pass

    def close(self):
        pass

    async def wait_closed(self):
        pass

    async def get_data(self, query: "DataQuery", **kwargs) -> AsyncIterable[AnyDict]:
        """Retrieves the dataset for the request made by the :class:`DataQuery`
        instance, from the database.
        """
        logger.debug("%r", query)

        sql_builder, sql_params = dataquery_sql(query)
        sql_query = sql_builder.get_sql()
        logger.debug("%s\n%s", sql_query, sql_params)

        async with self._acquire() as client:
            result = await client.execute_iter(query=sql_query,
                                               params=sql_params,
                                               settings={'max_block_size': 5000},
                                               with_column_types=True)
            columns, _ = zip(*(await result.__anext__()))
            async for row in result:
                yield dict(zip(columns, row))

    async def get_members(self, query: "MembersQuery", **kwargs):
        """Retrieves the members for the request made by the :class:`MembersQuery`
        instance, from the database.
        """
        logger.debug("%r", query)

        sql_builder, sql_params = membersquery_sql(query)
        sql_query = sql_builder.get_sql()
        logger.debug(sql_query, sql_params)

        async with self._acquire() as client:
            result = await client.execute_iter(query=sql_query,
                                               params=sql_params,
                                               settings={'max_block_size': 5000},
                                               with_column_types=True)
            columns, _ = zip(*(await result.__anext__()))
            async for row in result:
                yield dict(zip(columns, row))

    async def ping(self) -> bool:
        """Checks if the current connection is working correctly."""
        async with self._acquire() as client:
            result = await client.execute("SELECT 1")
            return result == [(1,)]

    async def validate_schema(self, schema: "Schema") -> None:
        """Checks all the tables and columns referenced in the schema exist in
        the backend.
        """
        # logger.debug("Schema %s", schema)
        # TODO: implement
        for cube in schema.cube_map.values():
            pass
        return None
