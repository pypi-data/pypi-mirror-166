# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from schemas.Mcc import Mcc
from schemas.Mnc import Mnc


class PlmnId(BaseModel):
    mcc: Mcc
    mnc: Mnc
