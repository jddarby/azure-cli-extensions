# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements


def load_command_table(self, _):  # pylint: disable=unused-argument
    with self.command_group('quota'):
        from azext_quota.custom import QuotaCreate, QuotaUpdate
        self.command_table['quota create'] = QuotaCreate(loader=self)
        self.command_table['quota update'] = QuotaUpdate(loader=self)
