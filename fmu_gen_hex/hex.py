"""
Created on Thu Apr 11 13:48:48 2024

@author: emrkay
"""
#%matplotlib qt
# % clear all
# % close all
# %
# % This was done within the Business Finland funded research project INTENS
# % by M. Manng?rd and J. Hammarstr?m.

# clc
# global cpc mc nCells cph mh Thin Tcin Tcout Thout
import scipy
from matplotlib import pyplot as plt
#from .utils.HE_functs import HESS,HEMinCells

#global cpc, mc, nCells, cph, mh, Thin, Tcin, Tcout, Thout

import numpy as np
from numpy.linalg import pinv, norm

# Define the objective function
def objfun(x,cpc, mc,nCells,  cph, mh, Thin, Tcin, Tcout, Thout):
    #global cpc, mc, nCells, cph, mh, Thin, Tcin, Tcout, Thout
    
    AA = np.block([[np.diag((cpc * mc + x) * np.ones(nCells)),
                    np.zeros((nCells, nCells))],
                   [np.zeros((nCells, nCells)),
                    np.diag((cph * mh + x) * np.ones(nCells))]])
    
    AA += np.block([[np.zeros((1, 2 * nCells))],
                    [np.diag(-cpc * mc * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, nCells + 1))],
                    [np.zeros((1, 2 * nCells))],
                    [np.zeros((nCells - 1, nCells)),
                     np.diag(-cph * mh * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, 1))]]) - x * np.flip(np.eye(2 * nCells),1)
    
    bb = np.zeros((2 * nCells, 1))
    bb[0] = cpc * mc * Tcin
    bb[nCells] = cph * mh * Thin
    
    CC = np.zeros((2, 2 * nCells))
    CC[0, nCells-1] = 1
    CC[1, 2 * nCells - 1] = 1
    
    f = norm(np.block([[Tcout], [Thout]]) - np.matmul(np.matmul(CC,pinv(AA)) ,bb),2)**2
    return f

# Define the objective function
def objfun3(x, cpc ,nCells,  cph, Tcout, Thout, K=-1, Thin=-1, Tcin=-1, mc=-1,  mh=-1):
    ix = 0
    if K==-1:
        K = x[ix]
        ix=ix+1
    if Thin==-1:
        Thin = x[ix]
        ix=ix+1
    if Tcin==-1:
        Tcin = x[ix]
        ix=ix+1
    if mc==-1:
        mc = x[ix]
        ix=ix+1       
    if mh==-1:
        mh = x[ix]
        ix=ix+1        
    AA = np.block([[np.diag((cpc * mc + K) * np.ones(nCells)),
                    np.zeros((nCells, nCells))],
                   [np.zeros((nCells, nCells)),
                    np.diag((cph * mh + K) * np.ones(nCells))]])
    
    AA += np.block([[np.zeros((1, 2 * nCells))],
                    [np.diag(-cpc * mc * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, nCells + 1))],
                    [np.zeros((1, 2 * nCells))],
                    [np.zeros((nCells - 1, nCells)),
                     np.diag(-cph * mh * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, 1))]]) - K * np.flip(np.eye(2 * nCells),1)
    
    bb = np.zeros((2 * nCells, 1))
    bb[0] = cpc * mc * Tcin
    bb[nCells] = cph * mh * Thin
    
    CC = np.zeros((2, 2 * nCells))
    CC[0, nCells-1] = 1
    CC[1, 2 * nCells - 1] = 1
    
    f = norm(np.block([[Tcout], [Thout]]) - np.matmul(np.matmul(CC,pinv(AA)) ,bb),2)**2
    return f

# Define the objective function
def objfun4(K, cpc ,nCells,  cph, Tcout, Thout, Thin, Tcin, mc,  mh):
    
    AA = np.block([[np.diag((cpc * mc + K) * np.ones(nCells)),
                    np.zeros((nCells, nCells))],
                   [np.zeros((nCells, nCells)),
                    np.diag((cph * mh + K) * np.ones(nCells))]])
    
    AA += np.block([[np.zeros((1, 2 * nCells))],
                    [np.diag(-cpc * mc * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, nCells + 1))],
                    [np.zeros((1, 2 * nCells))],
                    [np.zeros((nCells - 1, nCells)),
                     np.diag(-cph * mh * np.ones(nCells - 1)),
                     np.zeros((nCells - 1, 1))]]) - K * np.flip(np.eye(2 * nCells),1)
    
    bb = np.zeros((2 * nCells, 1))
    bb[0] = cpc * mc * Tcin
    bb[nCells] = cph * mh * Thin
    
    CC = np.zeros((2, 2 * nCells))
    CC[0, nCells-1] = 1
    CC[1, 2 * nCells - 1] = 1
    
    f = norm(np.block([[Tcout], [Thout]]) - np.matmul(np.matmul(CC,pinv(AA)) ,bb),2)**2
    return f




def HESS(K, cpc, cph, Tcin, Thin, mc, mh, n):
    A = np.block([[np.diag((cpc * mc + K) * np.ones(n)),
                   np.zeros((n, n))],
                  [np.zeros((n, n)),
                   np.diag((cph * mh + K) * np.ones(n))]])
    
    A += np.block([[np.zeros((1, 2 * n))],
                   [np.diag(-cpc * mc * np.ones(n - 1)),
                    np.zeros((n - 1, n + 1))],
                   [np.zeros((1, 2 * n))],
                   [np.zeros((n - 1, n)),
                    np.diag(-cph * mh * np.ones(n - 1)),
                    np.zeros((n - 1, 1))]]) - K * np.flip(np.eye(2 * n),1)
    
    b = np.zeros((2 * n, 1))
    b[0] = cpc * mc * Tcin
    b[n] = cph * mh * Thin
    
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    
    TC = np.concatenate((np.array([[Tcin]]), x[:n]), axis=0)
    TH = np.concatenate((np.array([[Thin]]), x[n:]), axis=0)
    
    return TC, TH

