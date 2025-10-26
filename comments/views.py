from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a comment to edit or delete it.
    """

    def has_object_permission(self, request,view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the comment's author
        return obj.user == request.user


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        startup_id = self.request.query_params.get('startup')
        if startup_id:
            return Comment.objects.filter(startup_id=startup_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
