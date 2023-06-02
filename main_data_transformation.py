import pandas as pd

from typing import List

from kedro.config import TemplatedConfigLoader
from kedro.io import DataCatalog

def sum_sales_by(
      df: pd.DataFrame,
      group_key: List[str],
      aggregation_col: List[str]
):
  grouped_df = (df.copy()
                  .groupby(group_key, as_index=False)[aggregation_col]
                  .sum()
               )
  return grouped_df

def compute_price_by_liter(
      df: pd.DataFrame,
      price_col_name: str,
      sales_col_name: str,
      volume_col_name: str
):
  df[price_col_name] = df[sales_col_name]/df[volume_col_name]
  return df

def run_main(
        catalog: DataCatalog
):

  input_df = catalog.load("input_df")

  prices_by_liter = (input_df.copy()
      .pipe(sum_sales_by,
              group_key=['BRAND','FISCAL_YEAR'],
              aggregation_col=["VOLUME_IN_L", "NET_SALES"]
            )
      .pipe(compute_price_by_liter,
              price_col_name="PRICE_BY_LITER",
              sales_col_name="NET_SALES",
              volume_col_name="VOLUME_IN_L"
            )
  )

  catalog.save("gcp_output_df", prices_by_liter)

if __name__ == "__main__":

  conf_loader = TemplatedConfigLoader("./conf", globals_pattern="*globals.yml")
  conf_catalog = conf_loader.get("my_catalog.yml")

  catalog = DataCatalog.from_config(conf_catalog)

  run_main(
    catalog=catalog
  )