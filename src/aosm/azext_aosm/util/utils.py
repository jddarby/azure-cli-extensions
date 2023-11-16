# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""Utility functions."""
from typing import Any, Dict, List


def input_ack(ack: str, request_to_user: str) -> bool:
    """
    Overarching function to request, sanitise and return True if input is specified ack.

    This prints the question string and asks for user input. which is santised by
    removing all whitespaces in the string, and made lowercase. True is returned if the
    user input is equal to supplied acknowledgement string and False if anything else
    """
    unsanitised_ans = input(request_to_user)
    return str(unsanitised_ans.strip().replace(" ", "").lower()) == ack


def snake_case_to_camel_case(text):
    """Converts snake case to camel case."""
    components = text.split("_")
    return components[0] + "".join(
        x[0].upper() + x[1:] for x in components[1:]
    )


def get_cgs_dict(
    cg_schema_name: str,
    properties: Dict[str, Any],
    required: List[str]
) -> Dict[str, Any]:
    """
    Get a dictionary for the full JSON of a Config Group Schema.

    :param cg_schema_name: The title of the Config Group Schema.
    :param properties: The properties of the Config Group Schema.
    :param required: The list of required property names of the Config Group Schema.
    """
    cgs_dict: Dict[str, Any] = {
        "$schema": "https://json-schema.org/draft-07/schema#",
        "title": cg_schema_name,
        "type": "object",
        "properties": properties,
        "required": required,
    }
    return cgs_dict
