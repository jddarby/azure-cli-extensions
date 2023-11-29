# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

from onboarding_nfd_base_input_config import OnboardingNFDBaseInputConfig


@dataclass
class ImageConfig:
    """Object representing an image configuration"""

    source_registry: str = field(
        metadata={
            "comment": (
                "optional. login server of the source acr registry from which to pull the image(s). "
                "For example sourceacr.azurecr.io. "
                "Leave blank if you have set source_local_docker_image."
            )
        }
    )
    source_registry_namespace: str = field(
        metadata={
            "comment": (
                "optional. namespace of the repository of the source acr registry from which to pull. "
                "For example if your repository is samples/prod/nginx then set this to samples/prod. "
                "Leave blank if the image is in the root namespace or you have set source_local_docker_image."
                "See https://learn.microsoft.com/en-us/azure/container-registry/container-registry-best-practices#repository-namespaces for further details."
            )
        }
    )
    source_local_docker_image: str = field(
        metadata={
            "comment": (
                "Optional. The image name of the source docker image from your local machine. "
                "For limited use case where the CNF only requires a single docker image "
                "that exists in the local docker repository."
            )
        }
    )


@dataclass
class HelmPackageConfig:
    """Helm package configuration."""

    nf_name: str = field(metadata={"comment": "The name of the Helm package."})
    path_to_chart: str = field(
        metadata={
            "comment": (
                "The file path of Helm Chart on the local disk. Accepts .tgz, .tar or .tar.gz. "
                "Use Linux slash (/) file separator even if running on Windows."
            )
        }
    )
    path_to_mappings: str = field(
        metadata={
            "comment": (
                "The file path (absolute or relative to input.json) of value mappings on the local disk where "
                "chosen values are replaced with deploymentParameter placeholders.\n "
                "Accepts .yaml or .yml. If left as a blank string, "
                "a value mappings file is generated with every value mapped to a deployment parameter. "
                "Use a blank string and --interactive on the build command to interactively choose which values to map."
            )
        }
    )
    # TODO: Implement split into 3 lists, if done elsewhere in code
    depends_on: list = field(
        metadata={
            "comment": (
                "Names of the Helm packages this package depends on. "
                "Leave as an empty array if there are no dependencies."
            )
        }
    )


# TODO: remove if not implementing this now, add to helmpackage config if we are
@dataclass
class DependsOnConfig:
    """Object representing a depends on object."""

    install_dependency: list = field(
        metadata={
            "comment": "List of Helm packages this package depends on for install."
        }
    )
    update_dependency: list = field(
        metadata={
            "comment": "List of Helm packages this package depends on for update."
        }
    )
    delete_dependency: list = field(
        metadata={
            "comment": "List of Helm packages this package depends on for delete."
        }
    )


@dataclass
class OnboardingCNFInputConfig(OnboardingNFDBaseInputConfig):
    """Input configuration for onboarding CNFs."""

    # Jordan: check this is never a list (90% sure)
    images: ImageConfig = field(metadata={"comment": "List of images "})
    helm_packages: [HelmPackageConfig] = field(
        metadata={"comment": "List of Helm packages to be included in the CNF."}
    )
