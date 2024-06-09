from django.contrib import admin
from .models import Country,DocumentSet,Customer,CustomerDocument


admin.site.register(Country)
admin.site.register(DocumentSet)
admin.site.register(Customer)
admin.site.register(CustomerDocument)
