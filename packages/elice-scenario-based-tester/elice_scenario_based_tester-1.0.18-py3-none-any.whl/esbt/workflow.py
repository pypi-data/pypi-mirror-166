from __future__ import annotations

import hashlib
from functools import cached_property
from typing import Any, Dict, Union

import aiohttp
import msgpack
from pydantic import BaseModel


class Workflow(BaseModel):
    dependency: Dict[tuple[str, Any], list[tuple[str, Any]]]
    context: Dict[str, Union[str, bool]]
    session: aiohttp.ClientSession

    @cached_property
    def ident(self) -> str:
        return hashlib.sha256(msgpack.packb(self.dict())).hexdigest()

    class Config:
        keep_untouched = (cached_property,)
        arbitrary_types_allowed = True


def init_dependency(
    dependency: Dict[tuple[str, Any], list[tuple[str, Any]]]
):
    for k, v in dependency.items():
        workflow.dependency[k] = v


workflow = Workflow(
    dependency={},
    context={},
    session=aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)),
)
