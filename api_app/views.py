from django.contrib.auth import authenticate
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Referral, User
from .serializers import (
    LoginSerializer,
    ReferralSerializer,
    UserDetailResponseSerializer,
    UserSerializer,
)


class RootView(GenericAPIView):
    def get(self, request):
        return Response({"message": "server is running"})


class SignupView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        user = User.objects.filter(email=serializer.validated_data.get("email")).first()
        refresh = RefreshToken.for_user(user)
        if referral := serializer.validated_data.get("referral_code"):
            refrerred_user = User.objects.filter(referral_code=referral).first()
            refrerred_user.referral_points += 1
            refrerred_user.save()
            Referral(user=user, referred_by=refrerred_user).save()

        return Response(
            {"message": "success", "token": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )
        if not user:
            return Response(
                {"status": 404, "message": "user not found"}, status.HTTP_404_NOT_FOUND
            )
        refresh = RefreshToken.for_user(user)
        return Response({"message": "logged in", "token": str(refresh.access_token)})


class UserDetailsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user_details = UserDetailResponseSerializer(request.user)
        return Response(user_details.data)


class ReferralsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
            OpenApiParameter(name="limit", description="result limit", type=int),
            OpenApiParameter(name="offset", description="Page offset", type=int),
        ]
    )
    def get(self, request: Request) -> Response:
        queryset = Referral.objects.filter(referred_by=request.user).all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReferralSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        refs = ReferralSerializer(queryset, many=True)
        return Response(refs.data)
