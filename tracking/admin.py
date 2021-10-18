from django.contrib import admin

# Register your models here.

from tracking.models import *

admin.site.register(Customer),
admin.site.register(reports),
admin.site.register(Container),
admin.site.register(customer_container),
admin.site.register(container_item),
