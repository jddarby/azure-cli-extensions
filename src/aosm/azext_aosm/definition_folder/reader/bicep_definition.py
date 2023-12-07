# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
from azure.cli.core.commands import LongRunningOperation
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentExtended
from pathlib import Path

from azext_aosm.common.utils import convert_bicep_to_arm
from azext_aosm.definition_folder.reader.base_definition import BaseDefinitionElement


class BicepDefinitionElement(BaseDefinitionElement):
    """ Bicep definition """

    def __init__(self, path: Path, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)

    def deploy(self, resource_client: ResourceManagementClient):
        """Deploy the element."""
        arm_json = convert_bicep_to_arm(self.path / "deploy.bicep")
        self._validate_and_deploy_arm_template(
            template=arm_json,
            # TODO: Create/store parameters somewhere? also pass in resource group
            parameters={},
            resource_group="",
            resource_client=resource_client,
        )

    def delete(self, resource_client: ResourceManagementClient):
        """Delete the element."""
        # TODO: Delete resources by Bicep or ARM template.
        # The ResourceManagementClient doesn't just do it, so we may need to parse the
        # template for resources and delete them individually.
        pass

    def _validate_and_deploy_arm_template(
        self, template: any, parameters: dict[any, any], resource_group: str, resource_client: ResourceManagementClient
    ) -> any:
        """
        Validate and deploy an individual ARM template.

        This ARM template will be created in the resource group passed in.

        :param template: The JSON contents of the template to deploy
        :param parameters: The JSON contents of the parameters file
        :param resource_group: The name of the resource group that has been deployed

        :return: Output dictionary from the bicep template.
        :raise RuntimeError if validation or deploy fails
        """
        # Get current time from the time module and remove all digits after the decimal
        # point
        current_time = str(time.time()).split(".", maxsplit=1)[0]

        # Add a timestamp to the deployment name to ensure it is unique
        deployment_name = f"AOSM_CLI_deployment_{current_time}"

        # Validation is automatically re-attempted in live runs, but not in test
        # playback, causing them to fail. This explicitly re-attempts validation to
        # ensure the tests pass
        validation_res = None
        for validation_attempt in range(2):
            try:
                validation = (
                    resource_client.deployments.begin_validate(
                        resource_group_name=resource_group,
                        deployment_name=deployment_name,
                        parameters={
                            "properties": {
                                "mode": "Incremental",
                                "template": template,
                                "parameters": parameters,
                            }
                        },
                    )
                )
                validation_res = LongRunningOperation(
                    self.cli_ctx, "Validating ARM template..."
                )(validation)
                break
            except Exception:  # pylint: disable=broad-except
                if validation_attempt == 1:
                    raise

        if not validation_res or validation_res.error:
            raise RuntimeError(f"Validation of template {template} failed.")

        # Validation succeeded so proceed with deployment
        poller = resource_client.deployments.begin_create_or_update(
            resource_group_name=resource_group,
            deployment_name=deployment_name,
            parameters={
                "properties": {
                    "mode": "Incremental",
                    "template": template,
                    "parameters": parameters,
                }
            },
        )

        # Wait for the deployment to complete and get the outputs
        deployment: DeploymentExtended = LongRunningOperation(
            self.cli_ctx, "Deploying ARM template"
        )(poller)

        if deployment.properties is not None:
            depl_props = deployment.properties
        else:
            raise RuntimeError("The deployment has no properties.\nAborting")

        if depl_props.provisioning_state != "Succeeded":
            raise RuntimeError(
                "Deploy of template to resource group"
                f" {resource_group} proceeded but the provisioning"
                f" state returned is {depl_props.provisioning_state}."
                "\nAborting"
            )

        return depl_props.outputs
