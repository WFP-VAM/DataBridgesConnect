import stata_setup
from data_bridges_utils.labels import get_column_labels, get_value_labels

def load_stata(df, stata_path="C:/Program Files/Stata18", stata_version="se", variable_labels=None, value_labels=None):
    # Configure the Stata installation path and version
    stata_setup.config(stata_path, stata_version)
    # Import necessary modules from the sfi package
    from sfi import Data, Macro, SFIToolkit, Frame, Datetime as dt

    """
    Loads a Pandas DataFrame into a Stata data file format.

    Args:
        df (pandas.DataFrame): The DataFrame to be loaded into Stata format.
        stata_path (str, optional): The path to the Stata installation. Defaults to "C:/Program Files/Stata18".
        stata_version (str, optional): The Stata version. Defaults to "se".
        variable_labels (dict, optional): A dictionary containing variable labels. Defaults to None.
        value_labels (dict, optional): A dictionary containing value labels. Defaults to None.

    Returns:
        pandas.DataFrame: The original DataFrame.
    """
    # Get the column names from the DataFrame
    colnames = df.columns
    # Set the total number of observations in the Stata Data object
    Data.setObsTotal(len(df))

    # Iterate over the columns in the DataFrame
    for i in range(len(colnames)):
        # Get the data type of the current column
        dtype = df.dtypes[i].name
        # Create a Stata-compatible variable name from the column name
        varname = SFIToolkit.makeVarName(colnames[i], retainCase=True)
        # Get the values of the current column as a list
        varval = df[colnames[i]].values.tolist()

        try:
            # If variable_labels is provided and the current variable name is in the dictionary,
            # set the variable label in Stata
            if variable_labels and varname in variable_labels:
                Data.setVarLabel(varname, variable_labels[varname])
        except ValueError as e:
            print(f"Error: {e}. Skipping variable {varname}.")
            continue

        # try:
        #     # If value_labels is provided and the current variable name is in the dictionary,
        #     # create a value label in Stata and associate it with the current variable
        #     if value_labels and varname in value_labels:
        #         value_label_name = f"{varname}_value_label"
        #         ValueLabel.createLabel(value_label_name)
        #         for value, label in value_labels[varname].items():
        #             ValueLabel.setLabelValue(value_label_name, value, label)
        #         ValueLabel.setVarValueLabel(varname, value_label_name)
        # except ValueError as e:
        #     print(f"Error: {e}. Skipping variable {varname}.")
        #     continue

        try:
            # Based on the data type of the current column, add a variable to the Stata Data object
            # and store the values in the appropriate format
            if dtype == "int64":
                Data.addVarInt(varname)
                Data.store(varname, None, varval)
            elif dtype == "float64":
                Data.addVarDouble(varname)
                Data.store(varname, None, varval)
            elif dtype == "bool":
                Data.addVarByte(varname)
                Data.store(varname, None, varval)
            elif dtype == "datetime64[ns]":
                Data.addVarFloat(varname)
                price_dt_py = [dt.getSIF(j, '%tdCCYY-NN-DD') for j in df[colnames[i]]]
                Data.store(varname, None, price_dt_py)
                Data.setVarFormat(varname, '%tdCCYY-NN-DD')
            else:
                Data.addVarStr(varname, 1)
                s = [str(i) for i in varval]
                Data.store(varname, None, s)

        except ValueError as e:
            print(f"Error: {e}. Skipping variable {varname}.")

    return df


# /* Data.setVarLabel(var, label)
# # Set the variable label. The field "label" has to be str, "var" the name of an existing variable in the Stata Data object.

# ValueLabel.createLabel('repair')
# # Create a value label with a name (e.g.: 'repair'). This is only the empty dictionary that interprets the value of a specific variable.

# ValueLabel.getNames()
# # Gets the list of value labels available in Data.

# ValueLabel.setLabelValue('repair', 1, 'One')
# # Populates the dictionary of value labels

# ValueLabel.getValueLabels('repair')
# # Returns the list of value labels of a specific dictionary
# # {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}

# ValueLabel.setVarValueLabel('rep78', 'repair')
# # associates the value labels dictionary (repair) to an existing variable (e.g.: rep78)

# ValueLabel.getVarValueLabel('rep78')
# # returns the value label (e.g.: repair) from an existing variable (e.g.: rep78) */
