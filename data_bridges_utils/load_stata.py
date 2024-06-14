import stata_setup
from data_bridges_utils.labels import get_column_labels, get_value_labels

def load_stata(df, stata_path="C:/Program Files/Stata18", stata_version="se", variable_labels=None, value_labels=None):
    stata_setup.config(stata_path, stata_version)
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
    colnames = df.columns
    Data.setObsTotal(len(df))

    for i in range(len(colnames)):
        dtype = df[colnames[i]].dtype
        varname = SFIToolkit.makeVarName(colnames[i], retainCase=True)
        varval = df[colnames[i]].values.tolist()

        # try:
        #     if variable_labels and varname in variable_labels:
        #         Data.setVarLabel(varname, variable_labels[varname])
        # except ValueError as e:
        #     print(f"Error: {e}. Skipping variable {varname}.")
        #     continue

        # try:
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
