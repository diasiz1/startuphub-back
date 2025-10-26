from rest_framework import viewsets, permissions, filters
from .models import Startup
from .serializers import StartupSerializer
from rest_framework.exceptions import PermissionDenied

class IsFounderOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for founder
        return obj.founder == request.user

class StartupViewSet(viewsets.ModelViewSet):
    queryset = Startup.objects.all().order_by('-created_at')
    serializer_class = StartupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsFounderOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category', 'description']

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'startup':
            raise PermissionDenied("Only users with the 'startup' role can create a startup.")
        serializer.save(founder=self.request.user)
