'''
<div align="center">
	<br/>
	<br/>
  <h1>
	<img height="140" src="assets/alma-cdk-cross-region-parameter.svg" alt="Alma CDK Cross-Region Parameter" />
  <br/>
  <br/>
  </h1>

```sh
npm i -D @alma-cdk/cross-region-parameter
```

  <div align="left">

Store [AWS SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) Parameters into another AWS Region with AWS CDK.

  </div>
  <br/>
</div><br/><div align="center">

![diagram](assets/diagram.svg)

</div><br/>

## 🚧   Project Stability

![experimental](https://img.shields.io/badge/stability-experimental-yellow)

This construct is still versioned with `v0` major version and breaking changes might be introduced if necessary (without a major version bump), though we aim to keep the API as stable as possible (even within `v0` development). We aim to publish `v1.0.0` soon and after that breaking changes will be introduced via major version bumps.

<br/>

## Getting Started

```python
import { CrossRegionParameter } from "@alma-cdk/cross-region-parameter";

new CrossRegionParameter(this, 'SayHiToSweden', {
  region: 'eu-north-1',
  name: '/parameter/path/message',
  description: 'Some message for the Swedes',
  value: 'Hej då!',
});
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ssm
import constructs


class CrossRegionParameter(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/cross-region-parameter.CrossRegionParameter",
):
    '''(experimental) Cross-Region SSM Parameter.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        name_: builtins.str,
        *,
        description: builtins.str,
        name: builtins.str,
        region: builtins.str,
        value: builtins.str,
        allowed_pattern: typing.Optional[builtins.str] = None,
        key_id: typing.Optional[builtins.str] = None,
        parameter_tier: typing.Optional[aws_cdk.aws_ssm.ParameterTier] = None,
        parameter_type: typing.Optional[aws_cdk.aws_ssm.ParameterType] = None,
        policies: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["TagProp", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Define a new Cross-Region SSM Parameter.

        :param scope: -
        :param name_: -
        :param description: (experimental) Information about the SSM Parameter that you want to add. Required by this construct (AWS considers it as optional).
        :param name: (experimental) SSM Parameter name.
        :param region: (experimental) Target region for the parameter. Must be some other region than the current Stack's region.
        :param value: (experimental) The SSM Parameter value that you want to add. Limits: - Standard parameters have a value limit of 4 KB. - Advanced parameters have a value limit of 8 KB.
        :param allowed_pattern: (experimental) A regular expression used to validate the SSM Parameter Value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$``.
        :param key_id: (experimental) The AWS Key Management Service (AWS KMS) ID that you want to use to encrypt a parameter. Either the default AWS KMS key automatically assigned to your AWS account or a custom key. Required for parameters that use the SecureString data type. The KMS Key must exists in the target region. If you don't specify a key ID, the system uses the default key associated with your AWS account.
        :param parameter_tier: (experimental) The SSM Parameter Tier to assign to a parameter. - Parameter Store offers a standard tier and an advanced tier for parameters. Standard parameters have a content size limit of 4 KB and can't be configured to use parameter policies. You can create a maximum of 10,000 standard parameters for each Region in an AWS account. Standard parameters are offered at no additional cost. - Advanced parameters have a content size limit of 8 KB and can be configured to use parameter policies. You can create a maximum of 100,000 advanced parameters for each Region in an AWS account. Advanced parameters incur a charge. For more information, see Standard and advanced parameter tiers in the AWS Systems Manager User Guide. - You can change a standard parameter to an advanced parameter any time. But you can't revert an advanced parameter to a standard parameter. Reverting an advanced parameter to a standard parameter would result in data loss because the system would truncate the size of the parameter from 8 KB to 4 KB. Reverting would also remove any policies attached to the parameter. Lastly, advanced parameters use a different form of encryption than standard parameters. - If you no longer need an advanced parameter, or if you no longer want to incur charges for an advanced parameter, you must delete it and recreate it as a new standard parameter. Default: ParameterTier.STANDARD
        :param parameter_type: (experimental) The type of SSM Parameter that you want to add. Default: ParameterType.STRING
        :param policies: (experimental) One or more policies to apply to a SSM Parameter.
        :param tags: (experimental) Tags to add into the SSM Paramater that you want to add.

        :stability: experimental

        Example::

            new CrossRegionParameter(this, 'SayHiToSweden', {
              region: 'eu-north-1',
              name: '/parameter/path/message',
              description: 'Some message for the Swedes',
              value: 'Hej då!',
            });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CrossRegionParameter.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name_", value=name_, expected_type=type_hints["name_"])
        props = CrossRegionParameterProps(
            description=description,
            name=name,
            region=region,
            value=value,
            allowed_pattern=allowed_pattern,
            key_id=key_id,
            parameter_tier=parameter_tier,
            parameter_type=parameter_type,
            policies=policies,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, name_, props])


