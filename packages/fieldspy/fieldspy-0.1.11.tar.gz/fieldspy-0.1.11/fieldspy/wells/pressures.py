from typing import Dict, List, Union
import pandas as pd
import geopandas as gpd
from datetime import date
import numpy as np
from pydantic import Field, validate_arguments,parse_obj_as
from .depthmodel import DepthModel

from enum import Enum

class PressureType(str,Enum):
    dynamic = 'dynamic'
    static = 'static'

class Pressure(DepthModel):
    date: date
    pressure: float
    type: PressureType = Field(PressureType.dynamic)

    
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def estimate_pressure_at_depth(
        self,
        depth:Union[float,List[float],np.ndarray],
        gradient:float=0.433,
        depth_ref:str = 'tvd'
    ):
        
        fact = 1 if depth_ref=='tvd' else -1
        
        depth_arr = np.atleast_1d(depth)
        depth_pres = getattr(self,f'{depth_ref}_top')
        height_diff = fact*(depth_arr - depth_pres)
        
        return self.pressure + height_diff*gradient
        
        
class Pressures(DepthModel):
    pressures: Dict[str,Pressure] = Field(None)

    class Config:
        validate_assignment = True

    def __repr__(self) -> str:
        return (f'pressures:\n'
            f'Number of items: {len(self.pressures)}')

    def __str__(self) -> str:
        return (f'pressures:\n'
            f'Number of items: {len(self.pressures)}')
    
    def __len__(self):
        return len(self.pressures)
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.pressures[key]
        elif isinstance(key, (int,slice)):
            return list(self.pressures.values())[key]
        else:
            raise KeyError(key)
    
    def __iter__(self):
        return (self.pressures[f] for f in self.pressures)

    @validate_arguments
    def df(self, pressures:Union[str,List[str]]=None):
        gdf_list = []
        for f in self.pressures:
            gdf_list.append(self.pressures[f].df())
        
        gdf = gpd.GeoDataFrame(pd.concat(gdf_list, axis=0))
        gdf.crs = gdf_list[0].crs
        gdf.index.name='pressure'
        if pressures:
            if isinstance(pressures,str):
                pressures = [pressures]
            gdf = gdf.loc[pressures]
        return gdf
    
    @classmethod
    def from_df(
        cls,
        df:pd.DataFrame,
        name:str=None,
        fields:List[str] = None,
        fmt:str=None,
        **kwargs
    ):
        df = df.copy()
        if name:
            df['name'] = df[name].copy()
            df.index = df['name']
        else:
            df['name'] = df.index
            
        #To change columns name to match Object
        if bool(kwargs):
            kwargs = {v: k for k, v in kwargs.items()}
            df = df.rename(columns=kwargs)
            
        df['date'] = pd.to_datetime(df['date'], format=fmt)
        
        if fields is not None:
            fields_dict = df[fields].to_dict(orient='index')
            df.drop(fields,axis=1,inplace=True)
            
            pr_dict = df.to_dict(orient='index')
            
            for fm in pr_dict:
                pr_dict[fm].update({'fields':fields_dict[fm]})
        else:
            pr_dict = df.to_dict(orient='index')
            
        
        
        return cls(
            pressures=parse_obj_as(
                Dict[str,Pressure],
                pr_dict
            )
        )
        
    @validate_arguments
    def add_pressures(self, pressures: Union[List[Pressure],Dict[str,Pressure],Pressure]):
        form_dict = {}
        if isinstance(pressures,Pressure):
            form_dict.update({pressures.name:pressures})
        elif isinstance(pressures,list):
            form_dict.update({p.name:p for p in pressures})
        elif isinstance(pressures,dict):
            form_dict = pressures
        
        if self.pressures:
            self.pressures.update(form_dict)
        else:
            #print(form_dict)
            self.pressures = form_dict

        return None
