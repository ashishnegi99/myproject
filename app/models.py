from django.db import models
from django.contrib.auth.models import User
import datetime

class Appium(models.Model):            
    name = models.CharField(max_length=30)
    details = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Appium"


class Storm(models.Model):           
    name = models.CharField(max_length=30)
    details = models.TextField(blank = True)
    date = models.DateTimeField()
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Storm"


class Revo(models.Model):           
    SuiteName = models.CharField(max_length=255)
    Test_Case = models.CharField(max_length=255)
    FileName = models.CharField(max_length=255)
    Total_Action = models.IntegerField()
    Pass = models.IntegerField()
    Fail = models.IntegerField()
    Exe_Time = models.TimeField(blank=True, null=True)
    Result = models.CharField(max_length=255)
    create_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name_plural = "Revo"


class racktestresult(models.Model):
    idTestResult = models.IntegerField()
    Date = models.DateField()
    ProjectName = models.CharField(max_length=255)
    TestJobName = models.CharField(max_length=255)
    TestJobExecutionId = models.CharField(max_length=255)
    SuiteName = models.CharField(max_length=255)
    TestCaseID = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Tester = models.CharField(max_length=255)
    BoxType = models.CharField(max_length=255)
    BoxUnitAddress = models.CharField(max_length=255)
    BoxIP = models.CharField(max_length=255)
    TotalActions = models.IntegerField()
    TotalConditions = models.IntegerField()
    PassNumbers = models.IntegerField()
    FailNumbers = models.IntegerField()
    Result = models.CharField(max_length=255)
    ExecutionTime = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Rack Test Result"


class Set_Top_Box(models.Model):           
    Device_Type = models.CharField(max_length=30)
    IP_Adress = models.CharField(max_length=30)
    Model_Name = models.CharField(max_length=30)
    Serial_Number = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Set Top Box"


class Test_Suite(models.Model):
    Test_Suite_Name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Test Suite"

    def __unicode__(self): 
            return self.Test_Suite_Name