from scipy.interpolate import interp1d
def HEMinCells(TC,TH,fig,ax):
    
    assert type(TC)==np.ndarray
    assert type(TH)==np.ndarray
    if len(TC.shape)>1:
        if TC.shape[1]>TC.shape[0]:
            TC = np.transpose(TC)
        TC = TC[:,0]
    if len(TH.shape)>1:
        if TH.shape[1]>TH.shape[0]:
            TH = np.transpose(TH)
        TH = TH[:,0]
# %HEMinCells Computes the minimum cells needed when discretizing a HE model
# %to acieve steady-state performance. Inpute TC and TH are the temperature
# %profiles for the HE on the cold and hot sides repsecively.
# %
# %See Varbanov, Klemes and Friedler (2011). Cell-based dynamic heat exchanger models?Direct
# %determination of the cell number and size. Computers & Chemical Engineering,
# %35(5), 943-948.
# %
# % This was done within the Business Finland funded research project INTENS
# % by M. Manngard and J. Hammarstrom.
    x = np.zeros(500)
    y = np.zeros(500)
    #TC = TC(end:-1:1)
    TC = TC[::-1]
    
    if len(TC)!=len(TH):
        #% error checking
        print('TC and TH should be the same length!')
    else:
        xline = np.linspace(0,1,len(TC))#; %xaxis
        ax.plot(xline,TC,'b-')
        ax.plot(xline,TH,'r-')
        k=0
        x[0]=1
        y[0]=TH[-1]
        xinterp = interp1d(TC,xline)
        yinterp = interp1d(xline,TH)
        while (y[k]<= TC[0]) and (y[k] <= TH[0]):
            k=k+1
            #%interpolate to find x-y coordinates
            x[k] = xinterp(y[k-1])#[0]
            y[k] = yinterp(x[k])#[0]
            #y[k] = np.interp(xline,TH,x[k])
       #end

        minCells = k+1; #; %minimum number of cells needed
        
        #%% plot results
        k=k+1 
        x[k]=0
        y[k]=y[k-1]
        x = x[0:(k+1)]
        y = y[0:(k+1)]
        #figure, hold on


        #ax.stairs([1,x],[TC[-1], y])
        plt.step(np.concatenate([np.array([1,]),x]), np.concatenate([np.array([TC[-1],]), y]), 'ko-',where='post')
        #plt.step(x, y, 'ko-')
        plt.xlabel('Normalized length')
        plt.ylabel('Temperature')
        ax.legend('Cold side','Hot side')
        #plt.grid()

    return minCells#,x,y


if __name__ == '__main__':
    #rtyhrtfyhrf
    # %% parameters
    nCells = 8;
    
    Area = 120;
    h = 8127.8;
    K0 = Area*h/nCells;
    
    mc = 46.22;
    mh = 56.27;
    
    Tcin = 68;
    Thin = 91;
    
    Tcout = 88.6;# %desired
    Thout = 74.1;# %desired
    
    cpc = 4190;
    cph = 4190;
    
    #% find K
    #[K,fval] = fminunc(@objfun,K0)
    result = scipy.optimize.minimize(objfun, K0,args=(cpc, mc, nCells, cph, mh, Thin, Tcin, Tcout, Thout), method='L-BFGS-B')
    K = result.x
    #% Solve system of equations
    
    [TC,TH] = HESS(K,cpc,cph,Tcin,Thin,mc,mh,nCells);
     
    #% Plot results
    fig,ax = plt.subplots()
    
    plt.plot(np.linspace(0,1,nCells+1),TC[::-1],'bo-')
    plt.plot(np.linspace(0,1,nCells+1),TH,'ro-')
    plt.grid()
    
    plt.title('Number of cells: '+str(nCells))
    #% 
    plt.legend(['Cold side','Hot side','Desired outlet temperature (cold side)','Desired outlet temperature (hot side)'])
    
    #drgdrgdrgd
    
    #%%
    nCells = 100;
    K=Area*h/nCells;
    
    [TC,TH] = HESS(K,cpc,cph,Tcin+10,Thin,mc,mh,nCells)
    
    #figure(2), hold on,
    fig,ax = plt.subplots()
    plt.plot(np.linspace(0,1,nCells+1),TC[::-1],'b-')
    plt.plot(np.linspace(0,1,nCells+1),TH,'r-')
    plt.grid()
    #% plot(0,Tcout,'bx','linewidth',2,'markersize',14)
    #% plot(1,Thout,'rx','linewidth',2,'markersize',14)
    plt.title('Number of cells: '+str(nCells))
    
    plt.legend(['Cold side','Hot side','Desired outlet temperature (cold side)','Desired outlet temperature (hot side)'])
    plt.xlabel('Cell number')
    plt.ylabel('Temperature (degC)')
    
    #fsadfadd
    #%% Graphical method to determine minimum number of cells
    MinCells = HEMinCells(TC,TH)
    print('MinCells:'+str(MinCells))
    MinCells = HEMinCells(np.array([[Tcin,Tcout]]),np.array([[Thin,Thout]]))
    print('MinCells:'+str(MinCells))
