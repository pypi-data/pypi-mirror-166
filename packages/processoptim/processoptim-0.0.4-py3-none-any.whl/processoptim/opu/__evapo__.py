# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 11:59:20 2022

@author: HEDI
"""
import CoolProp.CoolProp as CP
from numpy import zeros, array, ones, pi
from prettytable import PrettyTable


def Lv_T(T):
    return (CP.PropsSI("H", 'T', T+273.15, 'Q', 1, "water")-CP.PropsSI("H", 'T', T+273.15, 'Q', 0, "water"))/1000


class evapo:
    def __init__(self, **args):
        if "n" in args.keys():
            self.n = args["n"]
            args.pop("n")
        else:
            self.n = 1
        for k in ["x", "L", "T", "V", "rho_p", "p"]:
            setattr(self, k, zeros(self.n+1))
        for k, v in args.items():
            if k == "x0":
                self.x[0] = v
            elif k == "L0":
                self.L[0] = v
            elif k == "xt":
                self.x[-1] = v
            elif k in ["h", "S", "N", "u"]:
                if isinstance(v, list) and len(v) == self.n:
                    setattr(self, k, array(v))
                else:
                    setattr(self, k, ones(self.n)*v)
            elif k == "Ts":  # steam temperature
                self.T[0] = v
            else:
                setattr(self, k, v)
        self.ms = self.L[0]*self.x[0]  # dry matter flowrate
        if self.x[-1] != 0:
            self.L[-1] = self.ms/self.x[-1]
        self.mevap = self.L[0]-self.L[-1]
        self.V[0:] = self.mevap/self.n
        for j in range(1, self.n):
            self.L[j] = self.L[j-1]-self.V[j]
            self.x[j] = self.ms/self.L[j]
        self.T[1] = self.T[0]-self.V[0]*Lv_T(self.T[0])/(self.S[0]*self.h[0])

        self.EEB = zeros(self.n)
        self.f = zeros(self.n)
        self.F = zeros(self.n)
        self.DP = zeros(self.n)
        self.E = zeros(self.n)

        def EEB(T, x):
            Lv = Lv_T(T)
            T += 273.15
            return 8.314*T*T*x/Lv/.018/1000

        self.EEB[0] = EEB(self.T[1], self.x[1])

        if self.n > 1:
            for i in range(2, self.n+1):
                self.T[i] = self.T[i-1]
                err_ = 1
                while err_ > 1e-6:
                    eeb = EEB(self.T[i], self.x[i])
                    T = self.T[i-1]-self.V[i] * \
                        Lv_T(self.T[i]-eeb)/self.h[i-1]/self.S[i-1]
                    err_ = abs(T-self.T[i])
                    self.T[i] = T
                    self.EEB[i-1] = eeb
        for i, v in enumerate(self.T):
            self.p[i] = CP.PropsSI('P', 'T', v+273, 'Q', 1, "water")/1e5
        if hasattr(self, "liq"):
            for i, v in enumerate(self.x):
                self.rho_p[i] = self.liq.rho(v)

            for i in range(0, self.n):
                self.f[i] = .08*pow(self.rho_p[i]*self.d*self.u[i]/4, -.25)
                self.F[i] = self.u[i]*self.N[i]*pi*self.d*self.d/4
                self.DP[i] = 2*self.f[i] * \
                    (self.l/self.d)*self.rho_p[i]*self.u[i]**2
                self.E[i] = self.DP[i]*self.F[i]/1000
    def __repr__(self):
        def f(v,d):
            return ("{:."+str(d)+"f}").format(v)
        vap = PrettyTable()
        vap.field_names = ["", "bar", "°C", "kg/s"]
        for i in range(0,self.n+1):
            vap.add_row(["V"+str(i) ,f(self.p[i],2),f(self.T[i],0),f(self.V[i],2)])
        
        liq=PrettyTable()
        liq.field_names = ["", "MS%", "°C", "kg/s","kg/m3"]
        for i in range(0,self.n+1):
            liq.add_row(["L"+str(i) ,f(self.x[i]*100,2),f(self.T[i],0),f(self.L[i],2),f(self.rho_p[i],1)])
        
        eff = PrettyTable()
        eff.field_names = ["","EBP °C","DP bar", "Pump kW"]
        for i in range(0,self.n):
            eff.add_row(["Effet "+str(i+1) ,f(self.EEB[i],0),f(self.DP[i]/1e5,2),f(self.E[i],2)])
        return vap.get_string()+"\n"+liq.get_string()+"\n"+eff.get_string()
