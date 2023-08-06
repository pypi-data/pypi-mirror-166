# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from schemas.Uinteger import Uinteger


class Snssai(BaseModel):
    sst: Uinteger
    sd: str
