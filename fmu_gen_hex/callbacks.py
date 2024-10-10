import numpy as np
import pandas as pd

#from utils.HEsteadystate import objfun4
#from utils.simulation_functs import simulate_model

from .hex import objfun4, HESS, HEMinCells
from .sim import simulate_model
from .fmu_compile import fmu_compile

import scipy
from shutil import copyfile, make_archive
import zipfile
import os

# --- data callbacks ---
data_callbacks = [
    "supplier", "ref", "itemNumber", "customerName", "riskFactor", "model", "date", "place", "flowType",
    "media1", "specificHeatCapacity1", "inletTemperature1", "outletTemperature1", "flowRate1", "liquidMass1", "liquidVolume1", "liquidDensity1",
    "media2", "specificHeatCapacity2", "inletTemperature2", "outletTemperature2", "flowRate2", "liquidMass2", "liquidVolume2", "liquidDensity2",
    "testPressure1", "designPressure1", "maxTemperature1", "minTemperature1",
    "testPressure2", "designPressure2", "maxTemperature2", "minTemperature2",
    "netWeight", "weightWithWater", "heatingSurface", "coolingCapacity", "heatTransferCoefficient", "nCells", "K"
]

def validate_and_convert_params(params, required_fields):
    """Validate and convert parameters based on the required fields."""
    converted_params = {}
    for field in required_fields:
        try:
            if 'flowRate' in field or 'specificHeatCapacity' in field or 'inletTemperature' in field or 'outletTemperature' in field or 'liquidMass' in field or field == 'K':
                converted_params[field] = float(params[field])
            elif field == 'nCells':
                converted_params[field] = int(params[field])
            else:
                converted_params[field] = params[field]
        except ValueError as e:
            raise ValueError(f"Error in input conversion for field '{field}': {e}")
    return converted_params

# --- callbacks ---
def simulate_callback(*args):
    '''Simulate button callback'''
    if len(args) != len(data_callbacks):
        raise ValueError(f"Expected {len(data_callbacks)} arguments, got {len(args)}")
    
    # Map the args to the variable names in data_callbacks
    params = dict(zip(data_callbacks, args))
    
    # Define the required fields for simulation
    required_fields = [
        'flowRate1', 'flowRate2', 'specificHeatCapacity1', 'specificHeatCapacity2',
        'inletTemperature1', 'inletTemperature2', 'liquidMass1', 'liquidMass2', 'K', 'nCells', 'flowType'
    ]
    
    # Validate and convert parameters
    converted_params = validate_and_convert_params(params, required_fields)
    
    fmu_filepath = os.path.abspath(os.path.join(__file__, os.pardir, "models", "hex_delta.fmu"))
    config_dict = {
        'step_size': 0.1,
        'stop_time': 120.0,
        'nCells': converted_params['nCells'],
        'T1_in': converted_params['inletTemperature1'],
        'T2_in': converted_params['inletTemperature2'],
        'mdot1_in': converted_params['flowRate1'],
        'mdot2_in': converted_params['flowRate2'],
        'K': converted_params['K'],
        'cp1': converted_params['specificHeatCapacity1'],
        'cp2': converted_params['specificHeatCapacity2'],
        'm1': converted_params['liquidMass1'],
        'm2': converted_params['liquidMass2'],
        'flow_type': converted_params['flowType']
    }
    results = simulate_model(fmu_filepath, config_dict)
    
    # Create pd dataframe
    N = len(results)
    time = results[:, 2]
    temp1 = results[:, 0]
    temp2 = results[:, 1]
    cat1 = np.repeat("T1_out", N)
    cat2 = np.repeat("T2_out", N)
    
    # Add categories
    time = np.concatenate((time, time))
    temp = np.concatenate((temp1, temp2))
    cat = np.concatenate((cat1, cat2))

    df = pd.DataFrame({"Time": time, "Temperature": temp, "Name": cat})
    return df

