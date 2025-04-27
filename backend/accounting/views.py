from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decimal import Decimal
from rest_framework.permissions import BasePermission, IsAdminUser
from .serializers import TransactionSerializer
from .models import Transaction
from user.models import User

class IsAdminOrHasAdminRole(BasePermission):
    """
    Custom permission
    """
    def has_permission(self, request, view):
        if request.user.is_staff or (request.user.role and request.user.role.slug == 'admin'):
            return True
        return False

class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Lấy danh sách giao dịch của user",
        responses={
            200: openapi.Response('Danh sách giao dịch của user hiện tại', TransactionSerializer(many=True))
        }
    )
    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Tạo giao dịch cho user hiện tại",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reference': openapi.Schema(type=openapi.TYPE_STRING, description='Mã tham chiếu giao dịch'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Số tiền thay đổi (+ nạp, - rút)'),
            },
            required=['reference', 'amount']
        ),
        responses={
            201: openapi.Response('Transaction created successfully', TransactionSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        user = request.user
        previous_balance = user.balance or 0
        amount = request.data.get('amount')
        reference = request.data.get('reference')

        if amount is None or reference is None:
            return Response({'detail': 'Reference và Amount là bắt buộc.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(str(amount))
        except ValueError:
            return Response({'detail': 'Amount phải là số.'}, status=status.HTTP_400_BAD_REQUEST)
        if Transaction.objects.filter(reference=reference).exists():
            raise ValidationError({'reference': 'Mã reference đã tồn tại.'})

        new_balance = previous_balance + amount
        if new_balance < 0:
            return Response({'detail': 'Số dư không đủ.'}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(
            user=user,
            reference=reference,
            previous_balance=previous_balance,
            amount=amount,
            balance=new_balance,
            user_update=request.user
        )

        user.balance = new_balance
        user.save()

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class StaffTransactionCreateView(APIView):
    permission_classes = [IsAdminOrHasAdminRole]

    @swagger_auto_schema(
        operation_summary="Tạo giao dịch cho user bất kỳ (Chỉ dành cho Admin)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'reference', 'amount'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID người dùng cần tạo giao dịch'),
                'reference': openapi.Schema(type=openapi.TYPE_STRING, description='Mã tham chiếu duy nhất'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Số tiền thay đổi (âm/dương)'),
            }
        ),
        responses={201: TransactionSerializer}
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        reference = request.data.get('reference')
        amount = request.data.get('amount')

        if not user_id or not reference or amount is None:
            return Response({'detail': 'Phải cung cấp user_id, reference, amount.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        if Transaction.objects.filter(reference=reference).exists():
            raise ValidationError({'reference': 'Reference đã tồn tại.'})

        try:
            amount = Decimal(str(amount))
        except Exception:
            return Response({'detail': 'Amount phải là số.'}, status=status.HTTP_400_BAD_REQUEST)

        previous_balance = target_user.balance or Decimal('0')
        new_balance = previous_balance + amount

        if new_balance < 0:
            return Response({'detail': 'Số dư không đủ.'}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(
            user=target_user,
            reference=reference,
            previous_balance=previous_balance,
            amount=amount,
            balance=new_balance,
            user_update=request.user
        )

        target_user.balance = new_balance
        target_user.save()

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)