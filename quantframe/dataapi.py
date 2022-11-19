import abc
import datetime
import pandas as pd


def parse_date(
    start: 'str | list' = None,
    end: str = None,
) -> tuple:
    if not isinstance(start, list):
        start = pd.to_datetime(start) if start is not None else pd.to_datetime('2010-01-04')
        end = pd.to_datetime(end) if end is not None else pd.to_datetime(datetime.datetime.today())
        return (start, end)
            
    else:
        if end is not None:
            print(f"[!] start is a list, end will be ignored")
        return (pd.to_datetime(start), None)

def parse_commastr(
    commastr: 'str | list',
) -> pd.Index:
    if isinstance(commastr, str):
        commastr = commastr.split(',')
        return list(map(lambda x: x.strip(), commastr))
    elif isinstance(commastr, list):
        return commastr
    elif commastr is None:
        return None


class ApiBase(abc.ABC):
    
    @abc.abstractproperty
    def dates(self) -> pd.DatetimeIndex:
        pass
    
    @abc.abstractproperty
    def fields(self) -> pd.Index:
        pass
    
    @abc.abstractproperty
    def codes(self) -> pd.Index:
        pass
    
    @abc.abstractmethod
    def loc_date(self, date: 'str | list') -> pd.DatetimeIndex:
        pass
    
    @abc.abstractmethod
    def loc_field(self, field: 'str | list') -> pd.Index:
        pass
    
    @abc.abstractmethod
    def loc_codes(self, code: 'str | list') -> pd.Index:
        pass

    @abc.abstractmethod
    def query(
        self,
        code: str,
        field: str,
        start: 'str | list' = None,
        end: str = None,
    ):
        self.code = parse_commastr(code)
        self.field = parse_commastr(field)
        self.start, self.end = parse_date(start, end)
