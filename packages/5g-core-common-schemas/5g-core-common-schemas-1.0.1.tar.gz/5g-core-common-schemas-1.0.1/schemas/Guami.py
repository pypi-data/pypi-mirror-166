# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from schemas.AmfId import AmfId
from schemas.PlmnId import PlmnId


class Guami(BaseModel):
    plmnId: PlmnId
    amfId: AmfId