def optimize_callback(*args):
    '''Function optimizing K to fit outlet temperatures'''
    if len(args) != len(data_callbacks):
        raise ValueError(f"Expected {len(data_callbacks)} arguments, got {len(args)}")
    
    # Map the args to the variable names in data_callbacks
    params = dict(zip(data_callbacks, args))
    
    # Define the required fields for optimization
    required_fields = [
        'flowRate1', 'flowRate2', 'specificHeatCapacity1', 'specificHeatCapacity2',
        'inletTemperature1', 'inletTemperature2', 'outletTemperature1', 'outletTemperature2',
        'liquidMass1', 'liquidMass2', 'K', 'nCells'
    ]
    
    # Validate and convert parameters
    converted_params = validate_and_convert_params(params, required_fields)
    
    # Call the variable to be optimized
    cp1, cp2 = converted_params['specificHeatCapacity1'], converted_params['specificHeatCapacity2']
    T1out, T2out = converted_params['outletTemperature1'], converted_params['outletTemperature2']
    T1in, T2in = converted_params['inletTemperature1'], converted_params['inletTemperature2']
    m1, m2  = converted_params['flowRate1'], converted_params['flowRate2']
    
    # Group the arguments
    optKargs = (cp1, converted_params['nCells'], cp2, T1out, T2out, T2in, T1in ,m1, m2)
    result = scipy.optimize.minimize(objfun4, converted_params['K'], args=optKargs, method='Nelder-Mead')
    print(result)
    
    optimized_K = result.x[0]

    # Generate results for visualization
    TC, TH = HESS(optimized_K, cp1, cp2, T1in, T2in, m1, m2, converted_params['nCells'])
    
    # Make TC and TH to a one-dimensional arrays
    TC = TC.flatten()
    TH = TH.flatten()
    
    # Prepare the data for plotting
    cell_numbers = np.linspace(0, 1, converted_params['nCells'] + 1)
    cold_side_temps = TC[::-1]
    hot_side_temps = TH
    
    df = pd.DataFrame({
        "Time": np.concatenate((cell_numbers, cell_numbers)),
        "Temperature": np.concatenate((cold_side_temps, hot_side_temps)),
        "Name": np.concatenate((np.repeat("Cold Side", converted_params['nCells'] + 1), np.repeat("Hot Side", converted_params['nCells'] + 1)))
    })
    
    print(df)

    return df, str(optimized_K)

# -- export FMU callback --
def export_fmu_callback(K,ncells,flowtype,cp1,cp2,T1_in,T2_in,m1_in,m2_in,m1,m2, target_dir):
    '''Function for exporting an FMU model'''

    if flowtype == "Counter flow":
        counterflow = 1
    else:
        counterflow = 0
    
    hex_delta_base_path = os.path.abspath(os.path.join(__file__, os.pardir, "hex_delta55"))

    ori_cpp_path = os.path.abspath(os.path.join(hex_delta_base_path, "src", "hex_delta55_0.cpp"))
    out_cpp_path = os.path.abspath(os.path.join(hex_delta_base_path, "src", "hex_delta55.cpp"))

    #ori_cpp_path = current_dir + "\\utils\\hex_delta55\\src\\hex_delta55_0.cpp"
    #out_cpp_path = current_dir + "\\utils\\hex_delta55\\src\\hex_delta55.cpp"

    vars2vals = {'Counterflow':counterflow,'cp1':cp1,'cp2':cp2,'K':K,
                 'm1':m1,'m2':m2,'mdot1_in':m1_in,'mdot2_in':m2_in,'ncells':ncells,
                 'T1_in':T1_in,'T2_in':T2_in,'T1_ini':T1_in,'T2_ini':T2_in}
        
        
    fmu_path = fmu_compile(vars2vals,ori_cpp_path,out_cpp_path, hex_delta_base_path, target_dir)
    return fmu_path
