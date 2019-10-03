from msilib import text

import django_tables2 as tables
from django_tables2.utils import A
from .models import Customer, Payment, Shipping, BillOfLading, Operation, Contract


class CustomerTable(tables.Table):
    name = tables.LinkColumn('customer-detail', text=lambda record: record.name, args=[A('pk')])
    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'commercial_id_number', 'phone_1', 'ceo')


class PaymentTable(tables.Table):
    payment_number = tables.LinkColumn('payment-detail', text=lambda record: record.payment_number, args=[A('pk')])
    class Meta:
        model = Payment
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id','payment_number','payment_date','customer','amount','currency_type')


class BillOfLadingTable(tables.Table):
    class Meta:
        model = BillOfLading
        template_name = 'django_tables2/bootstrap4.html'


class OperationTable(tables.Table):
    # id = tables.columns()
    class Meta:
        model = Operation
        template_name = 'django_tables2/bootstrap4.html'


class ContractTable(tables.Table):
    id = tables.LinkColumn('contract-detail', text=lambda record: record.id, args=[A('pk')])
    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'initiation_date', 'customer', 'get_payments')