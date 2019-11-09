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
    id = tables.Column(linkify=('operation-detail', {'pk': tables.A('id')}))
    date = tables.DateColumn()
    # id = tables.LinkColumn('operation-detail', text=lambda record: record.id, args=[A('pk')])
    amount_in = tables.Column('IN', orderable=False)
    amount_out = tables.Column('OUT', orderable=False)
    balance = tables.Column('Balance', orderable=False)
    contract = tables.Column('Contract No', orderable=False)

    class Meta:
        # model = Operation
        template_name = 'django_tables2/bootstrap4.html'


class SummingColumn(tables.Column):

    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class PaymentTable(LoginRequiredMixin, tables.Table):
    payment_number = tables.LinkColumn('payment-detail', text=lambda record: record.payment_number, args=[A('pk')])
    amount_USD = SummingColumn()

    class Meta:
        model = Payment
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'payment_number', 'payment_date', 'customer', 'amount', 'currency','amount_USD')


class ContractPaymentTable(PaymentTable):
    amount_USD = SummingColumn()

    class Meta(PaymentTable.Meta):
        exclude = ('id', 'customer')


class BillOfLadingTable(tables.Table):
    id = tables.Column(linkify=('bl-detail', {'pk': tables.A('id')}))
    amount = SummingColumn()
    class Meta:
        model = BillOfLading
        template_name = 'django_tables2/bootstrap4.html'


class ContractBillTable(BillOfLadingTable):

    class Meta(BillOfLadingTable.Meta):
        exclude = ('contract',)


class OperationTable(tables.Table):
    # id = tables.columns()
    class Meta:
        model = Operation
        template_name = 'django_tables2/bootstrap4.html'


class StorageTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'


class ContractOperationTable(OperationTable):
    class Meta(OperationTable.Meta):
        exclude = ('id','customer','contract','customs_clearance_number','operation_type','amount_m3')


class TmpTable(tables.Table):
    # date = tables.DateColumn()
    # shipping = tables.Column()
    customs_clearance_number = tables.Column()
    amount_mt__sum = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'


class ContractTable(tables.Table):
    id = tables.LinkColumn('contract-detail', text=lambda record: record.id, args=[A('pk')])
    get_payments = tables.Column(verbose_name='Payment')

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'initiation_date', 'customer', 'get_payments')


class ShippingTable(tables.Table):
    # id = tables.LinkColumn('shipment-detail', text=lambda record: record.id, args=[A('pk')])
    trip_number = tables.LinkColumn('shipping-detail', text=lambda record: record.trip_number, args=[A('pk')])

    class Meta:
        model = Shipping
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('trip_number','date','vessel_name','contract_number','amount_metric_ton','number_of_BL')


class ShippingDeliveryTable(tables.Table):
    date = tables.DateColumn()
    amount_metric_ton = tables.Column('amount_metric_ton',orderable=False)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'

