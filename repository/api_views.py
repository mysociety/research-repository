"""
Created on 27 Sep 2019

@author: Alex
"""

from django.urls import re_path
from django.utils import timezone

from rest_framework import authentication, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.models import MiniSite

from .models import ResearchItem


class FileUploadView(APIView):
    """
    Accepts zipfile for item via api
    Token authenticated
    """

    parser_classes = (FileUploadParser,)
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, item_slug, format=None):
        try:
            item = ResearchItem.objects.get(slug=item_slug)
        except ResearchItem.DoesNotExist:
            item, created = ResearchItem.objects.get_or_create(
                slug=item_slug, date=timezone.now(), published=False
            )
        file_obj = request.FILES["file"]
        print(file_obj.name)
        item.zip_archive.save(file_obj.name, file_obj)
        item.unpack_archive()
        return Response({"Message": "Upload Complete", "item_id": item.id}, status=201)


class SiteUploadView(APIView):
    """
    Accepts zipfile for item via api
    Token authenticated
    """

    parser_classes = (FileUploadParser,)
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, item_slug, preserve_existing=False, format=None):
        try:
            item = MiniSite.objects.get(slug=item_slug)
        except MiniSite.DoesNotExist:
            return Response({"Message": "Slug does not match item"}, status=400)
        file_obj = request.FILES["file"]
        print((file_obj.name))
        if preserve_existing is not False:
            preserve_existing = True
        item.zip_archive.save(file_obj.name, file_obj)
        item.unpack_archive(preserve_existing)
        return Response({"Message": "Upload Complete"}, status=201)


urlpatterns = [
    re_path(
        "^upload_zip/(?P<item_slug>[-\w]+)$",
        FileUploadView.as_view(),
        name="upload_zip",
    ),
    re_path(
        "^upload_site/(?P<item_slug>[-\w]+)/$",
        SiteUploadView.as_view(),
        name="upload_site",
    ),
    re_path(
        "^upload_site/(?P<item_slug>[-\w]+)/(?P<preserve_existing>[-\w]+)$",
        SiteUploadView.as_view(),
        name="upload_site",
    ),
]
