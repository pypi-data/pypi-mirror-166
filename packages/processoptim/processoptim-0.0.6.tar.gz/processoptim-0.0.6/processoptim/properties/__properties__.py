# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:28:38 2022

@author: HEDI
"""
import inspect
from numpy import exp,array
from ..obj.__obj__ import unzip_args
import CoolProp.CoolProp as CP
__R__ = 8.314 #J/mol/K

class water:
    def rho(self,T):
        return CP.PropsSI('D','T',T+273,'Q',0,"water")
    def Cp(self,T):
        return CP.PropsSI("C",'T',T+273,'Q',0,"water")/1000
    def H(self,T):
        return CP.PropsSI("H",'T',T+273,'Q',0,"water")/1000
    def Lv_p(self,p):
        return (CP.PropsSI("H",'P',p*1e5,'Q',1,"water")-CP.PropsSI("H",'P',p*1e5,'Q',0,"water"))/1000
    def Lv_T(self,T):
        return (CP.PropsSI("H",'P',T+273.15,'Q',1,"water")-CP.PropsSI("H",'T',T+273.15,'Q',0,"water"))/1000
    def mu(self,T):
        return CP.PropsSI("V",'T',T+273,'Q',0,"water")
    def Lambda(self,T):
        return CP.PropsSI("L",'T',T+273,'Q',0,"water")
    
class tomato_sauce:
    def __check_array__(self,v):
        if isinstance(v, list):
            v=array(v)
        return v
    def rho(self,x):
        """
        Parameters
        ----------
        x : double or [double]
            mass fraction of dry matter [0-1]
        Returns
        -------
        TYPE
            density [kg/m3]
        """
        x=self.__check_array__(x)
        return 1/(x/1600+(1-x)/1000)
    def Cp(self,x):
        """
        Parameters
        ----------
        x : double or [double]
            mass fraction of dry matter [0-1]
        Returns
        -------
        TYPE
            specific heat [kJ/kg/K]
        """
        x=self.__check_array__(x)
        return x*.5 + 4.18*(1-x)
    def Lambda(self, x, T):
        """
        Parameters
        ----------
        x : double
            mass fraction of dry matter [0-1]
        T : double
            temperature [degC]
        Returns
        -------
        type of x or T
            thermal conductivity [W/m/K]
        """
        T+=273.15
        Es = 5*1000 # kJ/mol
        Ew = .17*1000 # kJ/mol
        Tr = 60+273.15 # K
        x=self.__check_array__(x)
        T=self.__check_array__(T)
        return x*.22*exp(-Es/__R__*(1/T-1/Tr))+(1-x)*.68*exp(-Ew/__R__*(1/T-1/Tr))
    def mu(self,x,T,u,d):
        """
        Parameters
        ----------
        x : TYPE
            mass fraction of dry matter [0-1]
        T : TYPE
            temperature [degC]
        u : TYPE
            velocity [m/s]
        d : TYPE
            characteristic length [m]
        Returns
        -------
        Apparent viscosity [Pa.s]
        """
        T+=273.15
        k0 = 1.27
        B=.15
        E=15.8*1000
        n0=.403
        b=.0028
        T0=25+273
        k = k0*exp(B*x)*exp(E/__R__*(1/T-1/T0))
        n = n0-b*x
        #k=1.84*pow(x*100,2.54)/(100-x*100)
        return k*pow(8*u/d,n-1)
    def H(self,x,T):
        """
        Parameters
        ----------
        x : TYPE
            mass fraction of dry matter [0-1]
        T : TYPE
           temperature [degC]
        Returns
        -------
        enthalpy [kJ/kg]
        """
        return self.Cp(x)*T
    
        