import pkg_resources


def _get_distro_version(distribution: str) -> str:
    """
    Get the version of an installed distribution
    """
    try:
        version = pkg_resources.get_distribution(distribution).version
    except pkg_resources.DistributionNotFound:
        version = "0.0"
    return version
