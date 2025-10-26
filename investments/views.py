from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Investment
from .serializers import InvestmentSerializer

class InvestmentListCreateView(generics.ListCreateAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'investor':
            # Show only investor’s own investments
            return Investment.objects.filter(investor=user).order_by('-created_at')
        elif user.role == 'startup':
            # Show investments made in the startup(s) they founded
            return Investment.objects.filter(startup__founder=user).order_by('-created_at')
        else:
            return Investment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'investor':
            raise PermissionDenied("Only investors can make investments.")

        serializer.save(investor=user)
