import os
import json
import traceback
from dotenv import load_dotenv
load_dotenv('./.env')
from meri import MERI, MERI_CONFIGS_PATH


# --- PDF extraction configuration ---
config_path = 'demo_data/he-specification_schema.json'
api_key = os.getenv('OPENAI_API_KEY')


# --- Unit Conversion ---
def convert_units(value, unit):
    # Conversion factors and mappings for various units
    conversions = {        
        "lb": ("kg", value / 2.20462),  # Convert pounds to kg
        "lb/h": ("kg/s", value / 7936.64),  # Convert lb/h to kg/s
        "lb/ft3": ("kg/m^3", value / 0.062428),  # Convert lb/ft3 to kg/m^3
        "ft^3": ("m^3", value / 35.3147),  # Convert cubic feet to cubic meters
        "deg fahrenheit": ("deg celsius", (value - 32) * 5/9),  # Convert Fahrenheit to Celsius
        "F": ("C", (value - 32) * 5/9),  # Convert Fahrenheit to Celsius
        "psi": ("bar", value / 14.5038),  # Convert psi to bar
        "W": ("kW", value / 1000),  # Convert W to kW
        
        # we can add other necessary conversions
    }
    # Check if the unit is in the conversion mapping
    if unit in conversions:
        new_unit, new_value = conversions[unit]
        return round(new_value, 2), new_unit
    else:
        return round(value, 2), unit  # Return the original if no conversion is defined

def convert_side_units(side_data):
    if isinstance(side_data, dict):
        for key, value in side_data.items():
            if isinstance(value, dict) and 'value' in value and 'unit' in value:
                converted_value, converted_unit = convert_units(value['value'], value['unit'])
                value['value'], value['unit'] = converted_value, converted_unit

# --- Unit Conversion for the entire tuple ---
def convert_tuple_units(tuple_values):
    
    pass
    
# https://www.vedantu.com/physics/density-of-water
# https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html
# https://www.vcalc.com/wiki/Water%20Density%20by%20Temperature
def compute_water_properties(mass=None, volume=None, density=None, temperature=None, compute='mass'):
    # Density of water at standard temperature (25 C or 298 K) is approximately 997 kg/m^3
    standard_density = 997  # kg/m^3

    if temperature is not None:
        #TODO Adjust density for different temperatures if necessary, simplified assumption
        density = standard_density # Placeholder for actual temperature adjustment formula

    if compute == 'mass' and volume is not None and density is not None:
        return volume * density  # mass = density * volume
    elif compute == 'volume' and mass is not None and density is not None:
        return mass / density  # volume = mass / density
    elif compute == 'density' and mass is not None and volume is not None:
        return mass / volume  # density = mass / volume
    elif compute == 'temperature':
        #TODO Implement temperature-dependent calculations if needed
        return temperature  # Placeholder for actual calculation
    else:
        return None



# --- PDF extraction ---
#def get_extracted_data(pdf_path, schema_path, str_val, api_key):
#    headers = {"Authorization": f"Bearer {api_key}"}
#    # print("Headers being sent:", headers) # Debugging to check if the headers are being sent
#    multimodal_llm = OpenAIMultiModal('gpt-4-vision-preview', max_new_tokens=4000, timeout=500, image_detail='auto', api_key=api_key)
#    json_schema_string = readJsonFile(schema_path)
#    pdf = SearchablePDF(pdf_path, json_schema_string, str_val, multimodal_llm=multimodal_llm)
    #extracted_data = pdf._getText()
#    return pdf

def extract_params_from_pdf(pdf_path, json_schema_path):
    with open(json_schema_path) as f:
        schema = json.load(f)

    # use default configurartion
    config_path = os.path.join(MERI_CONFIGS_PATH, "meri_yolo.yaml")

    meri = MERI(pdf_path=pdf_path, config_yaml_path=config_path)

    # populate provided json schema
    populated_schema = meri.run(json.dumps(schema))

    return populated_schema

def get_param_properties(param_dict, key):
    return param_dict.get(key, {}).get("parameter_properties", {})

