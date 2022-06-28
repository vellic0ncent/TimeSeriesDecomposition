import pandas as pd
from seasonCalculator.preparation.SelloutData import Sellout
from seasonCalculator.preparation.Database import DBConnection
from seasonCalculator.preparation.queries.sellout import SELLOUT_QUERY
from seasonCalculator.preparation.statics.localFileLoaders import save_to_csv
from seasonCalculator.processing.decomposition import Decomposer


def main():

    db = DBConnection(database_name="Stage")
    sales_data = db.load_data_by_statement(SELLOUT_QUERY)
    sellout = Sellout(sales_data)

    components_bag = []
    dynamics_bag = []

    for group_sap in sellout.get_unique("GroupSapEn"):
        for client in ["Mvideo", "Eldorado"]:
            sample = sellout.sales_by_group_sap(client_name=client, group_sap=group_sap)
            decomposer = Decomposer(dataframe=sample, freq=52)

            # Components
            try:
                components = decomposer.extract_components()
                components["client"] = client
                components["groupSap"] = group_sap
                components_bag.append(components)
            except TypeError:
                pass

            # Dynamic
            try:
                dynamic = pd.DataFrame({
                    "slope": pd.Series(data=decomposer.extract_slope()),
                    "growth_rate": pd.Series(data=decomposer.extract_growth_rate()),
                })

                dynamic["client"] = client
                dynamic["groupSap"] = group_sap
                dynamics_bag.append(dynamic)
            except TypeError:
                pass

    save_to_csv(dataframe=pd.concat(components_bag),
                result_file_name="components")
    save_to_csv(dataframe=pd.concat(dynamics_bag),
                result_file_name="dynamics_bag")

    # pd.concat(components_bag).to_excel("components.xlsx", encoding="utf-8")
    # pd.concat(dynamics_bag).to_excel("dynamics_bag.xlsx", encoding="utf-8")


if __name__ == '__main__':
    main()
