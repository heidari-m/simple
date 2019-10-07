from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
               path('contracts/', views.contract_list, name='contracts'),
               path('contract/<slug:C_No>', views.ContractDetailView.as_view(), name='contract-detail'),
               # path('contract2/<slug:C_Do>', views.ContractDetailView2.as_view(), name='contract-detail2'),
               path('contract/create/', views.ContractCreate.as_view(), name='contract_create'),
               path('contract/<slug:C_No>/update/', views.ContractUpdate.as_view(), name='contract_update'),
               path('contract/<slug:C_No>/delete/', views.ContractDelete.as_view(), name='contract_delete'),

               path('customers/', views.customer_list, name='customers'),
               path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
               path('customer/create/', views.CustomerCreate.as_view(), name='customer_create'),
               path('customer/<int:pk>/update/', views.CustomerUpdate.as_view(), name='customer_update'),
               path('customer/<int:pk>/delete/', views.CustomerDelete.as_view(), name='customer_delete'),

               path('payments/', views.payment_list, name='payments'),
               path('payment/<int:pk>', views.PaymentDetailView.as_view(), name='payment-detail'),
               path('payment/create/', views.PaymentCreate.as_view(), name='payment_create'),
               path('payment/<int:pk>/update/', views.PaymentUpdate.as_view(), name='payment_update'),
               path('payment/<int:pk>/delete/', views.PaymentDelete.as_view(), name='payment_delete'),
               # path('balances/', views.BalanceStorageView.as_view(), name='balances'),
               path('storage/', views.BalanceStorageView, name='storage'),

               # path('operations/', views.OperationListView.as_view(), name='operations'),
               path('operations/', views.storage_balance_view, name='operations'),
               path('operation/<int:pk>', views.OperationDetailView.as_view(), name='operation-detail'),
               path('operation/create/', views.OperationCreate.as_view(), name='operation_create'),
               path('operation/<int:pk>/update/', views.OperationUpdate.as_view(), name='operation_update'),
               path('operation/<int:pk>/delete/', views.OperationDeleteView.as_view(), name='operation_delete'),

               # path('mets/', views.operation_view, name='operation_view'),
               path('mets/', views.OperationTableView.as_view(), name='met-view'),
               # path('dev/', views.delivery_vs_payment, name='dev-view'),
               # path('simpl/', views.simple_list, name='simpl'),
               ]
