from dagster import AssetSelection, define_asset_job

ingest_yaml_job = define_asset_job(
    name="ingest_yaml_job",
    selection=AssetSelection.all(
        include_sources=False,
    )
)
