from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from apps.reports.application.use_cases import ReportService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination


class ReportViewSet(viewsets.ViewSet):
    service = ReportService()

    @swagger_auto_schema(
        operation_summary="Получить отчет о проданных товарах",
        operation_description="Возвращает отчет о проданных товарах с возможностью фильтрации по категории и подкатегории. "
                              "Если фильтры не указаны, возвращает все проданные товары.",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Фильтр по категории", type=openapi.TYPE_STRING),
            openapi.Parameter('subcategory', openapi.IN_QUERY, description="Фильтр по подкатегории", type=openapi.TYPE_STRING)
        ],
        responses={
            200: 'Успешный запрос, отчет о проданных товарах.',
            400: 'Неверные параметры запроса',
        }
    )
    @action(detail=False, methods=['get'])
    def sold_products(self, request):
        filters = request.query_params.dict()
        try:
            report = self.service.get_sold_products_report(filters)
            paginator = PageNumberPagination()
            paginated_report = paginator.paginate_queryset(report, request)
            return paginator.get_paginated_response(paginated_report)
        except ValidationError:
            return Response({"detail": "Неверные параметры запроса."}, status=status.HTTP_400_BAD_REQUEST)
