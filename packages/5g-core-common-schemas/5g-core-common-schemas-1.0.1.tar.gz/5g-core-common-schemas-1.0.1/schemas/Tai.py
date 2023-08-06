# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from schemas.PlmnId import PlmnId
from schemas.Tac import Tac


class Tai(BaseModel):
    plmnId: PlmnId
    tac: Tac
