from django.contrib import admin

from swipe.core.models import Document,Employee, EmployeeComplete

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file_title', 'uploaded_at', 'processed')
    list_filter = ['file_title','file_from','file_to', 'uploaded_at']
    search_fields = ['file_title']
    list_per_page = 500

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'attendence_date')
    search_fields = ['employee_id','employee_name']
    list_per_page = 500

class EmpCompleteAdmin(admin.ModelAdmin):
    list_display = ('empid', 'empname', 'dat', 'tim')
    search_fields = ['empid','empname']
    list_per_page = 500

admin.site.register(Document, DocumentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeComplete, EmpCompleteAdmin)