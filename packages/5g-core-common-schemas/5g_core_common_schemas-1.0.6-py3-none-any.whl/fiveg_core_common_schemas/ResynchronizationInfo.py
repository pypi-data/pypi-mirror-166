# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.


from Auts import Auts
from pydantic import BaseModel
from Rand import Rand


class ResynchronizationInfo(BaseModel):
    rand: Rand
    auts: Auts
