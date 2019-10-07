from django.db import models
from django.db.models import Sum, Count
from django.urls import reverse
import uuid  # Required for unique contract instances
from django.contrib.auth.models import User
from datetime import date
import pandas as pd
from django_pandas.io import read_frame
from django.http import HttpResponse



# Create your models here.
# class ContractInstance(models.Model):
#     """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
#
#     contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)


class Customer(models.Model):
    """Model representing a customer"""
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    commercial_id_number = models.CharField(max_length=15, null=True, blank=True)
    phone_1 = models.CharField(max_length=14, null=True, blank=True)
    phone_2 = models.CharField(max_length=14, null=True, blank=True)
    phone_3 = models.CharField(max_length=14, null=True, blank=True)
    fax = models.CharField(max_length=14, null=True, blank=True)
    ceo = models.CharField(max_length=60, null=True, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        """Returns the url to access a particular customer instance."""
        return reverse('customer-detail', args=[str(self.id)])

    def get_contracts(self):
        return self.contract_set.all()


class Currency(models.Model):
    currency_type = models.CharField(max_length=20, help_text='Which currency')

    def __str__(self):
        return self.currency_type


class Payment(models.Model):
    payment_number = models.CharField(max_length=14, null=True, blank=True)
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    currency_type = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    rate_1_usd = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.payment_number} - {self.customer.name} - ({self.amount} {self.currency_type})'

    def amountCurrency(self):
        return f'{"{0:.2f}".format(self.amount)} {self.currency_type}'

    amountCurrency.short_description = ('Amount')

    def get_absolute_url(self):
        """Returns the url to access a particular customer instance."""
        return reverse('payment-detail', args=[str(self.id)])


class Storage(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    capacity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)

    # shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.capacity}'


class Shipping(models.Model):
    trip_number = models.CharField(unique=True, max_length=11)
    VESSELS = (
        ('g', 'Geroii Rosii Pyatnitskyh'), ('a', 'Azeri Karabakh'), ('m', 'Marshal Tukhachevskiy'),
        ('d', 'Dahi ByulByul'), ('n', 'Neatis'))
    vessel_name = models.CharField(max_length=1, choices=VESSELS, null=True, blank=True)
    VESSEL_STATUS = (('ast_amr', 'Sails Astrakhan to Amirabad'), ('ast_afz', 'Sails Astrakhan to Anzali Free Zone'),
                     ('c', 'TRIP COMPLETED'))
    vessel_status = models.CharField(max_length=8, choices=VESSEL_STATUS, null=True, blank=True)
    depart_date = models.DateField(null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    contract_number = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True, blank=True)
    amount_metric_ton = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    amount_cubic_meter = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    number_of_BL = models.IntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.trip_number} - {self.get_vessel_name_display()}'


class BillOfLading(models.Model):
    BL_number = models.CharField(max_length=20, null=True, blank=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return f'{self.BL_number}'


class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    billoflading = models.ForeignKey(BillOfLading, on_delete=models.SET_NULL, null=True, blank=True)
    customs_clearance_number = models.IntegerField(null=True, blank=True)
    delivered_amount = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.shipping is None:
            return 'Unknown'
        # return f'{self.shipping.get_vessel_name_display()}'
        return f'{self.shipping.get_vessel_name_display()} {self.billoflading.BL_number} {self.customer.name}'

    def get_vessel_name(self):
        if self.shipping is None:
            return 'Unknown'
        return f'{self.shipping.get_vessel_name_display()}'

    get_vessel_name.short_description = "Vessel name"

from django_pandas.managers import DataFrameManager
class Product(models.Model):
  product_name=models.TextField()
  objects = models.Manager()
  pdobjects = DataFrameManager()  # Pandas-Enabled Manager


class Operation(models.Model):
    date = models.DateField(null=True, blank=True)
    TYPE = (('tank_in', 'IN'),('tank_out','OUT'))
    operation_type = models.CharField(max_length=8, choices=TYPE)
    amount_mt = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    amount_m3 = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    objects = models.Manager()
    pdobjects = DataFrameManager()

    # def get_context_data(self, *args, **kwargs):
    #     qs = Operation.objects.all()
    #     df = read_frame(qs)
    #     # context = {'ops': df}
    #     return HttpResponse(df.to_html())


class Contract(models.Model):
    """Model representing a contract (but not a specific contract)."""
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular contract')
    id = models.CharField(primary_key=True, max_length=12)
    initiation_date = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    contract_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    contract_amount_mt = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    # delivery_completion_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    proforma_number = models.CharField(max_length=12, null=True, blank=True)
    consignee = models.ManyToManyField('Customer', related_name='Customer', blank=True)
    # payment = models.ManyToManyField(Payment, help_text='Select payments of this contract')
    CONTRACT_STATUS = (('l', 'Lead'), ('cr', 'Compliance review'), ('n', 'Negotiation'),
                       ('p', 'Pro-Format'), ('s', 'Signed'), ('c', 'Completed'),
                       ('cl', 'Cancelled'), ('d', 'Default'), ('pc', 'Partially completed'),
                       ('a', 'Assignment'))
    status = models.CharField(max_length=2, choices=CONTRACT_STATUS, blank=True, default='I',
                              help_text='Current Status')
    EFFECTIVE_INCOTERM = (('cfr', 'CFR'), ('dap', 'DAP'), ('dat', 'DAT'), ('fob', 'FOB'))
    effective_incoterm = models.CharField(max_length=3, choices=EFFECTIVE_INCOTERM, null=True, blank=True)
    DELIVERY_PORT = (
        ('a', 'Amirabad'), ('afz', 'Anzali Free Zone'), ('s', 'Southern Ports'), ('n', 'Northern Ports'),
        ('d', 'Default'),
        ('t', 'TBD'))
    delivery_port = models.CharField(max_length=3, choices=DELIVERY_PORT, default='afz')
    PAYMENT_CONDITIONS = (('l', 'L/C'), ('t', 'T.T.'), ('b', 'L/C or T.T.'))
    payment_conditions = models.CharField(max_length=2, choices=PAYMENT_CONDITIONS, null=True, blank=True)
    PAYMENT_STATUS = (('n', 'Not paid'), ('p', 'Partial payment'),
                      ('f', 'Full payment'), ('g', 'Payment agreement'), ('d', 'Default'))
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='d')
    COMPLIANCE_REVIEW = (('n', 'NEGATIVE - NO PB'), ('p', 'POSITIVE - HIT'), ('na', 'N.A.'), ('nc', 'Not Checked'))
    compliance_review = models.CharField(max_length=2, choices=COMPLIANCE_REVIEW, default='na')
    comment = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.id

    def get_absolute_url(self):
        """Returns the url to access a detail record for this contract."""
        return reverse('contract-detail', args=[str(self.id)])

    def get_payments(self):
        sub_total = 0
        if not self.payment_set.all():
            return 'None'
        for pay_ins in self.payment_set.all():
            sub_total += pay_ins.amount
        return f'{float("{0:.2f}".format(sub_total))} {pay_ins.currency_type}'

    def get_payments_detail(self):
        payment_dict = dict()
        if not self.payment_set.all():
            return 'None'
        return self.payment_set.all()
        # for pay_ins in self.payment_set.all():
        #     payment_dict.update({pay_ins.id:pay_ins.amount})
        # return f'{float("{0:.2f}".format(sub_total))} {pay_ins.currency_type}'
    # def get_balance(self):


class Simple(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)


