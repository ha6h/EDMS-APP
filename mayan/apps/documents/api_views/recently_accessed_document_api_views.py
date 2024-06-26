from mayan.apps.rest_api import generics

from ..models.recently_accessed_document_models import RecentlyAccessedDocument
from ..permissions import permission_document_view
from ..serializers.recently_accessed_document_serializers import (
    RecentlyAccessedDocumentSerializer
)


class APIRecentlyAccessedDocumentListView(generics.ListAPIView):
    """
    get: Return a list of the recently accessed documents for the current user.
    """
    mayan_object_permission_map = {'GET': permission_document_view}
    serializer_class = RecentlyAccessedDocumentSerializer

    def get_source_queryset(self):
        return RecentlyAccessedDocument.valid.filter(user=self.request.user)
