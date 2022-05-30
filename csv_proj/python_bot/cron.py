from django.core.mail import send_mail
from csv_proj.python_bot.views import Source_file
from python_bot.models import SourceFile , SecondaryFile
import pandas as pd
import csv
import re
import PyPDF2
def func():
    source_files = SourceFile.objects.all().values()
    secondary_files = SecondaryFile.objects.all().values()
    dic = {}
    source_file_list = []
    for source_file in source_files:
        source_ext = source_file['file_name'].split('.')
        source_file = './media/source_files/'+source_file['file_name']
        if source_ext[1] == 'csv':
            csv1 =  open(source_file)
            for data in csv1:
                data = data.split('\n')
                source_file_list.append(data[0])
        if source_ext[1] == 'xlsx':
            df = pd.read_excel(source_file,)
            c = df.loc[:,'Clients']
            ods={}
            for i in c:
                source_file_list.append(i)
    if len(source_file_list)> 0:
        destination_file_list = []
        for file_name in secondary_files:
            # print(file_name['secondary_file_name'])
            destination_file = './media/destination_files/'+file_name['secondary_file_name']
            dest_ext =  file_name['secondary_file_name'].split('.')
            if dest_ext[1] == 'pdf':
                pdfFileObj = open(destination_file, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                for i in range(0,pdfReader.numPages):
                    pageObj = pdfReader.getPage(i)
                    x = pageObj.extractText()
                    for j in source_file_list:
                        ss = re.search(j,x)
                        if ss:
                            # print(ss)
                            dic[j]='Found'
                            send_mail(
                            'Mail testing',
                            'Welcome to Python Bot \nClient '+j+' found in '+file_name['secondary_file_name'],
                            'mishrasomanshu@gmail.com',
                            ['mishrasomanshu@gmail.com'],
                            fail_silently=False,
                        )
        
            elif dest_ext[1]=='ods':
                l = []
                # print('in ods')
                df1 = pd.read_excel(destination_file,engine='odf')
                df1 = df1.loc[:,'Clients']
                for data in df1:
                    if data in source_file_list:
                        dic[data]='Found'
                        send_mail(
                            'Mail testing',
                            'Welcome to Python Bot \nClient '+data+' found in '+file_name['secondary_file_name'],
                            'mishrasomanshu@gmail.com',
                            ['mishrasomanshu@gmail.com'],
                            fail_silently=False,
                        )
                        
            elif dest_ext[1]=='csv':
                csv1 = open(destination_file)
                csvreader = csv.reader(csv1)
                for data in csvreader:
                    if data[0] in source_file_list:
                        dic[data[0]]='Found'
                        send_mail(
                            'Mail testing',
                            'Welcome to Python Bot \nClient '+'<strong>'+data[0]+'</strong> found in '+file_name['secondary_file_name'],
                            'mishrasomanshu@gmail.com',
                            ['mishrasomanshu@gmail.com'],
                            fail_silently=False,
                        )

def new():
    send_mail(
        'Mail testing',
        'Mail from crontab using Django',
        'mishrasomanshu@gmail.com',
        ['mishrasomanshu@gmail.com'],
        fail_silently=False,
    )


