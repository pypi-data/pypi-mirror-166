# Copyright 2018-2019, James Nugent.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain
# one at http://mozilla.org/MPL/2.0/.

"""
Contains a Pulumi ComponentResource for creating a good-practice AWS VPC.
"""
import json, time
from typing import Mapping, Sequence
import pulumi
from pulumi import ComponentResource, ResourceOptions, StackReference
from pulumi import Input, Output

from resources import aws_lambda, cloudwatch

class LambdaFunction(ComponentResource):
    """
    Comment here

    """

    def __init__(self, name: str, props: None, opts:  ResourceOptions = None):
        """
        Constructs a Lambda Function.

        :param name: The Pulumi resource name. Child resource names are constructed based on this.
        """
        super().__init__('Bucket', name, {}, opts)

        Resources = [aws_lambda]

        for resource in Resources:
            resource.self = self
            resource.base_tags = props.base_tags


        # Create a lambda function
        lambda_function = [aws_lambda.Lambda_Function(
            props.lf[i]["name"],
            props,
            code=props.lf[i]["code"],
            role=props.lf[i]["role"],
            handler=props.lf[i]["handler"],
            runtime=props.lf[i]["runtime"],
            environment=props.lf[i]["environment"],
            parent=self,
            depends_on=opts.depends_on,
            provider=opts.providers.get(props.stack+'_prov')
        )
        for i in props.lf
        ]

        # Create Event Rule
        event_rule = [cloudwatch.Event_Rule(
            props.lf[i]["trigger"]["name"],
            props,
            description=props.lf[i]["trigger"]["description"],
            schedule_expression=props.lf[i]["trigger"]["schedule_expression"],
            is_enabled=props.lf[i]["trigger"]["is_enabled"],
            parent=self,
            depends_on=opts.depends_on,
            provider=opts.providers.get(props.stack+'_prov')
        )
        for i in props.lf
        ]

        # Create Event Trigger
        event_trigger = [cloudwatch.Event_Target(
            props.lf[i]["name"],
            props,
            arn=lambda_function[0].arn,
            rule=event_rule[0].name,
            parent=self,
            depends_on=opts.depends_on,
            provider=opts.providers.get(props.stack+'_prov')
        )
        for i in props.lf
        ]

        # Create Permission
        lambda_permission = [aws_lambda.Lambda_Permission(
            props.lf[i]["name"],
            props,
            action=props.lf[i]["permission"]["action"],
            function=lambda_function[0].name,
            principal=props.lf[i]["permission"]["principal"],
            source_arn=event_rule[0].arn,
            parent=self,
            depends_on=opts.depends_on,
            provider=opts.providers.get(props.stack+'_prov')
        )
        for i in props.lf
        ]