@jsii.data_type(
    jsii_type="@alma-cdk/cross-region-parameter.CrossRegionParameterProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "region": "region",
        "value": "value",
        "allowed_pattern": "allowedPattern",
        "key_id": "keyId",
        "parameter_tier": "parameterTier",
        "parameter_type": "parameterType",
        "policies": "policies",
        "tags": "tags",
    },
)
class CrossRegionParameterProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        region: builtins.str,
        value: builtins.str,
        allowed_pattern: typing.Optional[builtins.str] = None,
        key_id: typing.Optional[builtins.str] = None,
        parameter_tier: typing.Optional[aws_cdk.aws_ssm.ParameterTier] = None,
        parameter_type: typing.Optional[aws_cdk.aws_ssm.ParameterType] = None,
        policies: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["TagProp", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param description: (experimental) Information about the SSM Parameter that you want to add. Required by this construct (AWS considers it as optional).
        :param name: (experimental) SSM Parameter name.
        :param region: (experimental) Target region for the parameter. Must be some other region than the current Stack's region.
        :param value: (experimental) The SSM Parameter value that you want to add. Limits: - Standard parameters have a value limit of 4 KB. - Advanced parameters have a value limit of 8 KB.
        :param allowed_pattern: (experimental) A regular expression used to validate the SSM Parameter Value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$``.
        :param key_id: (experimental) The AWS Key Management Service (AWS KMS) ID that you want to use to encrypt a parameter. Either the default AWS KMS key automatically assigned to your AWS account or a custom key. Required for parameters that use the SecureString data type. The KMS Key must exists in the target region. If you don't specify a key ID, the system uses the default key associated with your AWS account.
        :param parameter_tier: (experimental) The SSM Parameter Tier to assign to a parameter. - Parameter Store offers a standard tier and an advanced tier for parameters. Standard parameters have a content size limit of 4 KB and can't be configured to use parameter policies. You can create a maximum of 10,000 standard parameters for each Region in an AWS account. Standard parameters are offered at no additional cost. - Advanced parameters have a content size limit of 8 KB and can be configured to use parameter policies. You can create a maximum of 100,000 advanced parameters for each Region in an AWS account. Advanced parameters incur a charge. For more information, see Standard and advanced parameter tiers in the AWS Systems Manager User Guide. - You can change a standard parameter to an advanced parameter any time. But you can't revert an advanced parameter to a standard parameter. Reverting an advanced parameter to a standard parameter would result in data loss because the system would truncate the size of the parameter from 8 KB to 4 KB. Reverting would also remove any policies attached to the parameter. Lastly, advanced parameters use a different form of encryption than standard parameters. - If you no longer need an advanced parameter, or if you no longer want to incur charges for an advanced parameter, you must delete it and recreate it as a new standard parameter. Default: ParameterTier.STANDARD
        :param parameter_type: (experimental) The type of SSM Parameter that you want to add. Default: ParameterType.STRING
        :param policies: (experimental) One or more policies to apply to a SSM Parameter.
        :param tags: (experimental) Tags to add into the SSM Paramater that you want to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CrossRegionParameterProps.__init__)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument allowed_pattern", value=allowed_pattern, expected_type=type_hints["allowed_pattern"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument parameter_tier", value=parameter_tier, expected_type=type_hints["parameter_tier"])
            check_type(argname="argument parameter_type", value=parameter_type, expected_type=type_hints["parameter_type"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "name": name,
            "region": region,
            "value": value,
        }
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if key_id is not None:
            self._values["key_id"] = key_id
        if parameter_tier is not None:
            self._values["parameter_tier"] = parameter_tier
        if parameter_type is not None:
            self._values["parameter_type"] = parameter_type
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) Information about the SSM Parameter that you want to add.

        Required by this construct (AWS considers it as optional).

        :stability: experimental

        Example::

            'Some message for the Swedes'
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) SSM Parameter name.

        :stability: experimental

        Example::

            '/parameter/path/message'
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Target region for the parameter.

        Must be some other region than the current Stack's region.

        :stability: experimental

        Example::

            'eu-north-1'
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The SSM Parameter value that you want to add.

        Limits:

        - Standard parameters have a value limit of 4 KB.
        - Advanced parameters have a value limit of 8 KB.

        :stability: experimental

        Example::

            'Hej då!'
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) A regular expression used to validate the SSM Parameter Value.

        For example, for String types with values restricted to numbers,
        you can specify the following: ``^\\d+$``.

        :see: https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html#systemsmanager-PutParameter-request-AllowedPattern
        :stability: experimental

        Example::

            '^\d+$'
        '''
        result = self._values.get("allowed_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS Key Management Service (AWS KMS) ID that you want to use to encrypt a parameter.

        Either the default AWS KMS key automatically assigned to your AWS account or a custom key. Required for parameters that use the SecureString data type.

        The KMS Key must exists in the target region.

        If you don't specify a key ID, the system uses the default key associated with your AWS account.

        :see: https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html#systemsmanager-PutParameter-request-KeyId
        :stability: experimental

        Example::

            '1234abcd-12ab-34cd-56ef-1234567890ab'
        '''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_tier(self) -> typing.Optional[aws_cdk.aws_ssm.ParameterTier]:
        '''(experimental) The SSM Parameter Tier to assign to a parameter.

        - Parameter Store offers a standard tier and an advanced tier for parameters. Standard parameters have a content size limit of 4 KB and can't be configured to use parameter policies. You can create a maximum of 10,000 standard parameters for each Region in an AWS account. Standard parameters are offered at no additional cost.
        - Advanced parameters have a content size limit of 8 KB and can be configured to use parameter policies. You can create a maximum of 100,000 advanced parameters for each Region in an AWS account. Advanced parameters incur a charge. For more information, see Standard and advanced parameter tiers in the AWS Systems Manager User Guide.
        - You can change a standard parameter to an advanced parameter any time. But you can't revert an advanced parameter to a standard parameter. Reverting an advanced parameter to a standard parameter would result in data loss because the system would truncate the size of the parameter from 8 KB to 4 KB. Reverting would also remove any policies attached to the parameter. Lastly, advanced parameters use a different form of encryption than standard parameters.
        - If you no longer need an advanced parameter, or if you no longer want to incur charges for an advanced parameter, you must delete it and recreate it as a new standard parameter.

        :default: ParameterTier.STANDARD

        :stability: experimental

        Example::

            ParameterTier.INTELLIGENT_TIERING
        '''
        result = self._values.get("parameter_tier")
        return typing.cast(typing.Optional[aws_cdk.aws_ssm.ParameterTier], result)

    @builtins.property
    def parameter_type(self) -> typing.Optional[aws_cdk.aws_ssm.ParameterType]:
        '''(experimental) The type of SSM Parameter that you want to add.

        :default: ParameterType.STRING

        :stability: experimental

        Example::

            ParameterType.STRING_LIST
        '''
        result = self._values.get("parameter_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ssm.ParameterType], result)

    @builtins.property
    def policies(self) -> typing.Optional[builtins.str]:
        '''(experimental) One or more policies to apply to a SSM Parameter.

        :see: https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html
        :stability: experimental
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["TagProp"]]:
        '''(experimental) Tags to add into the SSM Paramater that you want to add.

        :stability: experimental
        :todo: This might be incorrect type

        Example::

            [
              {
                Key: 'STRING_VALUE',
                Value: 'STRING_VALUE'
              },
            ]
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["TagProp"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/cross-region-parameter.TagProp",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class TagProp:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Tag properties.

        :param key: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TagProp.__init__)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CrossRegionParameter",
    "CrossRegionParameterProps",
    "TagProp",
]

publication.publish()
