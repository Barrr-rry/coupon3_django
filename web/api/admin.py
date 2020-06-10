from django.contrib import admin
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)

modellist = (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
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
    cls = type(class_name, (admin.ModelAdmin,), dict(
        list_display=list_display,
    ))
    admin.site.register(md, cls)
