import abc
import pandas as pd
from .dataapi import parse_commastr, parse_date


class TickerBase(abc.ABC):

    def __init__(self, code: str) -> None:
        """Ticker Base Class"""
        self.data = pd.DataFrame()
        self.code = code
        self.universe_type = UniverseBase
    
    def __add__(self, other: 'UniverseBase | TickerBase') -> 'UniverseBase':
        if isinstance(other, UniverseBase):
            return other + self
        elif isinstance(other, TickerBase):
            return self.universe_type(self, other)
    
    def __str__(self):
        return f'Ticker: {self.code}'
    
    def __repr__(self) -> str:
        return self.__str__()
            
    @abc.abstractmethod
    def load(
        self,
        start: 'str | list' = None,
        end: str = None,
        field: 'str | list' = None
    ) -> pd.DataFrame:
        self.start, self.end = parse_date(start, end)
        self.field = parse_commastr(field)
    

class UniverseBase(abc.ABC):

    def __init__(self, *tickers: 'list') -> None:
        """Universe Base Class"""
        self.tickers = []
        for ticker in tickers:
            self.tickers.append(ticker)
        self.data = [pd.DataFrame() for _ in range(len(tickers))]
    
    def __add__(self, other: 'TickerBase | UniverseBase') -> 'UniverseBase':
        if isinstance(other, TickerBase):
            self.tickers.append(other)
            return self
        if isinstance(other, UniverseBase):
            self.tickers += other.tickers
            return self
    
    def __str__(self):
        if len(self.tickers) >= 5:
            return f'Universe: {self.tickers[:5]}'
        return f'Universe: {self.tickers}'

    def __repr__(self) -> str:
        return self.__str__()
    
    @abc.abstractmethod
    def load(
        self,
        start: 'str | list' = None,
        end: str = None,
        field: 'str | list' = None,
    ) -> list[pd.DataFrame]:
        self.start, self.end = parse_date(start, end)
        self.field = parse_commastr(field)
        self.codes = [ticker.code for ticker in self.tickers]
     

class PairBase(abc.ABC):

    def __init__(self, tickerx: TickerBase, tickery: TickerBase):
        """"""
        self.tickerx = tickerx
        self.tickery = tickery
        self.data = (pd.DataFrame(), pd.DataFrame())
        self.universe_type = PairUniverseBase
    
    @abc.abstractmethod
    def load(
        self, 
        start: 'str | list' = None, 
        end: str = None,
        field: 'str | list' = None,
    ) -> tuple[pd.DataFrame]:
        self.start, self.end = parse_date(start, end)
        self.field = parse_commastr(field)
    
    def __str__(self):
        return f'Pair [{self.tickerx} - {self.tickery}]'

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other: 'PairBase | PairUniverseBase'):
        if isinstance(other, PairBase):
            return self.universe_type(self, other)
        if isinstance(other, PairUniverseBase):
            return other + self


class PairUniverseBase(abc.ABC):

    def __init__(self, *pairs: list[PairBase]) -> None:
        """Pair Universe Base Class"""
        self.pairs = []
        for pair in pairs:
            self.pairs.append(pair)
        self.data = [pd.DataFrame() for _ in range(len(pairs))]
    
    @abc.abstractmethod
    def load(self, start: 'str | list' = None, end: str = None, field: 'str | list' = None):
        self.start, self.end = parse_date(start, end)
        self.field = parse_commastr(field)

    def __add__(self, other: 'PairBase | PairUniverseBase'):
        if isinstance(other, PairBase):
            self.pairs.append(other)
        elif isinstance(other, PairUniverseBase):
            self.pairs += other.pairs
        return self
    