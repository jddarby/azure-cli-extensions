### Prerequisites

1. `python 3.8+`


### Dev environment setup

Follow [https://github.com/Azure/azure-cli-dev-tools](https://github.com/Azure/azure-cli-dev-tools)

Clone both azure-cli and azure-cli-extensions

Note for azure-cli-extensions we are currently on a fork : https://github.com/jddarby/azure-cli-extensions
```bash
# Go into your git clone of az-cli-extensions
cd azure-cli-extensions

# Create a virtual environment to run in
python3.8 -m venv ~/.virtualenvs/az-cli-env
source ~/.virtualenvs/az-cli-env/bin/activate

# Ensure you have pip
python -m pip install -U pip

# Install azdev
pip install azdev

git checkout add-aosm-extension

# Install all the python dependencies you need
azdev setup --cli /home/developer/code/azure-cli --repo .

# Install pyYAML types
python3 -m pip install types-PyYAML

# Add the extension to your local CLI
azdev extension add aosm
```
### Generating the AOSM Python SDK
**Note:**, these instructions may become unnecessary if we can simply consume the public SDK. Right now it's not clear that will be easy, so I'm recording these steps "just in case".

We use AutoRest to generate the SDK from the API.  Docs are here: https://github.com/Azure/autorest/blob/main/docs/readme.md . You're most likely to need:

 - [Installing AutoRest](https://github.com/Azure/autorest/blob/main/docs/install/readme.md)
 - [Generating clients](https://github.com/Azure/autorest/blob/main/docs/generate/readme.md)
 - If you need to update the AOSM CLI code due to changes in the SDK, ["How do I use my client"](https://github.com/Azure/autorest/blob/main/docs/client/readme.md) might be useful, though just reading the AOSM CLI code will probably get you most of the way.

The following set up and commands were used to generate the SDK for the 2023-09-01 GA release. They are for AutoRest running on Linux. They should be simple enough to adapt if you're running on Windows.

- API repo checked out locally (in this case to /home/developer/code/azure-rest-api-specs-pr/ )
- In the API repo, the files interesting for SDK generation are the readme*.md files at /home/developer/code/azure-rest-api-specs-pr/specification/hybridnetwork/resource-manager/ :
    - Hopefully you won't need to change the main readme.md file, but it's worth checking that the default version is set to the version you're generating for. Look at the `tag` value in the `yaml` section under "Basic information", like this:
        ```yaml
        openapi-type: arm
        openapi-subtype: rpaas
        tag: package-2023-09-01
        ```
    - For 2023-09-01, the readme.python.md file looked like this:
      ```yaml $(python)
        python:
          azure-arm: true
          license-header: MICROSOFT_MIT_NO_VERSION
          namespace: Microsoft.HybridNetwork
          package-name: hybridnetwork
          clear-output-folder: true
          models-mode: msrest
          no-namespace-folders: true
          output-folder: $(python-sdks-folder)
        ```
        The most important changes made from the original file were:
         - Add `models-mode: msrest`. Without this, you don't get models. However, 'msrest' is apparently deprecated, so we should likely do some investigation into whether there's an alternative. (In Sept 2023, the information was that you need to have a TypeSpec API to get models by default - I don't know the rationale!)
         - The orginal path for `output-folder:` was `$(python-sdks-folder)/azure-mgmt/hybridnetwork`. I cut this down so I could simply provide `--python-sdks-folder=./src/aosm/azext_aosm/vendored_sdks` in the autorest command (see below), and the generated code ends up in the right place. If you'd rather move the code yourself, you can of course do so.
- `cd` into the azure-cli-extension 'root' directory (so that the python `--python-sdks-folder` used below points to the right place)
- Run the command `autorest --python --python-sdks-folder=./src/aosm/azext_aosm/vendored_sdks /home/developer/code/azure-rest-api-specs-pr/specification/hybridnetwork/resource-manager/readme.md`
- Test and fix up AOSM CLI code as necessary



### VSCode environment setup.

Make sure your VSCode is running in the same python virtual environment

### Linting and Tests

#### Style
```bash
azdev style aosm
```

Expected output:
```
===============
| Style Check |
===============

Extensions: aosm

Running pylint on extensions...
Pylint: PASSED

Running flake8 on extensions...
Flake8: PASSED
```

#### Linter
```bash
azdev linter --include-whl-extensions aosm
```

Current expected output:
```

==============
| CLI Linter |
==============

Modules: aosm

Initializing linter with command table and help files...

 Results
=========

-  pass: faulty_help_example_parameters_rule
-  pass: faulty_help_example_rule
-  pass: faulty_help_type_rule
-  pass: unrecognized_help_entry_rule
-  pass: unrecognized_help_parameter_rule
-  pass: expired_command_group
-  pass: missing_group_help
-  pass: expired_command
-  pass: missing_command_help
-  pass: no_ids_for_list_commands
-  pass: bad_short_option
-  pass: expired_option
-  pass: expired_parameter
-  pass: missing_parameter_help
-  pass: no_parameter_defaults_for_update_commands
-  pass: no_positional_parameters
-  pass: option_length_too_long
-  pass: option_should_not_contain_under_score
```

#### Typing
```bash
cd src/aosm
mypy . --ignore-missing-imports --no-namespace-packages --exclude "azext_aosm/vendored_sdks/*"
```

Expected output:
```
Success: no issues found in 33 source files
```

#### Auto-formatting
The standard Python tool, `black`, is useful for automatically formatting your code.

You can use python-static-checks in your dev environment if you want, to help you:
```bash
pip3 install -U --index-url https://pkgs.dev.azure.com/msazuredev/AzureForOperators/_packaging/python/pypi/simple/ python-static-checks==4.0.0
python-static-checks fmt
```

### Tests
The tests in this repository are split into unit tests and integration tests. Both tests live in the `tests/latest` folder and can be run using the `azdev test aosm` command (you can optionally use the `--live` flag with this command as some integration tests are run only in live mode, e.g. CNF tests). All tests are expected to pass. All unit tests and Integration tests are run as part of the pipeline.
### Unit tests
To get code coverage run:
```bash
pip install coverage
cd src/aosm
coverage erase
coverage run -m pytest .
coverage report --include="*/src/aosm/*" --omit="*/src/aosm/azext_aosm/vendored_sdks/*","*/src/aosm/azext_aosm/tests/*" -m
```

#### Integration tests
The integration tests are tests which run real azure CLI commands such as `az aosm nsd publish`. When running for the first time in a repository these tests will create a real resource group (with a randomly generated name starting with "cli_test_") in the subscription that is active on your account and deploy real AOSM resources. These resources will be cleaned up after the tests have run. After the first "live" run these tests will be automatically recorded in the `tests/latest/recordings` folder. These recordings record all communication between the CLI and Azure which mean that the next time the test is run it will no longer be run live but instead will be will be run against the recorded responses. This means that the tests will run much faster and will not create any real resources. The recording also does not rely on the knowledge of a subscription and the credentials will be removed from the recordings.

If one of the publish tests fails, then it might be because you have made small tweaks and the recording is now out of date.
Delete the relevant file under tests/latest/recordings (the file names match the name of the tests), and re-run the test.
If that passes it will create a new recording for you. Running the tests using the `--live` flag will also run all tests
in "live" mode which will create a new recording for the integration tests.

To find out more about integration tests:

- For running tests `azdev test --help` explains the options
- For writing tests, see [here](https://github.com/Azure/azure-cli/blob/dev/doc/authoring_tests.md).

### Pipelines
The pipelines for the Azure CLI run in ADO, not in github.
To trigger a pipeline you need to create a PR against main.
Until we do the initial merge to main we don't want to have a PR to main for every code review.
Instead we have a single PR for the `add-aosm-extension` branch: https://github.com/Azure/azure-cli-extensions/pull/6426
Once you have merged your changes to `add-aosm-extension` then look at the Azure Pipelines under https://github.com/Azure/azure-cli-extensions/pull/6426/checks, click on the link that says `<X> errors / <Y> warnings`.