def param_dict_to_param_formatted_param_list(param_dict):
    
    default_text = ""
    default_value = "0"

    return [
        get_param_properties(param_dict, "supplier").get('text', default_text),
        get_param_properties(param_dict, "ref").get('text', default_text),
        get_param_properties(param_dict, "itemNumber").get('text', default_text),
        get_param_properties(param_dict, "customerName").get('text', default_text),
        get_param_properties(param_dict, "riskFactor").get('text', default_text),
        get_param_properties(param_dict, "model").get('text', default_text),
        '', # data
        '', # place
        "Parallel flow" if "Counter" not in get_param_properties(param_dict, "flowType").get('text', '') else "Counter flow",
        
        # Operation point side 1
        get_param_properties(param_dict, "side1Media").get('text', default_text),
        get_param_properties(param_dict, "side1SpecificHeatCapacity").get('value', default_value),
        get_param_properties(param_dict, "side1InletTemperature").get('value', default_value),
        get_param_properties(param_dict, "side1OutletTemperature").get('value', default_value),
        get_param_properties(param_dict, "side1FlowRate").get('value', default_value),
        get_param_properties(param_dict, "side1LiquidMass").get('value', default_value),
        get_param_properties(param_dict, "side1LiquidVolume").get('value', default_value),
        get_param_properties(param_dict, "side1LiquidDensity").get('value', default_value),
        
        # Operation point side 2
        get_param_properties(param_dict, "side2Media").get('text', default_text),
        get_param_properties(param_dict, "side2SpecificHeatCapacity").get('value', default_value),
        get_param_properties(param_dict, "side2InletTemperature").get('value', default_value),
        get_param_properties(param_dict, "side2OutletTemperature").get('value', default_value),
        get_param_properties(param_dict, "side2FlowRate").get('value', default_value),
        get_param_properties(param_dict, "side2LiquidMass").get('value', default_value),
        get_param_properties(param_dict, "side2LiquidVolume").get('value', default_value),
        get_param_properties(param_dict, "side2LiquidDensity").get('value', default_value),

        # Remarks side 1
        get_param_properties(param_dict, "side1TestPressure").get('value', default_text),
        get_param_properties(param_dict, "side1DesignPressure").get('value', default_value),
        get_param_properties(param_dict, "side1MaxTemperature").get('value', default_value),
        get_param_properties(param_dict, "side1MinTemperature").get('value', default_value),

        # Remarks side 2
        get_param_properties(param_dict, "side2TestPressure").get('value', default_text),
        get_param_properties(param_dict, "side2DesignPressure").get('value', default_value),
        get_param_properties(param_dict, "side2MaxTemperature").get('value', default_value),
        get_param_properties(param_dict, "side2MinTemperature").get('value', default_value),

        # Remarks extra parameters
        get_param_properties(param_dict, "side1NetWeight").get('value', default_text),
        get_param_properties(param_dict, "side1WeightWithWater").get('value', default_value),
        get_param_properties(param_dict, "side1HeatingSurface").get('value', default_value),
        get_param_properties(param_dict, "side1CoolingCapacity").get('value', default_value),
        get_param_properties(param_dict, "side1HeatTransferCoefficient").get('value', default_value)

        ]

# --- PDF processing ---
def process_pdf(pdf_file):
    # If no JSON file path is provided, use the PDF file path with a .json extension
    json_schema_path = os.path.abspath(os.path.join(__file__, os.pardir, "resources", "he-spec_schema.json"))
    #json_file_path = f"{pdf_file}.json"
    print(f"Processing PDF file...", {pdf_file})
    print("jsons chema exists: ", os.path.exists(json_schema_path), json_schema_path)
    try:
        
        extracted_parameters = extract_params_from_pdf(pdf_file, json_schema_path)
   
        print("EXTRACTED PARAMETERS: ", extracted_parameters)
        
        #### Continue here after lunch
        # Convert the values and units according to your requirements
        for key, value in extracted_parameters.items():
            props = value["parameter_properties"]
            if len(props["unit"]) > 0 :
                converted_value, converted_unit = convert_units(props['value'], props['unit'])
                props['value'], props['unit'] = converted_value, converted_unit
        
        # Initialize default values for missing keys
        
        default_text = ""
        default_value = "0"
        
        results = param_dict_to_param_formatted_param_list(extracted_parameters)
        print("RESULTS: ", results)
        return tuple(results)

    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return f"Failed to decode JSON. Check the format of your input: {str(e)}"
    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
        return f"Data extraction failed: Missing key {e}"
    except Exception as e:
        print(f"Unexpected error: {e}") # Debugging
        return tuple(["nothing"] * 33), f"Error: Unexpected issue encountered: {str(e)}"
