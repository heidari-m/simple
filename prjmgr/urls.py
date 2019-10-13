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
               # path('storage/', views.BalanceStorageView, name='storage'),

               # path('operations/', views.OperationListView.as_view(), name='operations'),
               path('operations/', views.storage_balance_view, name='operations'),
               path('operation/<int:pk>', views.OperationDetailView.as_view(), name='operation-detail'),
               path('operation/create/', views.OperationCreate.as_view(), name='operation_create'),
               path('operation/<int:pk>/update/', views.OperationUpdate.as_view(), name='operation_update'),
               path('operation/<int:pk>/delete/', views.OperationDeleteView.as_view(), name='operation_delete'),

               path('shipments/', views.shipping_view, name='shipments'),
               path('shipment/<slug:tNo>', views.ShippingDetailView.as_view(), name='shipping-detail'),
               path('shipment/create/', views.ShippingCreate.as_view(), name='shipping_create'),
               path('shipment/<slug:tNo>/update/', views.ShippingUpdate.as_view(), name='shipping_update'),
               path('shipment/<slug:tNo>/delete/', views.ShippingDelete.as_view(), name='shipping_delete'),

               path('bls/', views.billoflading_view, name='bls'),
               path('bl/<int:pk>', views.BillOfLading_detailView.as_view(), name='bls-detail'),
               path('bl/create', views.BillOfLadingCreate.as_view(), name='bl_create'),
               path('bl/<int:pk>/update', views.BillOfLadingUpdate.as_view(), name='bl_update'),
               path('bl/<int:pk>/delete', views.BillOfLadingDelete.as_view(), name='bl_delete'),
               # path('mets/', views.operation_view, name='operation_view'),
               # path('mets/', views.OperationTableView.as_view(), name='met-view'),
               # path('dev/', views.delivery_vs_payment, name='dev-view'),
               # path('simpl/', views.simple_list, name='simpl'),

               # path('shipdelivery/', views.shipping_delivery_view, name='shipping-delivery'),

               ]
