# -*- coding: utf-8 -*-
"""
Created on Tue May 21 12:38:11 2024

@author: emrkay
"""

def change_values_in_modelDescription(xml_path,vars2vals):
    with open(xml_path, 'r') as f:
        xml_data = f.read()
    
    xml_data2 = xml_data.split('ScalarVariable')
    
    
    
    for varname in vars2vals.keys():
        newval = vars2vals[varname]
        #newval = newvals[ivar]
        for icell,cell in enumerate(xml_data2):
            if 'name="'+varname+'"' in cell:
                istart = cell.find('start')+7
                for i in range(istart,istart+1000):
                    if cell[i]=='"':
                        iend = i
                        break
                cell = cell.replace(cell[(istart-7):iend],'start="'+str(newval))
                xml_data2[icell] = cell
                break
    
    xml_data3 = ""
    for cell in xml_data2[:-1]:
        xml_data3 = xml_data3 +cell+ 'ScalarVariable'
    
    xml_data3 = xml_data3 + xml_data2[-1]
    
    with open(xml_path, 'w') as f:
        f.write(xml_data3)