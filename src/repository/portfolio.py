import boto3
from boto3.dynamodb.conditions import Key
from typing import List
from src.model.portfolio import Portfolio


class PortfolioRepository:
    def __init__(self, table_name: str, region_name: str):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def getPortfoliosById(self, portfolio_id: int) -> List[Portfolio]:
        """
        Fetch all portfolio items from DynamoDB for a given portfolio_id.
        """
        response = self.table.query(KeyConditionExpression=Key("id").eq(portfolio_id))
        items = response.get("Items", [])

        # 将 DynamoDB 返回的字典转换为 Pydantic 对象
        portfolios = [Portfolio(**item) for item in items]
        return portfolios

    def get_all_portfolios(self) -> List[Portfolio]:
        """
        Fetch all portfolio items from DynamoDB.
        """
        response = self.table.scan()
        items = response.get("Items", [])

        # 将 DynamoDB 返回的字典转换为 Pydantic 对象
        portfolios = [Portfolio(**item) for item in items]
        return portfolios
