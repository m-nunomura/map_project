from django.contrib import admin
from .models import AddressList,QuakeList,StoreList,QuakeDetail,CityList
from import_export import resources
from import_export.admin import ImportExportMixin

# Register your models here.
admin.site.register(AddressList)
admin.site.register(QuakeList)
admin.site.register(QuakeDetail)


class CityResource(resources.ModelResource):
    class Meta:
        model = CityList

@admin.register(CityList)
class CityAdmin(ImportExportMixin, admin.ModelAdmin):

    resource_class = CityResource





class StoreResource(resources.ModelResource):
    class Meta:
        model = StoreList

@admin.register(StoreList)
class StoreAdmin(ImportExportMixin, admin.ModelAdmin):

    resource_class = StoreResource
