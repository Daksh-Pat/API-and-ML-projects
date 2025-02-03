import requests
import pandas
import os
from google.cloud import bigquery
import pandas_gbq
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound

Production_Files = os.listdir("Production_Data")
Production_Data = []
Consumption_Files = os.listdir("Consumption_Data")
Consumption_Data = []

def get_data(type,files,data):
	for i in range(len(files)):
		Data = pandas.read_csv(str(type)+"_Data/"+str(files[i]))

		Data.insert(0,"Production_Consumption",str(type),allow_duplicates=True)

		Data_Source=files[i].replace(str(type)+"_","").replace(".csv","")
		Data.insert(0, "Source", Data_Source, allow_duplicates=True)

		Data = Data.iloc[:,:-1]
		data.append(Data)

get_data("Production",Production_Files,Production_Data)
get_data("Consumption",Consumption_Files,Consumption_Data)

columns = list(Production_Data[0].columns.values)
Combined_Data = pandas.DataFrame(columns=columns)

for data in range(len(Production_Data)):
	Combined_Data=Combined_Data._append(Production_Data[data])
	Combined_Data=Combined_Data._append(Consumption_Data[data])

Combined_Data.to_csv("Combined_Data/Combined_Data.csv",index=False)

def upload_data(Upload_Data):
	table_id = "Combined_Energy_Data.Combined_Data"
	project_id="energy-449021"

	credentialsPath = "energy-449021-81f9fce32234.json"
	credentials = service_account.Credentials.from_service_account_file(credentialsPath)
	client = bigquery.Client(credentials=credentials)

	try:
		client.get_table(str(project_id)+"."+str(table_id))
		print("Table found, no changes made")

	except NotFound:
		pandas_gbq.to_gbq(Upload_Data,table_id,project_id=project_id)
		print("Table not found, created in project " +project_id)

upload_data(Combined_Data)