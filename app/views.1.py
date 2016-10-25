# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.forms import UserForm, NameForm
from app.models import Storm, Appium, Revo, Set_Top_Box, racktestresult
from django.contrib.auth.decorators import login_required
import jenkins
import urllib2
import urllib
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
import socket
import time
import string
import re
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
import os
import io
import csv
import json
from chartit import DataPool, Chart
from chartit.chartdata import DataPool
import json as simplejson
from chartit import DataPool, Chart
from django.db.models import Avg
from chartit import PivotDataPool, PivotChart
import datetime



def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/layout.html",
        RequestContext(request,
        {
            "title":"Home Page",
        })
    )

#################
## Revo Views ##
#################
def Revo_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
    else:
        form = NameForm()
    print request.POST.getlist('checks')
    print request.POST.getlist('optradio')

    form = NameForm(request.POST)
    stb1 = request.POST.getlist('optradio')
    list1 = request.POST.getlist('checks')
    cd1 = "<command>"
    cd2 = "</command>"
    test_runner_path2 = "cd C:\git_new\evo_automation\ tests\TestRunner"
    # request.POST.getlist('check1')

    STB = ', '.join(stb1)

    TestSuite = ', '.join(list1)
    # TestSuite1 = "REG_AGREED_SUITE02"
    report_location = "C:\git_new\evo_automation\ tests\TestRunner\ReportFile C:\git_new\evo_automation\ reports"
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')

    # mycommand1 = cd1 + test_runner_path + "\n" + STB + "\n" + TestSuite1 + "\nTrue \n" + report_location + cd2
    mycommand2 = cd1 + test_runner_path2 + "\n" + STB + "\n" + TestSuite + "\nTrue \n" + report_location + cd2
    mycommand3 = cd1 + "super" + cd2
    # print "mycommand1",mycommand1

    print "mycommand2",mycommand2

    jobConfig = j.get_job_config('sample')

    tree = ET.XML(jobConfig)
    with open("temp.xml", "w") as f:
        f.write(ET.tostring(tree))

    document = parse('temp.xml')
    actors = document.getElementsByTagName("command")

    for act in actors:
        for node in act.childNodes:
            if node.nodeType == node.TEXT_NODE:
                r = "{}".format(node.data)

    prev_command = cd1 + r + cd2


    shellCommand = jobConfig.replace(prev_command, mycommand2)
    j.reconfig_job('sample', shellCommand)


    j.build_job('sample')

    return render(request, 'app/layout.html', {'form': form})



