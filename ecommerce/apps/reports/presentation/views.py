from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.reports.application.use_cases import ReportService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReportViewSet(viewsets.ViewSet):
    service = ReportService()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category", type=openapi.TYPE_STRING),
            openapi.Parameter('subcategory', openapi.IN_QUERY, description="Filter by subcategory", type=openapi.TYPE_STRING)
        ]
    )
    @action(detail=False, methods=['get'])
    def sold_products(self, request):
        filters = request.query_params.dict()
        report = self.service.get_sold_products_report(filters)
        return Response(report, status=status.HTTP_200_OK)
