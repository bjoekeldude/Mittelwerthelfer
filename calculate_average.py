import json
import argparse
import pandas as pd
import logging

logger = logging.getLogger(__file__)

def split_xlsx_in_sondenarray(filename):
    raw_data = pd.read_excel(args.filename, index_col=0, skiprows=1) #hier muss die erste Zeile weggeschmissen werden
    raw_data = raw_data.dropna(axis=0) # delete all rows with nan values
    logger.debug(raw_data.info())
    sonden_data = []
    sonden_data.append(raw_data.iloc[:, :14 ]) #aber nur spalten 1-14
    sonden_data.append(raw_data.iloc[:, 15:28 ]) #aber nur spalten 15-28
    sonden_data.append(raw_data.iloc[:, 28:42 ]) #aber nur spalten 29-42
    sonden_data.append(raw_data.iloc[:, 42:56 ]) #aber nur spalten 43-56
    return sonden_data

def generate_analysis_dict(sonde, sonden_df):
    temp_dict = {   
                    "Sonde": 'none',
                    "Tag": 'none',
                    "Wassermelder %": 'none',
                    "Fehlercode": 'none',
                    "Logger": 'none',
                    "Seriennummer": 'none',
                    "Strömung X": 'none',
                    "Sigma(Strömung X)": 'none',
                    "Strömung Y": 'none',
                    "Sigma(Strömung Y)": 'none',
                    "Temperatur": 'none',
                    "Sigma(Temperatur)": 'none',
                    "Druck": 'none',
                    "Sigma(Druck)": 'none',
                    "Leitfähigkeit": 'none',
                    "Sigma(Leitfähigkeit)": 'none',
                    "Kappa25": 'none',
                    "Sigma(Kappa25)": 'none',
                    "Ges. Strömung": 'none',
                    "Sigma(Ges. Strömung)": 'none',
                    "Strömungsrichtung": 'none',
                    "Sigma(Strömungsrichtung)": 'none'
                    }

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

    sonden_dictlist = [generate_analysis_dict(sonde="test", sonden_df = x) for x in sonden_data]

    for set in sonden_dictlist:
        logger.debug(set)
        with open(str(set.get("Sonde", "NoSonde"))+"_"+str(set.get("Tag", "unbekannterTag")),"w") as outfile:
            jsonstr = json.dumps(set)
            logger.debug(jsonstr)
            outfile.write(jsonstr)
