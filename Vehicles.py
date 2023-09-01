# What we care about:
# Year, Make, Model, License Plate Number, Mileage, Diver,
import pandas as pd
from csv import DictWriter


class Motor_Vehicle:
    def __init__(self, ):
        self.data_frame_format = {
            "Plate Number": [],
             "Color": [],
             "Year": [],
             "Make": [],
             "Model": [],
             "Driver": []
        }

        self.current_data = pd.read_csv("Data/Vehicle-Data.csv")

    def search_database(self, plate_number):
        return self.current_data.loc[self.current_data['Plate Number'] == plate_number].values[0]

    def create_database_entry(self, dict_of_values):

        df_dictionary = pd.DataFrame([dict_of_values])

        self.current_data = pd.concat([self.current_data, df_dictionary])


        self.current_data.to_csv('Data/Vehicle-Data.csv', mode='w', index=False, header=True)

        # print message
        print("Data appended successfully.")








        #list_of_fieldnames = [key for key in dict_of_values.keys()]
        #list_of_values = [val for val in dict_of_values.values()]

        #with open("Data/Vehicle-Data.csv", "a") as doc:
        #    dictwriter_object = DictWriter(doc, fieldnames=list_of_fieldnames)
        #    dictwriter_object.writerow(dict_of_values)
        #    doc.close()


#test = Motor_Vehicle()
#print(test.search_database("012ABC"))
#
#
#
#
#test.create_database_entry(
#    {"Plate Number": "555SEX", "Color":"Gold", "Year": "2009", "Make":"Buick", "Model": "Crosstrek",
#     "Driver": "Unknown"})
#
#
#print(test.current_data)
#
#other_test = Motor_Vehicle()
#
#print(other_test.current_data)

