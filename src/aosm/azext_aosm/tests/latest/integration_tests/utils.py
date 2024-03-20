import unittest
from azure.cli.core.azclierror import CLIInternalError


def mock_in_unit_test(unit_test, target, replacement):

    if not isinstance(unit_test, unittest.TestCase):
        raise CLIInternalError("Patches can be only called from a unit test")

    mp = unittest.mock.patch(target, replacement)
    mp.__enter__()
    unit_test.addCleanup(mp.__exit__, None, None, None)
