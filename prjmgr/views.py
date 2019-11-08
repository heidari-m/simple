from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Contract, Customer, Payment, Currency, Shipping, BillOfLading, Operation
from django.db.models import Sum
from prjmgr import inventory
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django_pandas.io import read_frame
from django_tables2 import SingleTableView, RequestConfig, SingleTableMixin, MultiTableMixin
from .tables import CustomerTable, PaymentTable, BillOfLadingTable, ContractBillTable, OperationTable, StorageBalanceTable, \
    ContractTable, ContractPaymentTable, ContractOperationTable,ShippingTable, ShippingDeliveryTable, TmpTable  # , SimpleTable
from django.forms import ModelForm, ValidationError


# import prjmgr.inventory

# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable
    count_contracts = Contract.objects.all().count()
    total_shipment = Shipping.objects.all().aggregate(Sum('amount_metric_ton')).get('amount_metric_ton__sum') or 0
    total_delivered = Operation.objects.filter(operation_type='tank_in').aggregate(Sum('amount_mt')).get('amount_ton__sum') or 0
    context = {'count_contracts': count_contracts,
               'total_shipment': total_shipment,
               'total_delivered': total_delivered}
    return render(request, 'prjmgr/index.html', context=context)


@login_required
def contract_list(request):
    queryset = Contract.objects.all()
    table = ContractTable(queryset)
    RequestConfig(request).configure(table)
    return render(request, 'prjmgr/contract_list.html', {'table': table})


class ContractDetailView(LoginRequiredMixin,SingleTableMixin, generic.DetailView):
    model = Contract
    slug_field = 'id'
    slug_url_kwarg = 'C_No'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_qs = Payment.objects.filter(contract=self.kwargs['C_No']).values()
        context['total_payment'] = 0
        for i in payment_qs:
            context['total_payment'] += i['amount']*i['conversion_rate']
        context['sum_delivered'] = Operation.objects.filter(contract=self.kwargs['C_No'])\
            .filter(operation_type='tank_out').aggregate(Sum('amount_mt')).get('amount_mt__sum') or 0
        contract = Contract.objects.filter(id=self.kwargs['C_No']).values()
        context['delivered_value'] = context['sum_delivered'] * contract[0]['unit_price']
        context['deliverables'] = (context['total_payment']-context['delivered_value'])/contract[0]['unit_price']
        qs = Payment.objects.filter(contract=self.kwargs['C_No'])
        context['table'] = ContractPaymentTable(qs)
        qs4 = BillOfLading.objects.filter(contract=self.kwargs['C_No'])
        context['table4'] = ContractBillTable(qs4)
        return context


class ContractCreate(LoginRequiredMixin, generic.CreateView):
    model = Contract
    template_name = 'prjmgr/contract_form.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_contract'):
            return HttpResponseForbidden()
        return super(ContractCreate, self).dispatch(request, *args, **kwargs)


class ContractUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Contract
    slug_field = 'id'
    slug_url_kwarg = 'C_No'
    fields = '__all__'
    # fields = {'initiation_date', 'unit_price', 'currency', 'contract_amount_mt', 'customer', 'proforma_number',
    #           'consignee', 'status', 'effective_incoterm', 'delivery_port', 'payment_conditions', 'payment_status',
    #           'compliance_review', 'comment'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_contract'):
            return HttpResponseForbidden()
        return super(ContractUpdate, self).dispatch(request, *args, **kwargs)


class ContractDelete(LoginRequiredMixin, generic.DeleteView):
    model = Contract
    slug_field = 'id'
    slug_url_kwarg = 'C_No'
    success_url = reverse_lazy('contracts')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_contract'):
            return HttpResponseForbidden()
        return super(ContractDelete, self).dispatch(request, *args, **kwargs)


@login_required
def customer_list(request):
    queryset = Customer.objects.all()
    table = CustomerTable(queryset)
    RequestConfig(request).configure(table)
    return render(request, 'prjmgr/customer_list.html', {'table': table})


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer


class CustomerCreate(LoginRequiredMixin, generic.CreateView):
    model = Customer
    template_name = 'prjmgr/customer_form.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_customer'):
            return HttpResponseForbidden()
        return super(CustomerCreate, self).dispatch(request, *args, **kwargs)


class CustomerUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_customer'):
            return HttpResponseForbidden()
        return super(CustomerUpdate, self).dispatch(request, *args, **kwargs)


class CustomerDelete(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_customer'):
            return HttpResponseForbidden()
        return super(CustomerDelete, self).dispatch(request, *args, **kwargs)


@login_required
def payment_list(request):
    queryset = Payment.objects.all()
    table = PaymentTable(queryset)
    RequestConfig(request).configure(table)
    if not request.user.has_perm('prjmgr.delete_payment'):
        return HttpResponseForbidden()
    return render(request, 'prjmgr/payment_list.html', {'table': table})


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Payment


class PaymentCreate(LoginRequiredMixin, generic.CreateView):
    model = Payment
    template_name = 'prjmgr/payment_form.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_payment'):
            return HttpResponseForbidden()
        return super(PaymentCreate, self).dispatch(request, *args, **kwargs)


class PaymentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Payment
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_payment'):
            return HttpResponseForbidden()
        return super(PaymentUpdate, self).dispatch(request, *args, **kwargs)


class PaymentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Payment
    success_url = reverse_lazy('payments')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_payment'):
            return HttpResponseForbidden()
        return super(PaymentDelete, self).dispatch(request, *args, **kwargs)


