from django.urls import path
from .views import TransactionListCreateView, StaffTransactionCreateView

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('staff/transactions/', StaffTransactionCreateView.as_view(), name='staff-transaction-create'),
]
