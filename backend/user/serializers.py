from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Role
from rest_framework_simplejwt.tokens import RefreshToken

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID tự động tạo"
    )
    name = serializers.CharField(
        max_length=50,
        help_text="Tên vai trò, ví dụ: Admin, Customer, Technician, tối đa 50 ký tự"
    )
    permissions = serializers.JSONField(
        help_text="Danh sách quyền dưới dạng JSON, ví dụ: {'can_create_users': true, 'can_add_transactions': true}"
    )
    slug = serializers.CharField(
        max_length=50,
        help_text="slug tên vai trò"
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions','slug']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID tự động tạo"
    )
    username = serializers.CharField(
        max_length=50,
        help_text="Tên đăng nhập, tối đa 50 ký tự"
    )
    email = serializers.EmailField(
        max_length=100,
        help_text="Địa chỉ email, tối đa 100 ký tự"
    )
    role_name = serializers.CharField(
        source='role.name',
        read_only=True,
        allow_null=True,
        help_text="Vai trò của người dùng (Admin, Staff, Customer,v.v.), có thể để trống"
    )
    role_slug = serializers.CharField(
        source='role.slug',
        read_only=True,
        allow_null=True,
        help_text="slug vai trò của người dùng"
    )
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True,
        allow_null=True,
        help_text="ID vai trò (dùng khi tạo/cập nhật, có thể để trống)"
    )
    is_active = serializers.BooleanField(
        read_only=True,
        help_text="Trạng thái tài khoản"
    )
    date_joined = serializers.DateTimeField(
        read_only=True,
        help_text="Thời gian tạo tài khoản, định dạng ISO 8601 (ví dụ: 2025-04-14T10:00:00)"
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role_name', 'role_slug', 'role_id', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        help_text="Tên đăng nhập duy nhất, tối đa 150 ký tự"
    )
    email = serializers.EmailField(
        max_length=254,
        help_text="Địa chỉ email duy nhất, tối đa 254 ký tự"
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Mật khẩu của người dùng, tối thiểu 8 ký tự"
    )
    role_slug = serializers.SlugRelatedField(
        queryset=Role.objects.all(),
        slug_field='slug',
        required=False,
        allow_null=True,
        write_only=True,
        help_text="Slug của vai trò (Admin, Customer, Technician, v.v.), có thể để trống"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role_slug']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username đã tồn tại.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email đã tồn tại.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role_slug', None)
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        if role:
            user.role = role
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        # Kiểm tra xem người dùng nhập email hay username
        user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

        if user is None:
            raise serializers.ValidationError("Tài khoản không tồn tại")

        # Xác thực người dùng với password
        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError("Thông tin đăng nhập không đúng.")

        # Tạo token JWT cho người dùng
        refresh = RefreshToken.for_user(user)

        role = user.role

        # Trả về các token và thông tin người dùng
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                "role": {
                    "name": user.role.name,
                    "slug": user.role.slug,
                    "permissions": user.role.permissions,
                } if role else {},
            }
        }

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="Địa chỉ email của người dùng"
    )
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Mật khẩu cũ"
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Mật khẩu mới"
    )

    def validate_old_password(self, value):
        user = User.objects.filter(email=self.initial_data['email']).first()
        if user and not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không chính xác.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu mới phải dài ít nhất 8 ký tự.")
        return value