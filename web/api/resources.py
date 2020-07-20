from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File, Activity
)

# import export csv file用的
from import_export import resources

modellist = (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File, Activity
)


class StoreResource(resources.ModelResource):
    class Meta:
        model = Store


class ActivityResource(resources.ModelResource):
    class Meta:
        model = Activity


class StoreDiscountResource(resources.ModelResource):
    class Meta:
        model = StoreDiscount
