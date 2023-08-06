from dataclasses import dataclass
from typing import Optional, List, Any, Dict 
from omegaconf import MISSING
from enum import Enum


@dataclass
class SamplerConfig:
    _target_: str = MISSING

class DistributionType(Enum):
    int = 1
    float = 2
    categorical = 3


class Direction(Enum):
    minimize = 1
    maximize = 2