# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from unittest import TestCase
from azext_aosm.configuration_models.onboarding_sns_input_config import SiteNetworkServicePropertiesConfig, NSDVReferenceConfig
from azure.cli.core.azclierror import ValidationError

class TestSiteNetworkServicePropertiesConfig(TestCase):
    def setUp(self):
        self.nsdv_config = NSDVReferenceConfig(publisher_name="publisher", publisher_resource_group="resource_group", nsd_name="nsd", nsd_version="1.0.0")
        self.sns_config = SiteNetworkServicePropertiesConfig(location="location", operator_resource_group="resource_group", site_name="site", nsd_reference=self.nsdv_config)

    def test_validate_sns_config_all_fields_set(self):
        try:
            self.sns_config.validate()
        except ValidationError:
            self.fail("sns_config.validate() raised ValidationError unexpectedly!")

    def test_validate_sns_config_missing_field(self):
        self.sns_config.location = ""
        with self.assertRaises(ValidationError):
            self.sns_config.validate()

class TestNSDVReferenceConfig(TestCase):
    def setUp(self):
        self.nsdv_config = NSDVReferenceConfig(publisher_name="publisher", publisher_resource_group="resource_group", nsd_name="nsd", nsd_version="1.0.0")

    def test_validate_nsdv_config_all_fields_set(self):
        try:
            self.nsdv_config.validate()
        except ValidationError:
            self.fail("nsdv_config.validate() raised ValidationError unexpectedly!")

    def test_validate_nsdv_config_missing_field(self):
        self.nsdv_config.publisher_name = ""
        with self.assertRaises(ValidationError):
            self.nsdv_config.validate()