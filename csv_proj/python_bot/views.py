from ast import Delete
from multiprocessing import context
from urllib import request, response
from django.shortcuts import redirect, render
from django.http import HttpResponse , JsonResponse
from rest_framework.views import APIView
from python_bot.models import SourceFile , SecondaryFile
from python_bot.forms import CsvModelForm , SecondaryModelForm
from python_bot.serializer import *
import pandas as pd
import csv
import re
import PyPDF2
from django.core.mail import send_mail

# Create your views here.


class Source_file(APIView):
    serializer_class = Get_Source_Data_Serializer

    def get(self,request):
        data = SourceFile.objects.all().values()
        print(data,'dada')
        s = Get_Source_Data_Serializer(data=data,many=True)
        return JsonResponse({'s':list(data)})
        # if s.is_valid():
        #     return JsonResponse({'data':s.data})
        # else:
        #     return JsonResponse({'data':s.errors})
        # datas = CsvModelForm(data)
        # for d in data:
        #     print(d)

    def post(self,request):
        source_file = request.FILES.get('source_file',None)
        file_name = request.POST['file_name']
        source_form = CsvModelForm(request.POST or None, request.FILES or None)
        if source_form.is_valid():
            source_form.save()
            print('inside')
            return JsonResponse({'form':source_form.data})
        else:
            return JsonResponse({'error Message':source_form.errors})
        # return HttpResponse('alsdhl')

    def delete(self,request):
        pass


class Compare_file(APIView):
    serializer_class = Get_Secondary_Data_Serializer

    def get(self,request):
        data = SecondaryFile.objects.all().values()
        s = Get_Secondary_Data_Serializer(data=data,many=True)
        return JsonResponse({'s':list(data)})

    def post(self,request):
        secondary_file = request.FILES.get('secondary_file',None)
        secondary_file_name = request.POST.get('secondary_file_name',None)
        s_file = SecondaryModelForm(request.POST or None ,  request.FILES or None)
        print(s_file)
        if s_file.is_valid():
            s_file.save()
            return JsonResponse({'form':s_file.data})
        else:
            return JsonResponse({'error message':s_file.errors})

        # return HttpResponse(secondary_file_name)
        
    
    def delete(self,request):
        pass


def index(request):
     data = SourceFile.objects.all().values()
     s = Get_Source_Data_Serializer(data=data,many=True)
     data1 = SecondaryFile.objects.all().values()
     s1 = Get_Secondary_Data_Serializer(data=data1,many=True)
     context = {'source_files':list(data),'destination_files':list(data1)}
     return render(request,'list.html',context)


def compare(request):
    if request.method=='POST':
        dic={}
        source = request.POST['source']
        destination = request.POST.getlist('destination',None)
        print(destination)
        source_ext = source.split('.')
        source_file = './media/source_files/'+source
        source_file_list = []
        if source_ext[1] == 'csv':
            csv1 =  open(source_file)
            # c = pd.read_excel(source_file,engine='odf')
            for data in csv1:
                data = data.split('\n')
                source_file_list.append(data[0])
        if source_ext[1] == 'xlsx':
            df = pd.read_excel(source_file,)
            c = df.loc[:,'Clients']
            # print(c)
            # dic = {}
            ods={}
            for i in c:
                source_file_list.append(i)
        for file_name in destination:
            destination_file = './media/destination_files/'+file_name
            dest_ext =  file_name.split('.')
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
                            'Welcome to Python Bot \nClient '+j+' found in '+file_name,
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
                            'Welcome to Python Bot \nClient '+data+' found in '+file_name,
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
                            'Welcome to Python Bot \nClient '+'<strong>'+data[0]+'</strong> found in '+file_name,
                            'mishrasomanshu@gmail.com',
                            ['mishrasomanshu@gmail.com'],
                            fail_silently=False,
                        )

        return redirect('/')
    else:
        return HttpResponse('wrong method')

def show_all_source_files(request):
    data = SourceFile.objects.all().values()
    # s = Get_Source_Data_Serializer(data=data,many=True)
    context = {'source_files':list(data)}
    return render(request,'all_source.html',context)

def delete_source(request):
    if request.method=='GET':
        s_file = SourceFile.objects.get(sno=request.GET['sno'])
        s_file.delete()
        return redirect('/source_list')

def show_all_destination_files(request):
    data = SecondaryFile.objects.all().values()
    context = {'destination_files':list(data)}
    return render(request,'all_destination.html',context)

def delete_destination(request):
    if request.method=='GET':
        s_file = SecondaryFile.objects.get(sno=request.GET['sno'])
        s_file.delete()
        return redirect('/destination_list')

def try_func(request):
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
            print(file_name['secondary_file_name'])
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
    return JsonResponse({'message':'Cron completed'})