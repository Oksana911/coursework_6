from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsOwner
from ads.serializers import AdSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def get_queryset(self):
        if self.action == "me":
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    @action(detail=False, methods=["GET"])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    lookup_field = 'pk'
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        self.queryset = self.queryset.filter(ad_id=self.kwargs.get('ad_pk'))
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(ad_id=self.kwargs.get("ad_pk"), author_id=self.request.user.pk)
