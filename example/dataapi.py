import os
import pandas as pd
from pathlib import Path
from quantframe.dataapi import ApiBase


class Api(ApiBase):

    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self.data = {}
    
    @property
    def dates(self) -> pd.DatetimeIndex:
        return pd.read_parquet(self.directory.joinpath('dates').absolute())

    @property
    def fields(self) -> pd.Index:
        return pd.Index(os.listdir(self.directory))
    
    @property
    def codes(self) -> pd.Index:
        return pd.Index(pd.read_parquet(self.directory.joinpath('codes').absolute()))
    
    def loc_field(self, field: 'str | list') -> pd.Index:
        return super().loc_field(field)
    
    def loc_date(self, date: 'str | list') -> pd.DatetimeIndex:
        return super().loc_date(date)
    
    def loc_codes(self, code: 'str | list') -> pd.Index:
        return super().loc_codes(code)
    
    def query(self, code: str, field: str, start: 'str | list' = None, end: str = None):
        super().query(code, field, start, end)
        curdata = []
        for f in self.field:
            if f not in self.fields:
                raise ValueError(f"Field {f} not found")
            if self.data.get(f) is None:
                self.data[f] = pd.read_parquet(f'{self.directory}/{f}')
            if self.code is None:
                self.code = slice(None)
            if isinstance(self.start, pd.DatetimeIndex):
                curdata.append(self.data[f].loc[self.start, self.code].stack())
            else:
                curdata.append(self.data[f].loc[self.start:self.end, self.code].stack())
        
        curdata = pd.concat(curdata, axis=1)
        curdata.columns = self.field
        return curdata
