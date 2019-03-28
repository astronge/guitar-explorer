import json
import pandas as pd
import numpy as np
import sys
import os
from pandas.io.json import json_normalize

def clean_data(): 
    # Load json data
    new_data = []

    path = "data/guitar_data/"
    files = [path + json for json in os.listdir(path) if json.endswith(".json")]

    for file in files:
        with open(file) as f:
            data_holder = []
            data_holder = json.load(f)
            count = 1
            
            for guitar in data_holder:
                new_data.append(data_holder[str(count)])
                count = count + 1

    # Create new list to hold conforming data
    clean_data = []

    # Add conforming data to list
    for guitar in new_data:
        if ("Body" in guitar and 
            "Fretboard" in guitar and
            "Hardware" in guitar and
            "Manufacturer" in guitar and
            "Neck" in guitar and
            "Pickups" in guitar):
            clean_data.append(guitar)

    # Put json structure into dataframe  
    df = pd.DataFrame.from_dict(json_normalize(clean_data), orient="columns")
    df = df.sort_index(axis=1)

    # Replace NA values
    df.fillna("", inplace=True)
    df.replace(to_replace=["\t", "\n", "\xa0", "'"], value="", regex=True, inplace=True)

    # Limit data to only 6-string guitars
    df = df[df["Other.Number of strings"].str.contains("6")]

    # Clean body shape data
    col = "Body.Body shape"
    new_col = "body_shape"

    logic = [
        (df[col].str.contains("Double")),
        (df[col].str.contains("Single")),
        (df[col].str.contains("Other")),
        (df[col] == "V"),
        (df[col] == "Z")]
    values = ["Double cutaway", "Single cutaway", "Other", "V", "Z"]
    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean body type data
    col = "Body.Body type"
    new_col = "body_type"

    logic = [
        (df[col].str.contains("Solid")),
        (df[col].str.contains("Hollow body")),
        (df[col].str.contains("Semi"))]
    values = ["Solid", "Hollow", "Semi-hollow"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean neck join data
    col = "Neck.Joint"
    new_col = "neck_joint"

    logic = [
        (df[col].str.contains("Bolt-on", regex=True, case=False)),
        (df[col].str.contains("Set-in", regex=True, case=False)),
        (df[col].str.contains("Neck-through|Thru-neck", regex=True, case=False)),
        (df[col].str.contains("Set-through", regex=True, case=False))
    ]

    values = ["Bolt-on",
            "Set-in", 
            "Neck-thru", 
            "Set-thru"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean neck finish data
    col = "Neck.Neck finish"
    new_col = "neck_finish"

    logic = [
        (df[col].str.contains("Gloss", regex=True, case=False)),
        (df[col].str.contains("Satin", regex=True, case=False)),
        (df[col].str.contains("Oiled|Hand-rubbed", regex=True, case=False))
    ]

    values = ["Gloss",
            "Satin", 
            "Oiled"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean fretboard material data
    col = "Fretboard.Material"
    new_col = "fretboard_material"

    logic = [
        (df[col].str.contains("Maple", regex=True, case=False)),
        (df[col].str.contains("Rosewood", regex=True, case=False)),
        (df[col].str.contains("Ebony", regex=True, case=False)),
    ]

    values = ["Maple",
            "Rosewood", 
            "Ebony"]

    df[new_col] = np.select(logic, values, default="Other")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean number of frets data
    col = "Fretboard.Number of frets"
    new_col = "number_of_frets"

    logic = [
        (df[col].str.contains("20", regex=True, case=False)),
        (df[col].str.contains("21", regex=True, case=False)),
        (df[col].str.contains("22", regex=True, case=False)),
        (df[col].str.contains("24", regex=True, case=False))
    ]

    values = ["20",
            "21", 
            "22",
            "24"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean bridge type data
    col = "Hardware.Bridge type"
    new_col = "bridge_type"

    logic = [
        (df[col].str.contains("Tremolo", regex=True, case=False)),
        (df[col].str.contains("Fixed", regex=True, case=False))
    ]

    values = ["Tremolo",
            "Fixed"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean tuning machine data
    col = "Hardware.Tuning machines"
    new_col = "tuners"

    logic = [
        (df[col].str.contains("locking", regex=True, case=False))
    ]

    values = ["Locking"]

    df[new_col] = np.select(logic, values, default="Non-locking")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Active or passive pickups
    col = "Pickups.Active or passive pickups"
    new_col = "active_or_passive"

    logic = [
        (df[col].str.contains("Active", regex=True, case=False)),
        (df[col].str.contains("Passive", regex=True, case=False))
    ]

    values = ["Active",
            "Passive"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean pickup configuration data
    col = "Pickups.Configuration"
    new_col = "pickup_configuration"

    logic = [
        (df[col].str.contains("HH ?|HH\xa0", regex=True, case=False)),
        (df[col].str.contains("HSH", regex=True, case=False)),
        (df[col].str.contains("SSH", regex=True, case=False)),
        (df[col].str.contains("HSS", regex=True, case=False)),
        (df[col].str.contains("^HS$", regex=True, case=False)),
        (df[col].str.contains("^SS ?$", regex=True, case=False)),
        (df[col].str.contains("SSS", regex=True, case=False)),
        (df[col].str.contains("^H$", regex=True, case=False))
    ]

    values = ["HH",
            "HSH",
            "SSH",
            "HSS",
            "HS",
            "SS",
            "SSS",
            "H"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean piezo data
    col = "Pickups.Piezo"
    new_col = "piezo"

    logic = [
        (df[col].str.contains("Yes", regex=True, case=False)),
        (df[col].str.contains("No", regex=True, case=False))
    ]

    values = ["Yes",
            "No"]

    df[new_col] = np.select(logic, values, default="No")

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Clean country data
    col = "Other.Country of origin"
    new_col = "country"

    logic = [
        (df[col].str.contains("Japan", regex=True, case=False)), 
        (df[col].str.contains("United States", regex=True, case=False)),
        (df[col].str.contains("Korea", regex=True, case=False)),
        (df[col].str.contains("Indonesia", regex=True, case=False)),
        (df[col].str.contains("China", regex=True, case=False)),
        (df[col].str.contains("Mexico", regex=True, case=False)),
        (df[col].str.contains("Malaysia", regex=True, case=False))
    ]

    values = ["Japan",
            "United States",
            "South Korea",
            "Indonesia",
            "China",
            "Mexico",
            "Malaysia"]

    df[new_col] = np.select(logic, values, default="Unknown")

    # Clean manufacturer data
    col = 'Manufacturer'
    new_col = 'brand'

    logic = [
        (df[col].str.contains("Charvel", regex=True, case=False)), 
        (df[col].str.contains("DAngelico", regex=True, case=False)),
        (df[col].str.contains("Dean", regex=True, case=False)),
        (df[col].str.contains("Epiphone", regex=True, case=False)),
        (df[col].str.contains("Ernie", regex=True, case=False)),
        (df[col].str.contains("ESP", regex=True, case=False)),
        (df[col].str.contains("EVH", regex=True, case=False)),
        (df[col].str.contains("Fender", regex=True, case=False)),
        (df[col].str.contains("Gibson", regex=True, case=False)),
        (df[col].str.contains("G&L", regex=True, case=False)),
        (df[col].str.contains("Gretsch", regex=True, case=False)),
        (df[col].str.contains("Hamer", regex=True, case=False)),
        (df[col].str.contains("Ibanez", regex=True, case=False)),
        (df[col].str.contains("Jackson", regex=True, case=False)),
        (df[col].str.contains("Line", regex=True, case=False)),
        (df[col].str.contains("Mitchell", regex=True, case=False)),
        (df[col].str.contains("PRS", regex=True, case=False)),
        (df[col].str.contains("Reverend", regex=True, case=False)),
        (df[col].str.contains("Schecter", regex=True, case=False)),
        (df[col].str.contains("Squier", regex=True, case=False)),
        (df[col].str.contains("Sterling", regex=True, case=False)),
        (df[col].str.contains("Strandberg", regex=True, case=False)),
        (df[col].str.contains("Washburn", regex=True, case=False))
    ]

    values = ['Charvel',
            'DAngelico',
            'Dean',
            'Epiphone',
            'Ernie Ball Music Man',
            'ESP',
            'EVH',
            'Fender',
            'Gibson',
            'G&L',
            'Gretsch',
            'Hamer',
            'Ibanez',
            'Jackson',
            'Line 6',
            'Mitchell',
            'PRS',
            'Reverend',
            'Schecter',
            'Squier',
            'Sterling',
            'Strandberg',
            'Washburn']

    df[new_col] = np.select(logic, values, default='Unknown')

    # Drop old column
    df.drop(col, axis=1, inplace=True)

    # Rename existing columns
    df.rename(columns={'Price': 'price', 'Product': 'product'}, inplace=True)

    df2= df[['brand', 
            'price',
            'country',
            'product',
            'page_url',
            'image_url',
            'body_shape',
            'body_type',
            'neck_joint',
            'neck_finish',
            'fretboard_material',
            'number_of_frets',
            'bridge_type',
            'tuners',
            'active_or_passive',
            'pickup_configuration']]

    # Prepare JSON data
    json_data = df2.to_json(orient='records')

    # Write to file
    file_name = "guitar_data.json"

    with open(file_name, "w") as file:
        file.write(json_data)

    # Replace escapes for forward slashes
    with open(file_name, "r") as file:
        file_data = file.read()

    file_data = file_data.replace("\\", "")

    # Write the file out again
    with open(file_name, "w") as file:
        file.write(file_data)