"""
Created on Tue Apr 23 18:27:44 2024

@author: emrkay
"""
import pyfmi

import numpy as np

def simulate_model(fmu_filepath,config_dict):
    flow_type  =config_dict["flow_type"]
    param_keys = ['K', 'cp1', 'cp2', 'm1', 'm2']

    fmus=[]
    for ifmu in range(config_dict['nCells']):
        fmus.append(pyfmi.load_fmu(fmu_filepath))


    for fmu in fmus:      
        fmu.set('T1_ini',config_dict['T1_in'])
        fmu.set('T2_ini',config_dict['T2_in'])
        
        fmu.set('T1_in',config_dict['T1_in'])
        fmu.set('T2_in',config_dict['T2_in'])    
        
        fmu.set('m1_in',config_dict['mdot1_in'])
        fmu.set('m2_in',config_dict['mdot2_in'])
    
    for fmu in fmus:
        for paramkey in param_keys:            
            fmu.set(paramkey,config_dict[paramkey])    

    connections = []    
    
    for ifmu in range(config_dict['nCells']-1):
        connections.append((fmus[ifmu],'T1_out',fmus[ifmu+1],'T1_in'))
        connections.append((fmus[ifmu],'m1_out',fmus[ifmu+1],'m1_in'))
        
        if flow_type=="Counter flow":
            connections.append((fmus[ifmu+1],'T2_out',fmus[ifmu],'T2_in'))
            connections.append((fmus[ifmu+1],'m2_out',fmus[ifmu],'m2_in'))
        else:
            connections.append((fmus[ifmu],'T2_out',fmus[ifmu+1],'T2_in'))
            connections.append((fmus[ifmu],'m2_out',fmus[ifmu+1],'m2_in'))        

    coupled_simulation = pyfmi.master.Master(fmus,connections)
    
    opts = coupled_simulation.simulate_options()
    start_time = 0
    step_size = config_dict['step_size'] 
    opts["step_size"] = step_size
    stop_time = config_dict['stop_time']
    times = np.arange(start_time,stop_time+step_size,step_size)
    print(opts)
    
    n_steps = len(times)
    # Create the input matrix
    u = np.transpose(np.vstack((times ,config_dict['T1_in']*np.ones(n_steps) ,config_dict['T2_in']*np.ones(n_steps),config_dict['mdot1_in']*np.ones(n_steps) ,config_dict['mdot2_in']*np.ones(n_steps))))
    # Simulate the model response , given the initial parameters
    if flow_type=="Counter flow":
        T2outid = 0
        T2inid = -1
    else:
        T2outid = -1
        T2inid = 0
    
    input_labels = [(fmus[0],'T1_in'),(fmus[T2inid],'T2_in'),(fmus[0],'m1_in'),(fmus[T2inid],'m2_in')]
    input_object = (input_labels,u)
    
    
    res = coupled_simulation.simulate(options=opts,input=input_object,start_time=start_time,final_time=stop_time)

    results = np.zeros((n_steps,3))
    #for ifmu in range(config_dict['nCells']):
    results[:,0] = res[fmus[-1]]['T1_out']
    

        
    results[:,1] = res[fmus[T2outid]]['T2_out']
    
    results[:,2] = times
        

    
    return results