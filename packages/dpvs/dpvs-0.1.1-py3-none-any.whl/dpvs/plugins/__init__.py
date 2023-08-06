from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStoreWithProvider
from .typing import List, Any, SamplerConfig, MISSING, Direction, Optional, Dict


@dataclass
class OptunaSweeperConf:
    _target_: str = "dpvs.plugins.OptunaSweeper"
    defaults: List[Any] = field(default_factory=lambda: [{'sampler': 'tpe'}])
    # Sampling algorithm
    sampler: SamplerConfig = MISSING
    # Direction of optimization
    direction: Any = Direction.minimize
    # Storage URL to persist optimization results, e.g., `sqlite:///example.db`
    storage: Optional[Any] = None
    # Name of study to persist optimization results
    study_name: Optional[str] = None
    # Total number of function evaluations
    n_trials: int = 20
    # Number of parallel workers
    n_jobs: int = 2
    # Maximum authorized failure rate for a batch of parameters
    max_failure_rate: float = 0.0
    # Search space
    search_space: Optional[Dict[str, Any]] = None
    # Parameter
    params: Optional[Dict[str, str]] = None
    # https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html
    custom_search_space: Optional[str] = None


def register():
    with ConfigStoreWithProvider('optuna_sweeper') as cs:
        cs.store( 
            group="hydra/sweeper", name="optuna", node=OptunaSweeperConf
        )