def GetSerialNum(request):
    if request.method == 'GET':

        print 'calling SETTOPBOX function'
        i = 0

        msg = \
            'M-SEARCH * HTTP/1.1\r\n' \
            'HOST:239.255.255.250:1900\r\n' \
            'MX:2\r\n' \
            'MAN:ssdp:discover\r\n' \
            'ST:urn:schemas-upnp-org:device:ManageableDevice:2\r\n'

        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(5)
        s.sendto(msg, ('239.255.255.250', 1900))

        try:
            os.remove('serialnumbers.txt')
        except OSError:
            pass

        def logToFile(logTxt):
            logFile = open("serialnumbers.txt", "a+")
            logFile.write(logTxt + "\n")
            # print logTxt

        count = 0
        try:
            while True:
                count = count + 1
                data, addr = s.recvfrom(65507)

                mylist = data.split('\r')
                url = re.findall('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
                print url[0]
                response = urllib2.urlopen(url[0])
                the_page = response.read()

                tree = ET.XML(the_page)
                with open("temp.xml", "w") as f:
                    f.write(ET.tostring(tree))

                document = parse('temp.xml')
                actors = document.getElementsByTagName("ns0:serialNumber")
                for act in actors:
                    for node in act.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            r = "{}".format(node.data)
                            print r
                            logToFile(str(r))
                            i += 1
                            print i

        except socket.timeout:
            pass

        f = open("Reference_File.txt", "r")
        reader = csv.reader(f)

        data = open("temp1.csv", "wb")
        w = csv.writer(data)
        for row in reader:
            my_row = []
            my_row.append(row[0])
            w.writerow(my_row)
        data.close()

        with io.open('temp1.csv', 'r') as file1:
            with io.open('serialnumbers.txt', 'r') as file2:
                same = set(file1).intersection(file2)
                print same

        with open('results.csv', 'w') as file_out:
            for line in same:
                file_out.write(line)
                print line

        with open('results.csv', 'rb') as f:
            reader = csv.reader(f)
            result_list = []
            for row in reader:
                result_list.extend(row)

        with open('Reference_File.txt', 'rb') as f:
            reader = csv.reader(f)
            sample_list = []
            for row in reader:
                if row[0] in result_list:
                    sample_list.append(row + [1])
                else:
                    sample_list.append(row + [0])

        with open('sample_output.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(sample_list)
            print

        f = open('sample_output.csv', 'r')
        jsonfile = open('app/templates/app/temp1.json', 'w')
        reader = csv.DictReader(f, fieldnames=("STBSno", "STBLabel", "RouterSNo", "STBStatus"))
        out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
        jsonfile.write(out)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/layout.html",
        RequestContext(request,
        {
            "title":"Revo",
            "message":"Stuff about revo goes here.",
            "year":datetime.now().year,
        })
    )


@login_required
def Storm(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/layout.html",
        RequestContext(request,
        {
            "title":"Storm",
            "message":"Stuff about Storm goes here",
            "year":datetime.now().year,
        })
    )

#################
## Appium Views ##
#################
def Appium(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/layout.html",
        RequestContext(request,
        {
            "title":"Appium",
            "message":"Stuff about Appium goes here.",
            "year":datetime.now().year,
        })
    )

##################
## Graphs Views ##
##################
def reports_chart_view(request):
    error = False
    print "hello1"
    if 'q1' and 'q2'in request.GET:
        print "hello2"
        q1 = request.GET['q1']
        q2 = request.GET['q2']
        date_from = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        print date_from
        date_to = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')
        print date_to
        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            date_from = datetime.date(2016, 9, 21)
            date_to = datetime.date(2016, 9, 23)
            print "STATIC DATE FROM", date_from
            print "STATIC DATE TO",date_to
    date_from = datetime.date(2016, 9, 21)
    date_to = datetime.date(2016, 9, 21)
    #Column Chart 1   
    ds = DataPool(
       series=
        [{'options': {
            'source': racktestresult.objects.filter(Date__range = ('2016-09-21','2016-09-26'))},
          'terms': [
            'TotalConditions',
            'BoxType',
            'Result',
            'PassNumbers',
            'idTestResult',
            'ExecutionTime',
            'TestCaseID', 
            'FailNumbers']}
         ])

    cht= Chart(
        datasource = ds, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': True},
            'terms':{
              'TestCaseID': [
                'PassNumbers',
                'FailNumbers']
              }}],
        chart_options = 
          {'title': {
               'text': 'Test Cases (Pass/Fail)'},
           'xAxis': {
                'title': {
                   'text': 'Test Case Name'}}})

    
    #Column Chart 2
    ds1 = DataPool(
       series=
        [{'options': {
            'source': racktestresult.objects.filter(Date__range = (date_from, date_from))},
          'terms': [
            'TotalConditions',
            'BoxType',
            'Result',
            'PassNumbers',
            'idTestResult',
            'ExecutionTime',
            'TestCaseID', 
            'FailNumbers']}
         ])

    cht2= Chart(
        datasource = ds1, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': True},
            'terms':{
              'TestCaseID': [
                'ExecutionTime']
              }}],
        chart_options = 
          {'title': {
               'text': 'Test Execution Time'},
           'xAxis': {
                'title': {
                   'text': 'Test Case Name'}}})

    #Pie Chart
    revodata = DataPool(
       series=
        [{'options': {
            'source': racktestresult.objects.filter(Date__range=(date_from, date_to))},
          'terms': [
            'TotalConditions',
            'Date',
            'Author',
            'Result',
            'BoxType',
            'PassNumbers',
            'TestCaseID',
            'idTestResult',
            'ExecutionTime',
            'ProjectName',
            'SuiteName',
            'FailNumbers']}
         ])

    cht3 = Chart(
            datasource = revodata, 
            series_options = 
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                  'SuiteName': [
                    'FailNumbers',]
                  }}],
            chart_options = 
              {'title': {
               'text': 'Test Suite Failures'},
                   })

    return render(
        request,
        "app/reports.html",
        {
        'revochart': [cht, cht2, cht3],
        }
    )



# def search(request):
#     error = False
#     if 'q1' and 'q2'in request.GET:
#         q1 = request.GET['q1']
#         q2 = request.GET['q2']
#         if not q1:
#             error = True
#         elif not q2:
#             error = True
#         else:
#             books = racktestresult.objects.filter(Date__range=(q1,q2))
#             return render(request, 'app/reports.html',
#                 {'books': books })
#     return render(request, 'app/reports.html', {'error': error})


def Json(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        #"app/STBSampleJson.json",
        "app/temp1.json",
        RequestContext(request,
        {

        })
    )


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            pass
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
            'app/user/register_form.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)