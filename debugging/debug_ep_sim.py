
from honeybee_energy import run

from honeybee_energy.config import folders

print(folders.openstudio_exe)

# inputs
osw_directory = "D:\Elie\PhD\Simulation\Program_output\\test\simulation"
path_epw = "D:\Elie\PhD\Simulation\Program_output\\test\IS_5280_A_Haifa.epw"
path_model_json = "D:\Elie\PhD\Simulation\Program_output\\test\in.hbjson"
path_simulation_parameters = "D:\Elie\PhD\Simulation\Program_output\\test\simulation_parameter.json"

## Prepare simulation for OpenStudio ##
osw = run.to_openstudio_osw(osw_directory=osw_directory,
                            model_path=path_model_json,
                            sim_par_json_path=path_simulation_parameters,
                            epw_file=path_epw)

## Run simulation in OpenStudio to generate IDF ##
(osm, idf) = run.run_osw(osw, measures_only=False, silent=False)
# (osm, idf) = run.run_osw(osw, silent=False)

result = run.run_idf(idf, epw_file_path=path_epw, silent=False)