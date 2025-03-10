from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import AutoPlate, Bid, User
from .serializers import AutoPlateSerializer, BidSerializer

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = get_object_or_404(User, username=username)
    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

class AutoPlateListCreate(generics.ListCreateAPIView):
    queryset = AutoPlate.objects.all()
    serializer_class = AutoPlateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response({"error": "Only admins can create plates."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(created_by=self.request.user)

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
