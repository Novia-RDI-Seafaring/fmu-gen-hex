import gradio as gr
from fmu_gen_hex.hex import objfun4
from fmu_gen_hex.sim import simulate_model
from fmu_gen_hex.data_extraction import process_pdf
import os
import gradio as gr
from gradio_pdf import PDF
from pdf2image import convert_from_path
import numpy as np
import pandas as pd
import json
import os

from fmu_gen_hex.callbacks import *

OUTPUT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, "output"))

# --- some colors to indicate required, found, and optional parameter fields ---
css = """
#flow_required, #ncell_required, #k_required {background-color: #FFFCFA}
.optional {background-color: #FFF}
.required_block.required {
    border: 2px solid red;
    padding: 10px;
}

"""

js = """
function setupInputListeners() {
    function markRequired(element) {
        // Update the border based on whether the input is empty
        if(element.value.trim()) {
            element.style.border = '2px solid green'; // Field is correctly filled
        } else {
            element.style.border = '2px solid red'; // Field is empty and required
        }
    }

    function markAllRequired() {
        // Check individual inputs and textareas
        const inputs = document.querySelectorAll('.required_input input, .required_input textarea');
        inputs.forEach(input => {
            markRequired(input); // Mark each required field based on its content
        });

        // Check blocks for any empty required inputs or textareas
        document.querySelectorAll('.required_block').forEach(block => {
            const inputs = block.querySelectorAll('input, textarea');
            const isAnyEmpty = Array.from(inputs).some(input => !input.value.trim());
            block.classList.toggle('required', isAnyEmpty); // Toggle 'required' class if any input is empty
        });
    }

    // Simulate loading data and validating the form
    function loadDataAndValidate(pdfData, callback) {
        setTimeout(() => {
            callback(); // Execute callback function after simulated delay
        }, 500);
    }

    // Event listener for the button that triggers data loading and validation
    const extBtn = document.getElementById('ext_info_btn');
    extBtn.addEventListener('click', function() {
        loadDataAndValidate('', markAllRequired);
    });

    // Event listener for each input and textarea to update border on changes
    document.querySelectorAll('.required_input input, .required_input textarea').forEach(input => {
        input.addEventListener('input', () => {
            markRequired(input); // Re-check and mark the individual field
        });
    });
}
"""

def export_fmu_and_download(*args):

    fmu_path = export_fmu_callback(*args, OUTPUT_DIR)

    return fmu_path, gr.update(visible=True)



