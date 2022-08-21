from fastapi import FastAPI, File, UploadFile
import shutil
from datetime import datetime
import json
from typing import Dict
import pandas as pd
import numpy as np
import http.client

def split_xlsx_in_sondenarray(filename):
    raw_data = pd.read_excel(filename, index_col=0, skiprows=1) #hier muss die erste Zeile weggeschmissen werden
    raw_data = raw_data.dropna(axis=0) # delete all rows with nan values
    raw_data.index = pd.to_datetime(raw_data.index, format='%d/%m/%y %H:%M')
    sonden_data = []
    sonden_data.append(raw_data.iloc[:, :14 ]) #aber nur spalten 1-14
    sonden_data.append(raw_data.iloc[:, 14:28 ]) #aber nur spalten 15-28
    sonden_data.append(raw_data.iloc[:, 28:42 ]) #aber nur spalten 29-42
    sonden_data.append(raw_data.iloc[:, 42:56 ]) #aber nur spalten 43-56
    return sonden_data

def generate_analysis_dict(sonde: int , sonden_df: pd.DataFrame) -> Dict:
    column_extension = f".{sonde}" if sonde > 0 else ""
    temp_dict = {   
                    "Sonde": f"Sonde{sonde}" ,
                    "Tag": datetime.strftime(sonden_df.index[0], "%y_%m_%d"),
                    "Wassermelder %": int(sonden_df[f'Wassermelder{column_extension}'].mean()),
                    "Fehlercode": sonden_df[f'Fehlercode{column_extension}'][0],
                    "Logger": int(sonden_df[f'Logger{column_extension}'][0]),
                    "Seriennummer": int(sonden_df[f'Seriennr.{column_extension}'][0]),
                    "Stroemung X": sonden_df[f'Strömung X{column_extension}'].mean(),
                    "Sigma(Stroemung X)": sonden_df[f'Strömung X{column_extension}'].std(),
                    "Stroemung Y": sonden_df[f'Strömung Y{column_extension}'].mean(),
                    "Sigma(Stroemung Y)": sonden_df[f'Strömung Y{column_extension}'].std(),
                    "Temperatur": sonden_df[f'Temperatur{column_extension}'].mean(),
                    "Sigma(Temperatur)": sonden_df[f'Temperatur{column_extension}'].std(),
                    "Druck": sonden_df[f'Druck{column_extension}'].mean(),
                    "Sigma(Druck)": sonden_df[f'Druck{column_extension}'].std(),
                    "Leitfaehigkeit": sonden_df[f'Leitfähigkeit{column_extension}'].mean(),
                    "Sigma(Leitfaehigkeit)": sonden_df[f'Leitfähigkeit{column_extension}'].std(),
                    "Kappa25": sonden_df[f'Kappa 25{column_extension}'].mean(),
                    "Sigma(Kappa25)": sonden_df[f'Kappa 25{column_extension}'].std(),
                    "Ges. Stroemung": sonden_df[f'Ges. Strömung{column_extension}'].mean(),
                    "Sigma(Ges. Stroemung)": sonden_df[f'Ges. Strömung{column_extension}'].std(),
                    "Stroemungsrichtung": sonden_df[f'Strömungsrichtung{column_extension}'].std(),
                    "Sigma(Stroemungsrichtung)": sonden_df[f'Strömungsrichtung{column_extension}'].mean()
                    }
    for key, val in temp_dict.items():
        if isinstance(val, np.int64):
            temp_dict[key] = int(val)
        elif isinstance(val, float):
            temp_dict[key] = round(val, 4)

    #Werte aus df bestimmen, in ein JSON und zurückgeben

    return temp_dict




app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type != "application/octet-stream":
        return {"Info":f"Invalid document type {file.content_type}, *.xlsx expected"}
    with open ("temporary.xlsx", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    sonden_data = split_xlsx_in_sondenarray("temporary.xlsx")
    sonden_dictlist = [generate_analysis_dict(sonde=idx, sonden_df = x) for idx, x in enumerate(sonden_data)]

    result = [json.dumps(set, indent=4, ensure_ascii=False) for set in sonden_dictlist]

    return {"Info": f"success: {result}"}

