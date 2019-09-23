from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Contract, Customer, Payment, Currency, Delivery, Shipping, BillOfLading, Storage, \
    Operation  # , BalanceStorage
from django.db.models import Sum
from prjmgr import inventory
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden


# import prjmgr.inventory

# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    context = {'text': 'Simple contract manager', }
    return render(request, 'prjmgr/index.html', context=context)


class ContractListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Contract
    paginate_by = 10


class ContractDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contract
    slug_field = 'id'
    slug_url_kwarg = 'C_No'


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
    fields = {'initiation_date','unit_price','contract_currency','contract_amount_mt','customer','proforma_number','consignee','status','effective_incoterm','delivery_port','payment_conditions','payment_status','compliance_review','comment'}

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


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer


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


class PaymentListView(LoginRequiredMixin, generic.ListView):
    model = Payment


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


def BalanceStorageView(request):
    # total_in = Shipping.objects.aggregate(sumIn=Sum('amount_metric_ton'))['sumIn']
    # total_out = Delivery.objects.aggregate(sumOut=Sum('delivered_amount'))['sumOut']
    # inventory.inventoryIn()
    balance_mt = 0
    balance_m3 = 0
    density = 0
    for opr in (Operation.objects.all()):
        if opr.operation_type == 'in':
            balance_mt += opr.amount_mt
            balance_m3 += opr.amount_m3
            density = balance_mt / balance_m3
        else:
            balance_mt -= opr.amount_mt
            balance_m3 = (balance_mt / density)
    context = {'balance_mt': balance_mt,
               'balance_m3': balance_m3,
               'density': density,
               }
    return render(request, 'prjmgr/tank_situation.html', context=context)


class OperationListView(LoginRequiredMixin, generic.ListView):
    model = Operation


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
