from datetime import datetime
import json
import argparse
from typing import Dict
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__file__)

def split_xlsx_in_sondenarray(filename):
    raw_data = pd.read_excel(args.filename, index_col=0, skiprows=1) #hier muss die erste Zeile weggeschmissen werden
    raw_data = raw_data.dropna(axis=0) # delete all rows with nan values
    raw_data.index = pd.to_datetime(raw_data.index, format='%d/%m/%y %H:%M')
    logger.debug(raw_data.info())
    sonden_data = []
    sonden_data.append(raw_data.iloc[:, :14 ]) #aber nur spalten 1-14
    sonden_data.append(raw_data.iloc[:, 14:28 ]) #aber nur spalten 15-28
    sonden_data.append(raw_data.iloc[:, 28:42 ]) #aber nur spalten 29-42
    sonden_data.append(raw_data.iloc[:, 42:56 ]) #aber nur spalten 43-56
    return sonden_data

def generate_analysis_dict(sonde: int , sonden_df: pd.DataFrame) -> Dict:
    logger.info(sonden_df.iloc[0, :5])
    logger.info(sonden_df.iloc[:, 5:].describe())
    column_extension = f".{sonde}" if sonde > 0 else ""
    temp_dict = {   
                    "Sonde": f"Sonde{sonde}" ,
                    "Tag": datetime.strftime(sonden_df.index[0], "%y_%m_%d"),
                    "Wassermelder %": int(sonden_df[f'Wassermelder{column_extension}'].mean()),
                    "Fehlercode": sonden_df[f'Fehlercode{column_extension}'][0],
                    "Logger": int(sonden_df[f'Logger{column_extension}'][0]),
                    "Seriennummer": int(sonden_df[f'Seriennr.{column_extension}'][0]),
                    "Strömung X": sonden_df[f'Strömung X{column_extension}'].mean(),
                    "Sigma(Strömung X)": sonden_df[f'Strömung X{column_extension}'].std(),
                    "Strömung Y": sonden_df[f'Strömung Y{column_extension}'].mean(),
                    "Sigma(Strömung Y)": sonden_df[f'Strömung Y{column_extension}'].std(),
                    "Temperatur": sonden_df[f'Temperatur{column_extension}'].mean(),
                    "Sigma(Temperatur)": sonden_df[f'Temperatur{column_extension}'].std(),
                    "Druck": sonden_df[f'Druck{column_extension}'].mean(),
                    "Sigma(Druck)": sonden_df[f'Druck{column_extension}'].std(),
                    "Leitfähigkeit": sonden_df[f'Leitfähigkeit{column_extension}'].mean(),
                    "Sigma(Leitfähigkeit)": sonden_df[f'Leitfähigkeit{column_extension}'].std(),
                    "Kappa25": sonden_df[f'Kappa 25{column_extension}'].mean(),
                    "Sigma(Kappa25)": sonden_df[f'Kappa 25{column_extension}'].std(),
                    "Ges. Strömung": sonden_df[f'Ges. Strömung{column_extension}'].mean(),
                    "Sigma(Ges. Strömung)": sonden_df[f'Ges. Strömung{column_extension}'].std(),
                    "Strömungsrichtung": sonden_df[f'Strömungsrichtung{column_extension}'].std(),
                    "Sigma(Strömungsrichtung)": sonden_df[f'Strömungsrichtung{column_extension}'].mean()
                    }
    for key, val in temp_dict.items():
        if isinstance(val, np.int64):
            temp_dict[key] = int(val)
        elif isinstance(val, float):
            temp_dict[key] = round(val, 4)

    #Werte aus df bestimmen, in ein JSON und zurückgeben

    return temp_dict


if __name__ == '__main__':
    FORMAT = '%(levelname)s:%(message)s'
    logging.basicConfig(format=FORMAT,
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Durchschnittsbestimmung Sensordatenfile")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input file", metavar="FILE")
    args = parser.parse_args()
    
    sonden_data = split_xlsx_in_sondenarray(args.filename)

    sonden_dictlist = [generate_analysis_dict(sonde=idx, sonden_df = x) for idx, x in enumerate(sonden_data)]

    for set in sonden_dictlist:
        logger.debug(set)
        with open(f'{set.get("Sonde", "NoSonde")}_{set.get("Tag")}.json',"w") as outfile:
            json.dump(set, outfile, indent=4, ensure_ascii=False)
