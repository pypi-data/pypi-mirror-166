# Imports from newer versions are protected by try/except,
# so they don't break legacy versions of dbt-bigquery adapter.
try:
    from dbt.adapters.bigquery.column import BigQueryColumn  # noqa
except Exception as e:
    print("Running legacy version some imports were skipped.")

from dbt.adapters.base import AdapterPlugin  # noqa
from dbt.adapters.bigquery.connections import BigQueryConnectionManager  # noqa
from dbt.adapters.bigquery.connections import BigQueryCredentials  # noqa
from dbt.adapters.bigquery.impl import BigQueryAdapter, GrantTarget  # noqa
from dbt.adapters.bigquery.relation import BigQueryRelation  # noqa
from dbt.include import bigquery

from alvin_integration.producers.dbt.lineage.backend import AlvinBigQueryAdapter

Plugin = AdapterPlugin(
    adapter=AlvinBigQueryAdapter,
    credentials=BigQueryCredentials,
    include_path=bigquery.PACKAGE_PATH,
)

