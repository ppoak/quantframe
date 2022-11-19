import abc
import pandas as pd
from .asset import PairBase, PairUniverseBase


class FactorBase(abc.ABC):
    """Indicator Base Class
    =========================
    
    The base class deals with the common indicator
    computation problems and meanwhile integrates some
    common oprations in indicator computing.

    Inheritage
    -----------

    subclasses must implement __call__ function, and compute each
    day result returning a DataFrame
    """

    def __init__(
        self, 
        pair_or_universe: 'PairBase | PairUniverseBase', 
        name: str = "base_indicator",
    ):
        """Indicator Base Class
        -----------------------

        pair_or_universe: Pair or Universe, assign pair or a group of pairs
        on_date: str, on which date the indicator is computed
        start_date: str, the start point of indicator
        end_date: str, the end point of indicator
        lookback_window: int, the length of window the indicator is computed
        """
        self.pair_or_universe = pair_or_universe
        self.name = name
        
    def __str__(self):
        return f'{self.name} on {self.pair_or_universe} from {self.start_date} to {self.end_date}'
    
    @abc.abstractmethod
    def __call__(
        self, 
        start: 'str | list', 
        end: str, 
        field: 'str | list', 
        *args, 
        **kwargs
    ) -> pd.DataFrame:
        raise NotImplementedError