# --- layout ---
with gr.Blocks(css=css, js=js) as demo:
    # PDF column
    with gr.Row():
        with gr.Row():
            gr.Markdown("# Heat-Exchanger FMU generation")
    with gr.Row():
        with gr.Column():
            # pdf = gr.Image(label="PDF")
            pdf = PDF(label="PDF")
            ext_btn = gr.Button("Extract information", icon="resources/download-circle-orange.svg",variant="primary", elem_id="ext_info_btn")
            
        # --- DATA SHEET COLUMN ---    
        with gr.Column(min_width=800):
            # General information
            with gr.Accordion("General information", open=False):
                with gr.Row():
                    supplier = gr.Textbox(label="Supplier name",elem_classes="optional",interactive=True)
                    ref = gr.Textbox(label="Reference number",elem_classes="optional",interactive=True)
                    itemNumber = gr.Textbox(label="Item number",elem_classes="optional",interactive=True)
                with gr.Row():
                    customerName = gr.Textbox(label="Customer name",elem_classes="optional",interactive=True)
                with gr.Row():
                    riskFactor = gr.Textbox(label="Risk factor",elem_classes="optional",interactive=True)
                    model = gr.Textbox(label="Model",elem_classes="optional",interactive=True)
                    date = gr.Textbox(label="Date issued",elem_classes="optional",interactive=True)
                    place = gr.Textbox(label="Place issued",elem_classes="optional",interactive=True)
                with gr.Row():
                    flowType = gr.Radio(["Counter flow","Parallel flow"],label="* Flow direction",info="test",elem_id="flow_required",interactive=True)

            # Operation point
            with gr.Accordion("Operating point", open=False, elem_classes=["required_block"]) as op_accordion:
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Side 1**")
                        media1 = gr.Textbox(label="Media",interactive=True)
                        specificHeatCapacity1 = gr.Textbox(label="* Specific heat capacity",info="kJ/kg/K", elem_classes=["required_input"], interactive=True)
                        inletTemperature1 = gr.Textbox(label="* Inlet temperature",info="degC", elem_classes=["required_input"], interactive=True)
                        outletTemperature1 = gr.Textbox(label="* Outlet temperature",info="degC",elem_classes=["required_input"], interactive=True)
                        flowRate1 = gr.Textbox(label="* Mass flow rate",info="kg/s", elem_classes=["required_input"], interactive=True)
                        liquidMass1 = gr.Textbox(label="* Liquid mass",info="kg", elem_classes=["required_input"], interactive=True)
                        liquidVolume1 = gr.Textbox(label="Liquid volume",info="m^3",elem_id="optional",interactive=True)
                        liquidDensity1 = gr.Textbox(label="Liquid density",info="kg/m^3",elem_id="optional",interactive=True)
                    with gr.Column():
                        gr.Markdown("**Side 2**")
                        media2 = gr.Textbox(label="Media", interactive=True)
                        specificHeatCapacity2 = gr.Textbox(label="* Specific heat capacity",info="kJ/kg/K", elem_classes=["required_input"], interactive=True)
                        inletTemperature2 = gr.Textbox(label="* Inlet temperature",info="degC", elem_classes=["required_input"], interactive=True)
                        outletTemperature2 = gr.Textbox(label="* Outlet temperature",info="degC",elem_classes=["required_input"], interactive=True)
                        flowRate2 = gr.Textbox(label="* Mass flow rate",info="kg/s",elem_classes=["required_input"], interactive=True)
                        liquidMass2 = gr.Textbox(label="* Liquid mass",info="kg",elem_classes=["required_input"], interactive=True)
                        liquidVolume2 = gr.Textbox(label="Liquid volume",info="m^3",elem_id="optional",interactive=True)
                        liquidDensity2 = gr.Textbox(label="Liquid density",info="kg/m^3",elem_id="optional",interactive=True)

            # Remarks  
            with gr.Accordion("Remarks", open=False):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Side 1**")
                        testPressure1 = gr.Textbox(label="Test pressure",info="bar",elem_classes="optional",interactive=True)
                        designPressure1 = gr.Textbox(label="Design pressure",info="bar",elem_classes="optional",interactive=True)
                        maxTemperature1 = gr.Textbox(label="Max temperature",info="degC",elem_classes="optional",interactive=True)
                        minTemperature1 = gr.Textbox(label="Min temperature",info="degC",elem_classes="optional",interactive=True)
                    with gr.Column():
                        gr.Markdown("**Side 2**")
                        testPressure2 = gr.Textbox(label="Test pressure",info="bar",elem_classes="optional",interactive=True)	                      
                        designPressure2 = gr.Textbox(label="Design pressure",info="bar",elem_classes="optional",interactive=True)
                        maxTemperature2 = gr.Textbox(label="Max temperature",info="degC",elem_classes="optional",interactive=True)
                        minTemperature2 = gr.Textbox(label="Min temperature",info="degC",elem_classes="optional",interactive=True)
                    netWeight = gr.Textbox(label="Net weight",info="kg",elem_id="optional",interactive=True)
                    weightWithWater = gr.Textbox(label="Weight with water",info="kg",elem_classes="optional",interactive=True)
                    heatingSurface = gr.Textbox(label="Heating surface",info="m^2",elem_classes="optional",interactive=True)
                    coolingCapacity = gr.Textbox(label="Cooling capacity",info="kW",elem_classes="optional",interactive=True)
                    heatTransferCoefficient = gr.Textbox(label="Heat transfer coefficient",info="W/m^2/K",elem_classes="optional",interactive=True)
            
            # Advanced parameters
            with gr.Accordion("Advanced parameters",open=False):
                with gr.Row():
                    nCells = gr.Textbox(10,label="* Number of cells",info="The model is discretized in n number of cells.",elem_id="ncell_required",interactive=True)
                    K = gr.Textbox(10000,label="* Effective heat-transfer coefficient",info="K=Ah for large n",elem_id="k_required",interactive=True) # optimized_K_display
                opt_btn = gr.Button("Optimize",variant="secondary",icon="resources/auto-fix.svg",interactive=True)
                
            # Simulation section
            with gr.Row():
                ax = gr.ScatterPlot(
                    x = "Time",
                    y = "Temperature",
                    color="Name",
                    tooltip="Name",
                    y_title="Temperature",
                    color_legend_title="Signals",
                    container=False,
                    width=600,
                    height=200
                )
            with gr.Row():
                #sim_btn = gr.Button("Simulate",icon="resources/controller-classic.svg",variant="secondary")
                fmu_btn = gr.Button("Compile FMU",variant="secondary")
            with gr.Row(visible=False) as FMUFile:
                download_btn = gr.File(label="Download FMU")

      
        ext_btn.click(process_pdf, 
            inputs=[pdf],
            outputs=[supplier, ref, itemNumber, customerName, riskFactor, model, date, place, flowType,
                    media1, specificHeatCapacity1, inletTemperature1, outletTemperature1, flowRate1, liquidMass1, liquidVolume1, liquidDensity1,
                    media2, specificHeatCapacity2, inletTemperature2, outletTemperature2, flowRate2, liquidMass2, liquidVolume2, liquidDensity2,
                    testPressure1, designPressure1, maxTemperature1, minTemperature1,
                    testPressure2, designPressure2, maxTemperature2, minTemperature2,
                    netWeight, weightWithWater, heatingSurface, coolingCapacity, heatTransferCoefficient]
        )
        # opt_btn callback
        opt_btn.click(
            optimize_callback, 
            [
                supplier, ref, itemNumber, customerName, riskFactor, model, date, place, flowType,
                media1, specificHeatCapacity1, inletTemperature1, outletTemperature1, flowRate1, liquidMass1, liquidVolume1, liquidDensity1,
                media2, specificHeatCapacity2, inletTemperature2, outletTemperature2, flowRate2, liquidMass2, liquidVolume2, liquidDensity2,
                testPressure1, designPressure1, maxTemperature1, minTemperature1,
                testPressure2, designPressure2, maxTemperature2, minTemperature2,
                netWeight, weightWithWater, heatingSurface, coolingCapacity, heatTransferCoefficient, nCells, K
            ],
            outputs=[ax, K]  # K == a component to display the optimized K value
        )

        export_fmu_inputs = [K,nCells,flowType,specificHeatCapacity1,specificHeatCapacity2,inletTemperature1,
                             inletTemperature2,flowRate1,flowRate2,liquidMass1,liquidMass2]
        
        
        fmu_btn.click(export_fmu_and_download, inputs=export_fmu_inputs, outputs=[download_btn, FMUFile])


if __name__ == "__main__":
    demo.launch()