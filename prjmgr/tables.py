import django_tables2 as tables
from django_tables2.utils import A
from .models import Customer, Payment, Shipping, BillOfLading, Operation, Contract
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerTable(LoginRequiredMixin, tables.Table):
    name = tables.LinkColumn('customer-detail', text=lambda record: record.name, args=[A('pk')])

    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'commercial_id_number', 'phone_1', 'ceo')


class StorageBalanceTable(tables.Table):
    date = tables.DateColumn()
    amount_in = tables.Column('IN', orderable=False)
    amount_out = tables.Column('OUT', orderable=False)
    balance = tables.Column('Balance', orderable=False)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'


class PaymentTable(LoginRequiredMixin, tables.Table):
    payment_number = tables.LinkColumn('payment-detail', text=lambda record: record.payment_number, args=[A('pk')])

    class Meta:
        model = Payment
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'payment_number', 'payment_date', 'customer', 'amount', 'currency_type')


class ContractPaymentTable(PaymentTable):
    class Meta(PaymentTable.Meta):
        exclude = ('id', 'customer')


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


class ShippingDeliveryTable(tables.Table):
    date = tables.DateColumn()
    amount = tables.Column('In',orderable=False)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'

