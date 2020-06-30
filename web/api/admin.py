from django.contrib import admin
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File, Activity
)
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from api.resources import StoreResource, ActivityResource, StoreDiscountResource

modellist = (
    StoreType, County, District, DiscountType, StoreImage, File
)

for md in modellist:
    list_display = []
    for field in md._meta.get_fields():
        if isinstance(field, ForeignKey):
            list_display.append(field.attname)
        elif isinstance(field, ManyToOneRel):
            pass
        elif isinstance(field, ManyToManyRel) or isinstance(field, ManyToManyField):
            pass
        else:
            list_display.append(field.name)
    datetime_list = []
    for i in ['created_at', 'updated_at', 'deleted_at', 'created']:
        if i in list_display:
            list_display.remove(i)
            datetime_list.append(i)
    list_display += datetime_list

    class_name = f'{md.__name__}Admin'
    cls = type(class_name, (ImportExportModelAdmin, ImportExportActionModelAdmin), dict(
        list_display=list_display,
    ))
    admin.site.register(md, cls)

for md, resource in [
    (Store, StoreResource),
    (Activity, ActivityResource),
    (StoreDiscount, StoreDiscountResource),
]:
    list_display = []
    for field in md._meta.get_fields():
        if isinstance(field, ForeignKey):
            list_display.append(field.attname)
        elif isinstance(field, ManyToOneRel):
            pass
        elif isinstance(field, ManyToManyRel) or isinstance(field, ManyToManyField):
            pass
        else:
            list_display.append(field.name)
    datetime_list = []
    for i in ['created_at', 'updated_at', 'deleted_at', 'created']:
        if i in list_display:
            list_display.remove(i)
            datetime_list.append(i)
    list_display += datetime_list

    class_name = f'{md.__name__}Admin'
    cls = type(class_name, (ImportExportModelAdmin, ImportExportActionModelAdmin), dict(
        list_display=list_display,
        resource_class=resource
    ))
    admin.site.register(md, cls)
