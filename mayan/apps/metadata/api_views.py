from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import MetadataType
from .permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)
from .serializers import (
    DocumentMetadataSerializer, DocumentTypeMetadataTypeSerializer,
    MetadataTypeSerializer
)


class APIDocumentMetadataListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of selected document's metadata types and values.
    post: Add an existing metadata type and value to the selected document.
    """
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permission_map = {
        'GET': permission_document_metadata_view,
        'POST': permission_document_metadata_add
    }
    mayan_object_permission_map = {'GET': permission_document_metadata_view}
    ordering_fields = ('id', 'metadata_type', 'value')
    serializer_class = DocumentMetadataSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.get_external_object()
        }

    def get_source_queryset(self):
        return self.get_external_object().metadata.all()

    def perform_create(self, serializer):
        if 'metadata_type_id' in serializer.validated_data:
            serializer.validated_data['metadata_type'] = serializer.validated_data['metadata_type_id']

        return super().perform_create(serializer=serializer)


class APIDocumentMetadataView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Remove this metadata entry from the selected document.
    get: Return the details of the selected document metadata type and value.
    patch: Edit the selected document metadata type and value.
    put: Edit the selected document metadata type and value.
    """
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'
    lookup_url_kwarg = 'metadata_id'
    mayan_external_object_permission_map = {
        'DELETE': permission_document_metadata_remove,
        'GET': permission_document_metadata_view,
        'PATCH': permission_document_metadata_edit,
        'PUT': permission_document_metadata_edit
    }
    mayan_object_permission_map = {
        'DELETE': permission_document_metadata_remove,
        'GET': permission_document_metadata_view,
        'PATCH': permission_document_metadata_edit,
        'PUT': permission_document_metadata_edit
    }
    serializer_class = DocumentMetadataSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_source_queryset(self):
        return self.get_external_object().metadata.all()


class APIMetadataTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the metadata types.
    post: Create a new metadata type.
    """
    mayan_object_permission_map = {'GET': permission_metadata_type_view}
    mayan_view_permission_map = {'POST': permission_metadata_type_create}
    ordering_fields = ('id', 'label', 'name')
    serializer_class = MetadataTypeSerializer
    source_queryset = MetadataType.objects.all()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected metadata type.
    get: Return the details of the selected metadata type.
    patch: Edit the selected metadata type.
    put: Edit the selected metadata type.
    """
    lookup_url_kwarg = 'metadata_type_id'
    mayan_object_permission_map = {
        'DELETE': permission_metadata_type_delete,
        'GET': permission_metadata_type_view,
        'PATCH': permission_metadata_type_edit,
        'PUT': permission_metadata_type_edit
    }
    serializer_class = MetadataTypeSerializer
    source_queryset = MetadataType.objects.all()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class MetadataTypeFilterAPIMixin:
    metadata_type_permission_map = {
        'DELETE': permission_metadata_type_edit,
        'GET': permission_metadata_type_view,
        'PATCH': permission_metadata_type_edit,
        'PUT': permission_metadata_type_edit
    }

    def get_metadata_type_queryset(self):
        permission = self.metadata_type_permission_map.get(
            self.request.method, None
        )

        queryset = MetadataType.objects.all()
        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return queryset

    def get_source_queryset(self):
        return self.get_external_object().metadata.filter(
            metadata_type__in=self.get_metadata_type_queryset()
        )


class APIDocumentTypeMetadataTypeListView(
    ExternalObjectAPIViewMixin, MetadataTypeFilterAPIMixin,
    generics.ListCreateAPIView
):
    """
    get: Returns a list of selected document type's metadata types.
    post: Add a metadata type to the selected document type.
    """
    external_object_class = DocumentType
    external_object_pk_url_kwarg = 'document_type_id'
    mayan_external_object_permission_map = {
        'GET': permission_document_type_view,
        'POST': permission_document_type_edit
    }
    serializer_class = DocumentTypeMetadataTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentTypeMetadataTypeView(
    ExternalObjectAPIViewMixin, MetadataTypeFilterAPIMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Remove a metadata type from a document type.
    get: Retrieve the details of a document type metadata type.
    patch: Edit the selected document type metadata type.
    put: Edit the selected document type metadata type.
    """
    external_object_class = DocumentType
    external_object_pk_url_kwarg = 'document_type_id'
    lookup_url_kwarg = 'metadata_type_id'
    mayan_external_object_permission_map = {
        'DELETE': permission_document_type_edit,
        'GET': permission_document_type_view,
        'PATCH': permission_document_type_edit,
        'PUT': permission_document_type_edit
    }
    serializer_class = DocumentTypeMetadataTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }
