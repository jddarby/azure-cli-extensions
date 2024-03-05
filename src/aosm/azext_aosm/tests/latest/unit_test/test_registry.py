# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from unittest import TestCase
from unittest.mock import Mock, patch, mock_open
import logging
import sys
import json

from azext_aosm.common.registry import (
    ContainerRegistry,
    AzureContainerRegistry,
    ContainerRegistryHandler,
)


class TestRegistry(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        self.registry = ContainerRegistry(
            registry_name="registry.example.com", registry_namespace=""
        )

    def test_add_namespace(self):

        namespace_to_add = "Test_namespace"

        self.registry.add_namespace(namespace_to_add)

        assert namespace_to_add in self.registry.registry_namespaces

    def test_get_access_credentials(self):
        # Mock the docker config file
        docker_config = {
            "auths": {
                self.registry.registry_name: {
                    "auth": "dXNlcm5hbWU6cGFzc3dvcmQ="  # base64 encoded "username:password"
                }
            }
        }

        docker_config = json.dumps(docker_config)

        mocked_open = mock_open(read_data=docker_config)

        with patch("builtins.open", mocked_open):
            username, password = self.registry.get_access_credentials()

        self.assertEqual(username, "username")
        self.assertEqual(password, "password")

    def test_get_images(self):
        # Mock the get_access_credentials method
        self.registry.get_access_credentials = Mock(
            return_value=("username", "password")
        )

        # Mock the requests.get method
        mocked_response = Mock()
        mocked_response.json.return_value = {"tags": ["tag1", "tag2"]}
        mocked_get = Mock(return_value=mocked_response)

        with patch("requests.get", mocked_get):
            images = self.registry.get_images()

        registry_namespace = self.registry.registry_namespaces[0]

        self.assertEqual(len(images), 2)
        self.assertIn("tag1", images)
        self.assertIn("tag2", images)
        self.assertEqual(images["tag1"], (self.registry, registry_namespace))
        self.assertEqual(images["tag2"], (self.registry, registry_namespace))


class TestACRRegistry(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        self.registry = AzureContainerRegistry(
            registry_name="registry.azurecr.io", registry_namespace=""
        )

    def test_get_images(self):
        # Mock the _login method
        self.registry._login = Mock()

        # Mock the call_subprocess_raise_output function
        mocked_output = ["image1", "image2"]
        mocked_call_subprocess_raise_output = Mock(return_value=mocked_output)

        with patch(
            "azext_aosm.common.registry.call_subprocess_raise_output",
            mocked_call_subprocess_raise_output,
        ):
            images = self.registry.get_repositories()

        registry_namespace = self.registry.registry_namespaces[0]

        self.assertEqual(len(images), 2)
        self.assertIn("image1", images)
        self.assertIn("image2", images)
        self.assertEqual(images["image1"], (self.registry, registry_namespace))
        self.assertEqual(images["image2"], (self.registry, registry_namespace))


class TestRegistryHandler(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        self.registry_name_1 = "registry.azurecr.io"
        self.registry_name_2 = "registry.example.com/sample"
        self.registry_name_3 = "registry.example.com"

        with patch.object(
            ContainerRegistryHandler,
            "_get_images",
            return_value={
                "image1": (AzureContainerRegistry(self.registry_name_1, ""), ""),
                "image2": (ContainerRegistry(self.registry_name_2, "sample"), "sample"),
            },
        ):
            self.registry_handler = ContainerRegistryHandler(
                image_sources=[
                    self.registry_name_1,
                    self.registry_name_2,
                    self.registry_name_3,
                ]
            )

    def test_get_registry_list(self):
        registry_list = self.registry_handler.get_registry_list()

        # There are two unique registries (registry.example.com and registry.azurecr.io)
        self.assertEqual(len(registry_list), 2)

        registry_count = 0
        acr_registry_count = 0

        for registry in registry_list:
            self.assertIn(registry.registry_name, self.registry_handler.image_sources)

            if isinstance(registry, AzureContainerRegistry):
                acr_registry_count += 1
            elif isinstance(registry, ContainerRegistry):
                registry_count += 1
            else:
                self.fail("Unexpected registry type")

        self.assertEqual(registry_count, 1)
        self.assertEqual(acr_registry_count, 1)

    def test_find_registry_for_image(self):

        registry_1 = self.registry_handler.find_registry_for_image("image1")[0]

        self.assertEqual(registry_1.registry_name, self.registry_name_1)

        registry_2, namespace = self.registry_handler.find_registry_for_image("image2")

        self.assertEqual(registry_2.registry_name, self.registry_name_2)
        self.assertEqual(namespace, "sample")
