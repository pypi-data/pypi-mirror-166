# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:34:21 2022

@author: HEDI
"""

from ..properties.__properties__ import water, tomato_sauce
from ..opu.__evapo__ import evapo
import matplotlib.pyplot as plt
from numpy import linspace,array

def plot(disp_rho=0,disp_mu=0,disp_lambda=0,disp_Cp=0):
    st =tomato_sauce()
    w = water()
    
    
    x = linspace(.06,.32,100)
    rho = []
    mu30=[]
    mu60=[]
    mu90=[]
    l30=[]
    l60=[]
    l90=[]
    Cp=[]
    for x1 in x:
        rho.append(st.rho(x1))
        mu30.append(st.mu(x1, 30, 5, 2.5e-2)*1000)
        mu60.append(st.mu(x1, 60, 5, 2.5e-2)*1000)
        mu90.append(st.mu(x1, 90, 5, 2.5e-2)*1000)
        l30.append(st.Lambda(x1, 30))
        l60.append(st.Lambda(x1, 60))
        l90.append(st.Lambda(x1, 90))
        Cp.append(st.Cp(x1))
    if disp_rho:
        plt.figure()
        plt.plot(x,rho,label="tomato sauce")
        plt.plot([0],[w.rho(20)],'s',markerfacecolor='white',markersize=6,markeredgecolor='blue',label='water')
        plt.xlabel("Mass fraction of dry matter [-]")
        plt.ylabel("Density [kg/m3]")
        plt.legend()
        plt.grid()
    if disp_mu:
        plt.figure()
        plt.plot(x,mu30,label="tomato sauce 30°C")
        plt.plot(x,mu60,label="tomato sauce 60°C")
        plt.plot(x,mu90,label="tomato sauce 90°C")
        plt.plot([0],[w.mu(30)*1000],'s',markerfacecolor='white',markersize=6,markeredgecolor='blue',label='water 30°C')
        plt.plot([0],[w.mu(60)*1000],'s',markerfacecolor='white',markersize=6,markeredgecolor='tomato',label='water 60°C')
        plt.plot([0],[w.mu(90)*1000],'s',markerfacecolor='white',markersize=6,markeredgecolor='red',label='water 90°C')
        plt.plot([.25,.1336,.0911,.0692,.057],array([.022,.013,.013,.011,.01])*1000,"*",label="littérature 25°C")
        plt.xlabel("Mass fraction of dry matter [-]")
        plt.ylabel("mu [mPa.s]")
        plt.legend()
        plt.grid()
    if disp_lambda:
        plt.figure()
        plt.plot(x,l30,label="tomato sauce 30°C")
        plt.plot(x,l60,label="tomato sauce 60°C")
        plt.plot(x,l90,label="tomato sauce 90°C")
        plt.plot([0],[w.Lambda(30)],'s',markerfacecolor='white',markersize=6,markeredgecolor='blue',label='water 30°C')
        plt.plot([0],[w.Lambda(60)],'s',markerfacecolor='white',markersize=6,markeredgecolor='tomato',label='water 60°C')
        plt.plot([0],[w.Lambda(90)],'s',markerfacecolor='white',markersize=6,markeredgecolor='red',label='water 90°C')
        plt.xlabel("Mass fraction of dry matter [-]")
        plt.ylabel("thermal conductivity [W/m/K]")
        plt.legend()
        plt.grid()
    if disp_Cp:
        plt.figure()
        plt.plot(x,Cp,label="tomato sauce")
        plt.plot([0],[w.Cp(20)],'s',markerfacecolor='white',markersize=6,markeredgecolor='blue',label='water')
        plt.xlabel("Mass fraction of dry matter [-]")
        plt.ylabel("specific heat [kJ/kg/K]")
        plt.legend()
        plt.grid()

# def test_evapo():
#     ev = evapo(n=3,x0=.06,xt=.32,L0=5)
#     print("L",ev.L)