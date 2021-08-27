import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

#Reading excel file as input
file_name = input('Enter File Name : ')
file_name = file_name+'.xlsx'
file = pd.read_excel(file_name)


#Sequencing the file chronologically and saving it in excel
mondict = {'January':1,'Feburary':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
file = file.replace({'Month':mondict})

file['Full Date']=''

for i in range(0,len(file)):
    year = str(file['Year'][i])
    year = year.zfill(4)

    file['Full Date'][i] = year+'-'+str(file['Month'][i])+'-'+str(file['Day'][i])


for i in range(0,len(file)):    
    file['Full Date'][i] = datetime.strptime(file['Full Date'][i], '%Y-%m-%d' )

file = file.sort_values(by="Full Date")
file.pop('Full Date')
reversemonth = {1: 'January',2:'Feburary',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
file = file.replace({'Month':reversemonth})
file.to_excel(file_name,index=False)

#Iterating for each row in dataframe
for i in range(0,len(file)):
    CourtName = file['High Court'][i]
    CourtName = str(CourtName)

    
    
    
    #Creating a folder with high court name
    try: 
        os.mkdir(CourtName) 
    except FileExistsError:
        pass

    #Finding year 
    year = file['Year'][i]
    year = str(year)
    parent_dir = CourtName
    directory = year
    #Joining path for court and year to create a sub folder
    path = os.path.join(parent_dir, directory)

    #Naming a missing data file and joining the paths to create a missing data file for links that could not save data
    miss_file = 'missing_data.txt'
    miss_dir = os.path.join(parent_dir, miss_file)
    try:
        #Creating year sub folder
        os.mkdir(path) 
    except FileExistsError:
        pass

    #Creating month sub folder
    month = file['Month'][i]
    month = str(month)
    directory_2 = month
    path_2 = os.path.join(path, directory_2)
    try: 
        os.mkdir(path_2) 
    except FileExistsError:
        pass

    #Extracting url from each row
    url = file['Link'][i]
    url = str(url)
    print(url)
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    while True:
        try:
            #Visiting the required url to save data
            r = requests.get(url, headers=headers)
            break
        except(AttributeError, requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            print("Request Error, Sleeping for 5...")
            time.sleep(5)

    #Using beautiful soup to extract file title and replacing unaccepted characters in windows file name with blank spaces
    soupt = BeautifulSoup(r.content,'html.parser')
    title = soupt.title.text
    title = str(title)
    #patch added for non-ascii characters in names of files causing errors while compressing files
    #patch start
    encoded_title = title.encode("ascii","ignore")
    decoded_title = encoded_title.decode()
    title = decoded_title
    #patch end
    title = title.replace('/','')
    title = title.replace(':','')
    title = title.replace('<','')
    title = title.replace('|','')
    title = title.replace('?','')
    title = title.replace('*','')
    title = title.replace('>','')
    title = title.replace('"','')
    title = title.replace('\\','')

    
    #Joining path to save file within month folder
    save = os.path.join(path_2, title)
    save_file = save+'.html'
    
    try:
        #If same title already exists, adding an extra string to make it distinct
        if os.path.isfile(save_file):
            save_file = save+ " " + str(i) + '.html'
        #Writing content in the file
        with open(save_file,'wb') as f:
            f.write(r.content)

    #If due to some reason file could not be saved adding its detail in missing data file           
    except FileNotFoundError:
        with open(miss_dir,'a') as f2:
            f2.write(title) 
            f2.write('\n')
        pass 
        
