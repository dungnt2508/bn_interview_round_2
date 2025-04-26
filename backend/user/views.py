from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, ResetPasswordSerializer
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Tên người dùng'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mật khẩu'),
                'role_slug': openapi.Schema(type=openapi.TYPE_STRING, description='role slug (admin/staff/customer/có thể null)'),
            },
            required=['username', 'email', 'password'],
        ),
        responses={
            201: openapi.Response('User registered successfully', UserSerializer),
            400: 'Bad Request - Invalid data or duplicate username/email'
        }
    )
    def post(self, request):
        """Đăng ký người dùng mới và trả về JWT token."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username_or_email': openapi.Schema(type=openapi.TYPE_STRING, description='Username hoặc Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mật khẩu'),
            },
            required=['username_or_email', 'password']
        ),
        responses={
            200: openapi.Response(description="Đăng nhập thành công", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                    })
                }
            )),
            400: "Sai thông tin đăng nhập"
        }
    )
    def post(self, request):
        """Đăng nhập và trả về JWT token."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token để blacklist'),
            },
            required=['refresh'],
        ),
        responses={
            205: 'Logout successful',
            400: 'Bad Request - Invalid token'
        }
    )
    def post(self, request):
        """Đăng xuất và blacklist refresh token."""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Thay đổi mật khẩu của người dùng.",
        request_body=ResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Mật khẩu đã được cập nhật thành công.",
                examples={
                    'application/json': {
                        'detail': 'Mật khẩu đã được cập nhật.'
                    }
                }
            ),
            400: openapi.Response(
                description="Lỗi yêu cầu, ví dụ: email không tồn tại hoặc mật khẩu cũ không đúng.",
                examples={
                    'application/json': {
                        'detail': 'Mật khẩu cũ không đúng.'
                    }
                }
            )
        }
    )
    def post(self, request):
        """reset pass"""
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response(
                    {"detail": "Email không tồn tại."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.check_password(old_password):
                return Response(
                    {"detail": "Mật khẩu cũ không đúng."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Mật khẩu đã được cập nhật."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)