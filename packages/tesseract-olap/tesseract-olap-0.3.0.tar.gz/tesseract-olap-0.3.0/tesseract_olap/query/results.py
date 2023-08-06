"""Result structs module

This module contains wrapper classes for the resulting data of queries obtained
for structs in the requests module.
"""

from dataclasses import dataclass
from typing import AsyncIterable

from tesseract_olap.common import AnyDict, Array

from .requests import DataRequest, MembersRequest


@dataclass(eq=False, frozen=True, order=False)
class DataResult:
    """Container class for results to :class:`DataRequest`."""
    data: AsyncIterable[AnyDict]
    sources: Array[AnyDict]
    query: DataRequest


@dataclass(eq=False, frozen=True, order=False)
class MembersResult:
    """Container class for results to :class:`MembersRequest`."""
    data: AsyncIterable[AnyDict]
    query: MembersRequest
