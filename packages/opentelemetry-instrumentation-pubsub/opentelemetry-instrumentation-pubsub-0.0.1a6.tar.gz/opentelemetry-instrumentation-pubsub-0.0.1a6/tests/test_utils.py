import pkg_resources

from pubsub_opentelemetry.utils import _get_distro_version


def test_get_distro_version(mocker):
    mocker.patch('pkg_resources.get_distribution')
    mock_distro = mocker.Mock()
    mock_distro.version = '1.2.3'
    pkg_resources.get_distribution.return_value = mock_distro
    version = _get_distro_version('some-package')
    assert version == '1.2.3'


def test_get_not_found_distro_version(mocker):
    mocker.patch('pkg_resources.get_distribution')
    pkg_resources.get_distribution.side_effect = pkg_resources.DistributionNotFound()
    version = _get_distro_version('some-package')
    assert version == '0.0'
