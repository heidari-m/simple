from django.contrib import admin
from .models import Contract, Customer, Payment, Currency, Shipping, BillOfLading, Operation
from django.contrib.auth.models import Permission


# Register your models here.
# admin.site.register(Permission)
class ContractsInline(admin.TabularInline):
    model = Contract


class CustomerAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name',)
    # fields = ['name']
    # inlines = [ContractsInline]


admin.site.register(Customer, CustomerAdmin)


# class ContractsInstanceInline(admin.TabularInline):
#     model = ContractInstance

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiation_date', 'customer')


# @admin.register(ContractInstance)
# class ContractInstanceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'contract', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number','payment_date','customer','amountCurrency')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


# @admin.register(Delivery)
# class DeliveryAdmin(admin.ModelAdmin):
#     list_display = ('billoflading','get_vessel_name','customer','amount_metric_ton')

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    pass

@admin.register(BillOfLading)
class BillOfLadingAdmin(admin.ModelAdmin):
    pass


# @admin.register(Storage)
# class StorageAdmin(admin.ModelAdmin):
#     pass


# @admin.register(BalanceStorage)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('remaining',)
#     # pass

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    pass
