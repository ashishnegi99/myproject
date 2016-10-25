from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from app.models import Appium, Storm, Revo, Set_Top_Box, Test_Suite, racktestresult

admin.site.register(Appium)
admin.site.register(Storm)



# class RevoResource(resources.ModelResource):

#     class Meta:
#         model = Revo
#         import_id_fields = ('SuiteName',)
#         fields = ('SuiteName', 'Test_Case', 'FileName', 'Total_Action', 'Pass', 'Fail', 'Exe_Time', 'Result')
#         export_order = ('SuiteName', 'Test_Case', 'FileName', 'Total_Action', 'Pass', 'Fail', 'Exe_Time', 'Result')



class ResultResource(resources.ModelResource):

    class Meta:
        model = racktestresult
        import_id_fields = ('idTestResult',)
        fields = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')
        export_order = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')

class RevoAdmin(ImportExportModelAdmin):
	# pass
	# resource_class = RevoResource
	list_display = ('SuiteName', 'Test_Case', 'FileName', 'Total_Action', 'Pass', 'Fail', 'Exe_Time', 'Result')
	list_filter = ['SuiteName', 'Test_Case', 'Total_Action', 'Pass', 'Fail', 'Exe_Time', 'Result']
	search_fields = ['SuiteName', 'Test_Case', 'Total_Action', 'Pass', 'Fail', 'Exe_Time', 'Result' ]


class Set_Top_BoxAdmin(admin.ModelAdmin):
	list_display = ('Device_Type', 'IP_Adress', 'Model_Name', 'Serial_Number')


class Test_Suite_Admin(admin.ModelAdmin):
	list_display = ['Test_Suite_Name']


class racktestresultAdmin(ImportExportModelAdmin):
	pass
	resource_class = ResultResource
	list_filter = ['Date']
	list_display = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')

admin.site.register(Revo, RevoAdmin)
admin.site.register(racktestresult, racktestresultAdmin)
admin.site.register(Test_Suite, Test_Suite_Admin)
admin.site.register(Set_Top_Box, Set_Top_BoxAdmin)
