import pandas as pd
from typing import Union


class Sellout:
    instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls.instance is None:
    #         cls.instance = super().__new__(Sellout)
    #         return cls.instance
    #     return cls.instance

    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe

    # Basic methods
    def show_head(self, n_heads: int):
        return self.data.head(n_heads)

    def show_columns(self):
        return self.data.columns

    def use_column(self, columns_in: Union[list[str], str]):
        return self.data[columns_in]

    def get_unique(self, col: str):
        return self.use_column(columns_in=col).unique()

    # Dataframe filter methods
    def filter_client(self, client_name: str) -> pd.Series:
        return self.data["ChainNameEn"] == client_name

    def filter_business_unit(self, business_unit: str) -> pd.Series:
        return self.data["BusinessUnit"] == business_unit

    def filter_group_sap(self, group_sap: str) -> pd.Series:
        return self.data["GroupSapEn"] == group_sap

    # Dataframe filter apply methods
    def apply_business_unit_filter(self, business_unit: str) -> pd.DataFrame:
        return self.data[self.filter_business_unit(business_unit=business_unit)]

    def apply_client_filter(self, client_name: str) -> pd.DataFrame:
        return self.data[self.filter_client(client_name=client_name)]

    def apply_group_sap_filter(self, group_sap: str) -> pd.DataFrame:
        return self.data[self.filter_group_sap(group_sap=group_sap)]

    def apply_group_sap_client_filter(self, client_name: str, group_sap: str) -> pd.DataFrame:
        return self.data[
            (self.filter_client(client_name=client_name)) & (self.filter_group_sap(group_sap=group_sap))]

    # Dataframe aggregation methods
    def sales_by_group_sap(self, client_name: str, group_sap: str):
        dataframe = self.apply_group_sap_client_filter(client_name=client_name, group_sap=group_sap) \
            .groupby([
            "GroupSapEn",
            "GroupSapRu",
            "Date",
        ]) \
            .agg({
            "SebTotalSellout": "sum",
            "ClientTotalSellout": "sum",
            "SebOnlineSellout": "sum",
            "ClientOnlineSellout": "sum"
        })

        return dataframe
