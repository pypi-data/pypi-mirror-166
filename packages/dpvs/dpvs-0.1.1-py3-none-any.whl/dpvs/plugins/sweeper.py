from dpvs.logging import get_logger
from hydra_plugins.hydra_optuna_sweeper.optuna_sweeper import OptunaSweeper as Original
from typing import List

class OptunaSweeper(Original):
    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)