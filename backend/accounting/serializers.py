from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID tự động tạo."
    )
    reference = serializers.CharField(
        max_length=50,
        help_text="Mã tham chiếu giao dịch."
    )
    previous_balance = serializers.DecimalField(
        max_digits=12, decimal_places=2,
        read_only=True,
        help_text="Số dư trước giao dịch."
    )
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Số tiền thay đổi (+ hoặc -)."
    )
    balance = serializers.DecimalField(
        max_digits=12, decimal_places=2,
        read_only=True,
        help_text="Số dư sau giao dịch."
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Ngày giờ giao dịch."
    )

    class Meta:
        model = Transaction
        fields = ['id', 'reference', 'previous_balance', 'amount', 'balance', 'created_at']
        read_only_fields = ['id', 'previous_balance', 'balance', 'created_at']
