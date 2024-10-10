# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:56:48 2024

@author: emrkay
"""
import subprocess
import os

from shutil import copyfile,make_archive
from .xml_functs import change_values_in_modelDescription

#try:
#    from utils.xml_functs import change_values_in_modelDescription
#except:
#    from xml_functs import change_values_in_modelDescription


def edit_fmu_sourcefile(vars2vals,ori_cpp_path,out_cpp_path):
    with open(ori_cpp_path, 'r') as f:
        cpp_data = f.read()
    
    
    cpp_data1 = cpp_data.split("// initialize input variables and/or parameters")
    
    cpp_data2 = cpp_data1[1].split("// initialize output variables")[0].split(';')[:-1]
    
    #vars2vals = dict()
    new_cpp_data2 = []
    for i,cell in enumerate(cpp_data2):
        cell2 = cell.split('=')
        #curr_var_val = cell2[-1]
        for key in vars2vals.keys():
            if key in cell2[0] and  (key + 'i') not in cell2[0]:
                newcell = cell2[0] + '= '+str(vars2vals[key])
                break
        new_cpp_data2.append(newcell)
        
    for icell,cell in enumerate(cpp_data2):
        cpp_data1[1] = cpp_data1[1].replace(cell,new_cpp_data2[icell])
    
    new_cpp_data = cpp_data1[0] + "// initialize input variables and/or parameters" + cpp_data1[1]
    
    with open(out_cpp_path,'w') as f:
        f.write(new_cpp_data)

def fmu_compile(vars2vals,ori_cpp_path,out_cpp_path,builder_dir, target_dir):
    edit_fmu_sourcefile(vars2vals,ori_cpp_path,out_cpp_path)

    proc_return = subprocess.run([os.path.join(builder_dir, "build.sh")],
                                check=True,  # Raises an error if the command fails
                                shell=True,   # Use shell to execute the script
                                text=True )

    so_path = os.path.join(builder_dir, "build", "libhex_delta55.so")
    xml_path = os.path.join(builder_dir, "data", "modelDescription.xml")

    #outp_dir = builder_dir +"\\zip_contents\\"
    outp_dir = os.path.join(builder_dir, "zip_contents")
    if not os.path.exists(outp_dir):
        os.mkdir(outp_dir)
        
    #dll_dir = outp_dir + "binaries\\win64\\"
    so_dir = os.path.join(outp_dir, "binaries", "linux64")
    
    if not os.path.exists(so_dir):
        os.makedirs(so_dir, exist_ok=True)    
    copyfile(so_path, os.path.join(so_dir, "hex_delta55.so"))

    change_values_in_modelDescription(xml_path, vars2vals)


    copyfile(xml_path ,os.path.join(outp_dir, "modelDescription.xml"))

    output_fmu_path = os.path.join(target_dir, "hex_delta55_exported.fmu")
    make_archive(output_fmu_path, 'zip', outp_dir)
    if os.path.exists(output_fmu_path):
        os.remove(output_fmu_path)

    os.rename(output_fmu_path+'.zip',output_fmu_path)
    
    return output_fmu_path


