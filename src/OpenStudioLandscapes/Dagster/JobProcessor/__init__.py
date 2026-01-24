import sys
from importlib import metadata
from pathlib import Path
from dagster import get_dagster_logger

LOGGER = get_dagster_logger(__name__)

if sys.version_info[:2] >= (3, 11):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import (  # pragma: no cover
        Distribution,
        PackageNotFoundError,
        version,
    )
else:
    raise RuntimeError("Python version >= 3.11 required.")

try:
    package: Path = Path(__file__).parent
    package_namespace = package.parent
    # package = namespace.name

    namespaces = [package.name]

    while not package_namespace.name == "OpenStudioLandscapes":
        namespaces.insert(0, package_namespace.name)
        package_namespace = package_namespace.parent
    dist: Distribution = metadata.distribution(".".join(namespaces))

    __version__: str = version(dist.name)
except PackageNotFoundError:  # pragma: no cover
    LOGGER.error("Can't find metadata.distribution based on namespaces")
    __version__: str = "unknown"
finally:
    del version, PackageNotFoundError
