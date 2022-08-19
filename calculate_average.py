import json
import argparse
import pandas as pd

def split_xlsx_in_sondenarray(filename):
    raw_data = pd.read_excel(args.filename, index_col=0) #hier muss die erste Zeile weggeschmissen werden
    sonden_data = []
    sonden_data[0] = raw_data #aber nur spalten 1-14
    sonden_data[1] = raw_data #aber nur spalten 15-28
    sonden_data[2] = raw_data #aber nur spalten 29-42
    sonden_data[3] = raw_data #aber nur spalten 43-56
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
    parser = argparse.ArgumentParser(description="Durchschnittsbestimmung Sensordatenfile")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input file", metavar="FILE")
    args = parser.parse_args()

    sonden_data = split_xlsx_in_sondenarray(args.filename)

    sonden_dict = []
    for n in range(0,3):
        sonden_dict[n] = generate_analysis_dict(sonden_data[n])

    for set in sonden_dict:
        with open(str(set)+"_"+str(sonden_dict["Tag"]),"w") as outfile:
            jsonstr = json.dumps(set)
            outfile.write(jsonstr)
