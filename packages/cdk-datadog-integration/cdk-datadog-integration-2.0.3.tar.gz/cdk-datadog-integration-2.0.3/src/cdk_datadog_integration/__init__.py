'''
# AWS Cloud Development Kit (CDK) Datadog Integration

This construct makes it easy to integrate your AWS account with Datadog. It
creates nested stacks based on the official
[Datadog Cloudformation templates](https://github.com/DataDog/cloudformation-template/blob/master/aws/main.yaml)
using [Amazon Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/).

## Basic Usage

1. Install the package

   ```console
   npm i --save cdk-datadog-integration
   ```

   Or via [pypi](https://pypi.org/project/cdk-datadog-integration/),
   [NuGet](https://www.nuget.org/packages/BenLimmer.CdkDatadogIntegration/), or
   [GitHub Packages](https://github.com/blimmer/cdk-datadog-integration/packages).
2. Import the stack and pass the required parameters.

   ```python
   import * as cdk from "aws-cdk-lib";
   import { MonitoringInfrastructureStack } from "../lib/monitoring-infrastructure-stack";

   const app = new cdk.App();
   new MonitoringInfrastructureStack(app, "MonitoringInfrastructure");
   ```

   ```python
   import * as cdk from "aws-cdk-lib";
   import * as secrets from "aws-cdk-lib/aws-secretsmanager";
   import { DatadogIntegrationStack } from "cdk-datadog-integration";

   export class MonitoringInfrastructureStack extends cdk.Stack {
     constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
       super(scope, id, props);

       const datadog = new DatadogIntegrationStack(this, "Datadog", {
         // Generate an ID here: https://app.datadoghq.com/account/settings#integrations/amazon-web-services
         externalId: "",

         // Create or lookup a `Secret` that contains your Datadog API Key
         // See https://docs.aws.amazon.com/cdk/api/latest/docs/aws-secretsmanager-readme.html for details on Secrets in CDK
         // Get your API key here: https://app.datadoghq.com/account/settings#api
         apiKey: secrets.Secret.fromSecretNameV2(
           this,
           "DatadogApiKey",
           "<your secret name>"
         ),
       });
     }
   }
   ```

## Configuration

Use `DatadogIntegrationConfig` to set additional configuration parameters. Check
out
[docs](/API.md#cdk-datadog-integration.DatadogIntegrationConfig)
for more details on what's available.

Additionally, a CDK `Construct` is exposed, should you want to add additional
customizations vs. using the out-of-the-box `Stack`.

## CDK Version Compatibility

This package is expected to work with all recent versions of CDK v2. It has been
tested with 2.1.0 so almost certainly works will all newer versions, and
probably works with some older versions too, but is untested.

If you're still on CDK v1, you can use `cdk-datadog-integration@1`, but this
version is unmaintained. Please upgrade to CDKv2.

## How it Works

This module uses the
[`CfnStack` CDK Construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudformation.CfnStack.html)
to import the three CloudFormation stacks referenced by the
[main Datadog CloudFormation template](https://github.com/DataDog/cloudformation-template/tree/master/aws).
By referencing the Datadog-provided templates, you can be confident that the
integration works exactly as Datadog intends.

## Author

This package is created and maintained by
[Ben Limmer](https://www.linkedin.com/in/blimmer/), a
[freelance architect and consultant](https://benlimmer.com/freelance/). I love
helping businesses of all sizes solve their hardest technology problems. Let's
[connect](https://benlimmer.com/freelance/contact/) if I can be of help!

## Contributing

PRs are welcome!

### Releasing

To release, merge your PR to `main`.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import constructs


class DatadogIntegration(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-datadog-integration.DatadogIntegration",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_key: aws_cdk.aws_secretsmanager.ISecret,
        external_id: builtins.str,
        additional_forwarder_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        additional_integration_role_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_trails: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        forwarder_name: typing.Optional[builtins.str] = None,
        forwarder_version: typing.Optional[builtins.str] = None,
        iam_role_name: typing.Optional[builtins.str] = None,
        install_datadog_policy_macro: typing.Optional[builtins.bool] = None,
        log_archives: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        permissions: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        '''
        props = DatadogIntegrationConfig(
            api_key=api_key,
            external_id=external_id,
            additional_forwarder_params=additional_forwarder_params,
            additional_integration_role_params=additional_integration_role_params,
            cloud_trails=cloud_trails,
            forwarder_name=forwarder_name,
            forwarder_version=forwarder_version,
            iam_role_name=iam_role_name,
            install_datadog_policy_macro=install_datadog_policy_macro,
            log_archives=log_archives,
            permissions=permissions,
            site=site,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-datadog-integration.DatadogIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "external_id": "externalId",
        "additional_forwarder_params": "additionalForwarderParams",
        "additional_integration_role_params": "additionalIntegrationRoleParams",
        "cloud_trails": "cloudTrails",
        "forwarder_name": "forwarderName",
        "forwarder_version": "forwarderVersion",
        "iam_role_name": "iamRoleName",
        "install_datadog_policy_macro": "installDatadogPolicyMacro",
        "log_archives": "logArchives",
        "permissions": "permissions",
        "site": "site",
    },
)
class DatadogIntegrationConfig:
    def __init__(
        self,
        *,
        api_key: aws_cdk.aws_secretsmanager.ISecret,
        external_id: builtins.str,
        additional_forwarder_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        additional_integration_role_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_trails: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        forwarder_name: typing.Optional[builtins.str] = None,
        forwarder_version: typing.Optional[builtins.str] = None,
        iam_role_name: typing.Optional[builtins.str] = None,
        install_datadog_policy_macro: typing.Optional[builtins.bool] = None,
        log_archives: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        permissions: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "api_key": api_key,
            "external_id": external_id,
        }
        if additional_forwarder_params is not None:
            self._values["additional_forwarder_params"] = additional_forwarder_params
        if additional_integration_role_params is not None:
            self._values["additional_integration_role_params"] = additional_integration_role_params
        if cloud_trails is not None:
            self._values["cloud_trails"] = cloud_trails
        if forwarder_name is not None:
            self._values["forwarder_name"] = forwarder_name
        if forwarder_version is not None:
            self._values["forwarder_version"] = forwarder_version
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if install_datadog_policy_macro is not None:
            self._values["install_datadog_policy_macro"] = install_datadog_policy_macro
        if log_archives is not None:
            self._values["log_archives"] = log_archives
        if permissions is not None:
            self._values["permissions"] = permissions
        if site is not None:
            self._values["site"] = site

    @builtins.property
    def api_key(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def external_id(self) -> builtins.str:
        '''External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).'''
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_forwarder_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional parameters to pass through to the underlying Forwarder CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml
        for the latest parameters.
        '''
        result = self._values.get("additional_forwarder_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def additional_integration_role_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional parameters to pass through to the underlying Integration Role CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml
        for the latest parameters.
        '''
        result = self._values.get("additional_integration_role_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cloud_trails(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        '''S3 buckets for Datadog CloudTrail integration.

        Permissions will be automatically
        added to the Datadog integration IAM role.
        https://docs.datadoghq.com/integrations/amazon_cloudtrail
        '''
        result = self._values.get("cloud_trails")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]], result)

    @builtins.property
    def forwarder_name(self) -> typing.Optional[builtins.str]:
        '''The Datadog Forwarder Lambda function name.

        DO NOT change when updating an existing
        CloudFormation stack, otherwise the current forwarder function will be replaced and
        all the triggers will be lost.

        :default: DatadogForwarder
        '''
        result = self._values.get("forwarder_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarder_version(self) -> typing.Optional[builtins.str]:
        '''Specify a version of the forwarder to use.

        See
        https://github.com/DataDog/datadog-serverless-functions/releases. Pass this
        parameter as a version string, e.g., '3.9.0'

        :default: latest
        '''
        result = self._values.get("forwarder_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''Customize the name of IAM role for Datadog AWS integration.

        :default: DatadogIntegrationRole
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_datadog_policy_macro(self) -> typing.Optional[builtins.bool]:
        '''If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again.

        :default: true
        '''
        result = self._values.get("install_datadog_policy_macro")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_archives(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        '''S3 paths to store log archives for log rehydration.

        Permissions will be automatically added to the Datadog integration IAM role.
        https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        '''
        result = self._values.get("log_archives")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Customize the permission level for the Datadog IAM role.

        Select "Core" to only grant Datadog read-only permissions (not recommended).

        :default: Full
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        '''Define your Datadog Site to send data to.

        For the Datadog EU site, set to datadoghq.eu

        :default: datadoghq.com
        '''
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogIntegrationStack(
    aws_cdk.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-datadog-integration.DatadogIntegrationStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_key: aws_cdk.aws_secretsmanager.ISecret,
        external_id: builtins.str,
        additional_forwarder_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        additional_integration_role_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_trails: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        forwarder_name: typing.Optional[builtins.str] = None,
        forwarder_version: typing.Optional[builtins.str] = None,
        iam_role_name: typing.Optional[builtins.str] = None,
        install_datadog_policy_macro: typing.Optional[builtins.bool] = None,
        log_archives: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        permissions: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = DatadogIntegrationStackConfig(
            api_key=api_key,
            external_id=external_id,
            additional_forwarder_params=additional_forwarder_params,
            additional_integration_role_params=additional_integration_role_params,
            cloud_trails=cloud_trails,
            forwarder_name=forwarder_name,
            forwarder_version=forwarder_version,
            iam_role_name=iam_role_name,
            install_datadog_policy_macro=install_datadog_policy_macro,
            log_archives=log_archives,
            permissions=permissions,
            site=site,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-datadog-integration.DatadogIntegrationStackConfig",
    jsii_struct_bases=[DatadogIntegrationConfig, aws_cdk.StackProps],
    name_mapping={
        "api_key": "apiKey",
        "external_id": "externalId",
        "additional_forwarder_params": "additionalForwarderParams",
        "additional_integration_role_params": "additionalIntegrationRoleParams",
        "cloud_trails": "cloudTrails",
        "forwarder_name": "forwarderName",
        "forwarder_version": "forwarderVersion",
        "iam_role_name": "iamRoleName",
        "install_datadog_policy_macro": "installDatadogPolicyMacro",
        "log_archives": "logArchives",
        "permissions": "permissions",
        "site": "site",
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
    },
)
class DatadogIntegrationStackConfig(DatadogIntegrationConfig, aws_cdk.StackProps):
    def __init__(
        self,
        *,
        api_key: aws_cdk.aws_secretsmanager.ISecret,
        external_id: builtins.str,
        additional_forwarder_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        additional_integration_role_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_trails: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        forwarder_name: typing.Optional[builtins.str] = None,
        forwarder_version: typing.Optional[builtins.str] = None,
        iam_role_name: typing.Optional[builtins.str] = None,
        install_datadog_policy_macro: typing.Optional[builtins.bool] = None,
        log_archives: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Bucket]] = None,
        permissions: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if isinstance(env, dict):
            env = aws_cdk.Environment(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "api_key": api_key,
            "external_id": external_id,
        }
        if additional_forwarder_params is not None:
            self._values["additional_forwarder_params"] = additional_forwarder_params
        if additional_integration_role_params is not None:
            self._values["additional_integration_role_params"] = additional_integration_role_params
        if cloud_trails is not None:
            self._values["cloud_trails"] = cloud_trails
        if forwarder_name is not None:
            self._values["forwarder_name"] = forwarder_name
        if forwarder_version is not None:
            self._values["forwarder_version"] = forwarder_version
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if install_datadog_policy_macro is not None:
            self._values["install_datadog_policy_macro"] = install_datadog_policy_macro
        if log_archives is not None:
            self._values["log_archives"] = log_archives
        if permissions is not None:
            self._values["permissions"] = permissions
        if site is not None:
            self._values["site"] = site
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def api_key(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def external_id(self) -> builtins.str:
        '''External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).'''
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_forwarder_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional parameters to pass through to the underlying Forwarder CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml
        for the latest parameters.
        '''
        result = self._values.get("additional_forwarder_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def additional_integration_role_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional parameters to pass through to the underlying Integration Role CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml
        for the latest parameters.
        '''
        result = self._values.get("additional_integration_role_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cloud_trails(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        '''S3 buckets for Datadog CloudTrail integration.

        Permissions will be automatically
        added to the Datadog integration IAM role.
        https://docs.datadoghq.com/integrations/amazon_cloudtrail
        '''
        result = self._values.get("cloud_trails")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]], result)

    @builtins.property
    def forwarder_name(self) -> typing.Optional[builtins.str]:
        '''The Datadog Forwarder Lambda function name.

        DO NOT change when updating an existing
        CloudFormation stack, otherwise the current forwarder function will be replaced and
        all the triggers will be lost.

        :default: DatadogForwarder
        '''
        result = self._values.get("forwarder_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarder_version(self) -> typing.Optional[builtins.str]:
        '''Specify a version of the forwarder to use.

        See
        https://github.com/DataDog/datadog-serverless-functions/releases. Pass this
        parameter as a version string, e.g., '3.9.0'

        :default: latest
        '''
        result = self._values.get("forwarder_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''Customize the name of IAM role for Datadog AWS integration.

        :default: DatadogIntegrationRole
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_datadog_policy_macro(self) -> typing.Optional[builtins.bool]:
        '''If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again.

        :default: true
        '''
        result = self._values.get("install_datadog_policy_macro")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_archives(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        '''S3 paths to store log archives for log rehydration.

        Permissions will be automatically added to the Datadog integration IAM role.
        https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        '''
        result = self._values.get("log_archives")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Customize the permission level for the Datadog IAM role.

        Select "Core" to only grant Datadog read-only permissions (not recommended).

        :default: Full
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        '''Define your Datadog Site to send data to.

        For the Datadog EU site, set to datadoghq.eu

        :default: datadoghq.com
        '''
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[aws_cdk.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[aws_cdk.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[aws_cdk.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogIntegrationStackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DatadogIntegration",
    "DatadogIntegrationConfig",
    "DatadogIntegrationStack",
    "DatadogIntegrationStackConfig",
]

publication.publish()
