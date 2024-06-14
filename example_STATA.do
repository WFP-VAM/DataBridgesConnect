python:

"""
Read a 'full' Household dataset  from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""

from data_bridges_utils import DataBridgesShapes
from data_brdiges_utils.labels import map_value_labels, get_stata_variable_labels
from data_bridges_utils.load_stata import load_stata
import stata_setup

stata_path = r"E:\Program Files\Stata18"
stata_version = "mp"

stata_setup.config(stata_path, stata_version)
from sfi import Data, Macro,  SFIToolkit, Frame, Datetime as dt

# Path to YAML file containing Data Bridges API credentials
CONFIG_PATH = r"data_bridges_api_config.yaml"

# Example dataset and questionnaire from 2023 Congo CFSVA
CONGO_CFSVA = {
    'questionnaire': 1509,
    'dataset': 3094
}

# Initialize DataBridges client with credentials from YAML file
client = DataBridgesShapes(CONFIG_PATH)

# Get houhold data for survey id
survey_data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='full')
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Map the categories to survey_data
mapped_survey_data = map_value_labels(survey_data, questionnaire)

# Load into STATA dataframe
ds1 = load_stata(mapped_survey_data, stata_path, stata_version)

var_label = get_stata_variable_labels(questionnaire)
ds2 = load_stata(survey_data, stata_path, stata_version, variable_labels=var_label)


end