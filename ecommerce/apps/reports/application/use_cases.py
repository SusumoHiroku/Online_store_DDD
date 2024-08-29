from typing import List, Dict
from apps.reports.infrastructure.repositories import ReportRepository

class ReportService:
    def __init__(self):
        self.report_repo = ReportRepository()

    def get_sold_products_report(self, filters: Dict = None) -> List[Dict]:
        """
            Получает отчет по проданным товарам с возможностью фильтрации.

            :param filters: Словарь фильтров, включающий параметры для категорий и подкатегорий.
            :return: Список словарей, содержащих информацию о проданных товарах.
        """
        return self.report_repo.get_sold_products_report(filters)
