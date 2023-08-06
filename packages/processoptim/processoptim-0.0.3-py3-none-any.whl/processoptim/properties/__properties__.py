# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:28:38 2022

@author: HEDI
"""
import inspect
from ..obj.__obj__ import unzip_args
class tomato_sauce:
    def rho(self,x):
        """

        Parameters
        ----------
        x : TYPE
            mass fraction of dry matter [0-1]

        Returns
        -------
        TYPE
            density [kg/m3]

        """
        return 1/(x/1600+(1-x)/1000)
    def Cp(self,x):
        """

        Parameters
        ----------
        x : TYPE
            mass fraction of dry matter [0-1]

        Returns
        -------
        TYPE
            specific heat [kJ/kg/K]

        """
        return x*.5 + 4.18*(1-x)
    
        