# def BalanceStorageView(request):
#     # total_in = Shipping.objects.aggregate(sumIn=Sum('amount_metric_ton'))['sumIn']
#     # total_out = Delivery.objects.aggregate(sumOut=Sum('delivered_amount'))['sumOut']
#     # inventory.inventoryIn()
#     balance_mt = 0
#     balance_m3 = 0
#     density = 0
#     for opr in (Operation.objects.all()):
#         if opr.operation_type == 'in':
#             balance_mt += opr.amount_mt
#             balance_m3 += opr.amount_m3
#             density = balance_mt / balance_m3
#         else:
#             balance_mt -= opr.amount_mt
#             balance_m3 = (balance_mt / density)
#     context = {'balance_mt': balance_mt,
#                'balance_m3': balance_m3,
#                'density': density,
#                }
#     return render(request, 'prjmgr/tank_situation.html', context=context)
#
#
# class OperationListView(LoginRequiredMixin, generic.ListView):
#     model = Operation


@login_required()
def storage_balance_view(request):
    data = list(Operation.objects.values())
    balance = 0
    for i in data:
        if (i['operation_type'] == 'tank_in'):
            balance += i['amount_mt']
            i.update({'id': i['id'], 'amount_in': i['amount_mt'], 'balance': balance})
        else:
            balance -= i['amount_mt']
            i.update({'id': i['id'], 'amount_out': i['amount_mt'], 'balance': balance})

    # data = [{'tank_in':50},{'tank_in':70},{'tank_out':30},{'tank_in':20}]
    table = StorageBalanceTable(data)
    return render(request, 'prjmgr/operation_list.html', {'table': table})


# class OperationTableView(SingleTableView):
#     model = Operation
#     table_class = OperationTable
#     template_name = 'prjmgr/met_view.html'


class OperationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Operation


class OperationCreate(LoginRequiredMixin, generic.CreateView):
    model = Operation
    template_name = 'prjmgr/operation_form.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_operation'):
            return HttpResponseForbidden()
        return super(OperationCreate, self).dispatch(request, *args, **kwargs)


class OperationUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Operation
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_operation'):
            return HttpResponseForbidden()
        return super(OperationUpdate, self).dispatch(request, *args, **kwargs)


class OperationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Operation
    success_url = reverse_lazy('operations')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_operation'):
            return HttpResponseForbidden()
        return super(OperationDeleteView, self).dispatch(request, *args, **kwargs)


# @login_required()
# def shipping_delivery_view(request):
#     qs = list(Shipping.objects.all().values('date','amount_metric_ton').union(Delivery.objects.all().values('date','amount_metric_ton')))
#     table = ShippingDeliveryTable(qs)
#     # joined_data = dict()
#     # data = list(Shipping.objects.values())
#     # for i in data:
#     #     joined_data.update({'date': i['arrival_date'] , 'amount':i['amount_metric_ton']})
#     # table = ShippingDeliveryTable(joined_data)
#     return render(request, 'prjmgr/shipping_delivery.html', {'table': table})


@login_required()
def shipping_view(request):
    table = ShippingTable(Shipping.objects.all())
    return render(request, 'prjmgr/shipping_list.html', {'table':table})


class ShippingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Shipping
    slug_field = 'trip_number'
    slug_url_kwarg = 'tNo'


# class ShippingCreateForm(ModelForm):
#     class Meta:
#         model = Shipping
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(ShippingCreateForm, self).__init__(*args, **kwargs)
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if Shipping.objects.filter(user=self.user, title=title).exists():
#             raise ValidationError('Error messeage')
#         return title


class ShippingCreate(LoginRequiredMixin, generic.CreateView):
    model = Shipping
    template_name = 'prjmgr/shipping_form.html'
    # form_class = ShippingCreateForm
    fields = '__all__'

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def get_initial(self, *args, **kwargs):
    #     initial = super(ShippingCreate, self).get_initial(**kwargs)
    #     initial['title'] = 'My Title'
    #     return initial
    #
    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(ShippingCreate, self).get_form_kwargs(*args, **kwargs)
    #     kwargs['user'] = self.request.user
    #     return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_shipping'):
            return HttpResponseForbidden()
        return super(ShippingCreate, self).dispatch(request, *args, **kwargs)


class ShippingUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Shipping
    slug_field = 'trip_number'
    slug_url_kwarg = 'tNo'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_shipping'):
            return HttpResponseForbidden()
        return super(ShippingUpdate, self).dispatch(request, *args, **kwargs)


class ShippingDelete(LoginRequiredMixin, generic.DeleteView):
    model = Shipping
    slug_field = 'trip_number'
    slug_url_kwarg = 'tNo'
    success_url = reverse_lazy('shipments')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_shipping'):
            return HttpResponseForbidden()
        return super(ShippingDelete, self).dispatch(request, *args, **kwargs)


@login_required()
def billoflading_view(request):
    table = BillOfLadingTable(BillOfLading.objects.all())
    return render(request, 'prjmgr/billoflading_list.html', {'table':table})


class BillOfLading_detailView(LoginRequiredMixin, generic.DetailView):
    model = BillOfLading


class BillOfLadingCreate(LoginRequiredMixin, generic.CreateView):
    model = BillOfLading
    template_name = 'prjmgr/billoflading_form.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.add_billoflading'):
            return HttpResponseForbidden()
        return super(BillOfLadingCreate, self).dispatch(request, *args, **kwargs)


class BillOfLadingUpdate(LoginRequiredMixin, generic.UpdateView):
    model = BillOfLading
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.change_billoflading'):
            return HttpResponseForbidden()
        return super(BillOfLadingUpdate, self).dispatch(request, *args, **kwargs)


class BillOfLadingDelete(LoginRequiredMixin, generic.DeleteView):
    model = BillOfLading
    success_url = reverse_lazy('bls')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('prjmgr.delete_billoflading'):
            return HttpResponseForbidden()
        return super(BillOfLadingDelete, self).dispatch(request, *args, **kwargs)
