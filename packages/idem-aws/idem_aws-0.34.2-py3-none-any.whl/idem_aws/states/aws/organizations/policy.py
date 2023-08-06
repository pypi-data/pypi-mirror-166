"""State module for managing Amazon Organizations Policies."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.organizations.policy_attachment.absent",
        ],
    },
    "present": {
        "require": [
            "aws.organizations.account.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    description: str = None,
    policy_type: str = None,
    content: str = None,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Creates a policy of a specified type that you can attach to a root, an organizational unit (OU), or an individual AWS account.

    If the request includes tags, then the requester must have the ``organizations:TagResource`` permission. This
    operation can be called only from the organization's management account.

    Args:
        name(str):
            The name of the policy.
        resource_id(str, Optional):
            The ID of the policy in Amazon Web Services.
        description(str, Optional):
            A description to assign to the policy.
        policy_type(str, Optional):
            The type of policy to create. Only supported values are ``SERVICE_CONTROL_POLICY`` and ``TAG_POLICY``.
        content(str, Optional):
            The policy text content to add to the new policy. The text that you supply must adhere to the rules of the policy type.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the policy.

            * Key (*str*):
                The key identifier, or name, of the tag.
            * Value (*str*):
                The string value that's associated with the key of the tag.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_policy]:
          aws.organizations.policy.present:
            - name: 'string'
            - resource_id: 'string'
            - description: 'string'
            - policy_type: 'SERVICE_CONTROL_POLICY|TAG_POLICY'
            - content: 'string'
            - tags:
              - Key: 'string'
                Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy:
              aws.organizations.policy.present:
                - name: 'idem_test_policy'
                - description: 'Enables admins of attached accounts to delegate all S3 permissions'
                - policy_type: 'SERVICE_CONTROL_POLICY'
                - content:
                    Version: '2012-10-17'
                    Statement:
                      - Sid: 'AllowAllS3Actions'
                        Effect: 'Allow'
                        Action: ['s3:*']
                - tags:
                  - Key: 'provider'
                    Value: 'idem'
    """
    result = dict(comment=(), name=name, result=True, old_state=None, new_state=None)
    before = None
    existing_tags = None

    if resource_id:
        before = await hub.exec.boto3.client.organizations.describe_policy(
            ctx, PolicyId=resource_id
        )
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    change_dict = dict(Name=None, Description=None, Content=None)

    update_tag = False
    policy_id = None
    if before:
        # Policy exists , update
        if not ctx.get("test", False):
            result["comment"] = result["comment"] + (
                f"aws.organizations.policy '{name}' exists.",
            )
        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
            before["ret"]["Policy"]
        )
        plan_state = copy.deepcopy(result["old_state"])

        policy_id = before["ret"]["Policy"]["PolicySummary"].get("Id")

        try:

            if before["ret"]["Policy"]["PolicySummary"].get("Name") != name:
                change_dict["Name"] = name

            if (
                before["ret"]["Policy"]["PolicySummary"].get("Description")
                != description
            ):
                change_dict["Description"] = description

            if before["ret"]["Policy"]["Content"] != content:
                change_dict["Content"] = content

            if any(value is not None for value in change_dict.values()):

                if ctx.get("test", False):
                    plan_state["resource_id"] = policy_id
                    if change_dict.get("Name"):
                        plan_state["name"] = change_dict.get("Name")
                    if change_dict.get("Description"):
                        plan_state["description"] = change_dict.get("Description")
                    if change_dict.get("Content"):
                        plan_state["content"] = change_dict.get("Content")
                    result["comment"] = result["comment"] + (
                        f"Would update aws.organizations.policy '{name}'",
                    )
                else:
                    update_policy_ret = (
                        await hub.exec.boto3.client.organizations.update_policy(
                            ctx,
                            PolicyId=policy_id,
                            Name=change_dict.get("Name"),
                            Description=change_dict.get("Description"),
                            Content=change_dict.get("Content"),
                        )
                    )

                    if not update_policy_ret["result"]:
                        result["comment"] = (
                            result["comment"] + update_policy_ret["comment"]
                        )
                        result["result"] = update_policy_ret["result"]
                        return result
                    after = update_policy_ret

                    if after["ret"]:
                        result[
                            "new_state"
                        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
                            after["ret"]["Policy"]
                        )
                        result["comment"] = result["comment"] + (
                            f"Updated aws.organizations.policy '{name}'",
                        )

            else:
                result["new_state"] = copy.deepcopy(result["old_state"])

            old_tags = await hub.exec.boto3.client.organizations.list_tags_for_resource(
                ctx, ResourceId=policy_id
            )

            if old_tags["result"]:
                existing_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    old_tags["ret"]["Tags"]
                )
                result["old_state"]["tags"] = existing_tags

                # If no update in tags , then new_state will contain same tags as old
                if tags is None and not ctx.get("test", False):
                    result["new_state"]["tags"] = existing_tags

            if tags is not None and tags != existing_tags:

                update_tags_ret = await hub.tool.aws.organizations.tag.update_tags(
                    ctx, policy_id, existing_tags, tags
                )
                if not update_tags_ret["result"]:
                    result["comment"] = result["comment"] + update_tags_ret["comment"]
                    result["result"] = update_tags_ret["result"]
                    return result

                if update_tags_ret["result"]:
                    update_tag = True
                    if ctx.get("test", False):
                        plan_state["tags"] = tags

                    result["comment"] = result["comment"] + (
                        f"Updated tags on aws.organizations.policy '{name}'.",
                    )

        except hub.tool.boto3.exception.ClientError as e:
            result["result"] = False
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)

    else:

        # Policy does not exist , create

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "description": description,
                    "policy_type": policy_type,
                    "content": content,
                    "tags": tags,
                },
            )
            result["comment"] = result["comment"] + (
                f"Would create aws.organizations.policy '{name}'",
            )
            return result

        try:
            create_policy_ret = await hub.exec.boto3.client.organizations.create_policy(
                ctx,
                Name=name,
                Description=description,
                Type=policy_type,
                Content=content,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = create_policy_ret["result"]
            if not result["result"]:
                result["comment"] = result["comment"] + create_policy_ret["comment"]
                return result

            after = create_policy_ret

            result[
                "new_state"
            ] = hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
                after["ret"]["Policy"]
            )

            policy_id = result["new_state"]["resource_id"]
            if tags is not None:
                list_tags = (
                    await hub.exec.boto3.client.organizations.list_tags_for_resource(
                        ctx, ResourceId=policy_id
                    )
                )

                if list_tags["result"]:
                    result["new_state"][
                        "tags"
                    ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                        list_tags["ret"]["Tags"]
                    )
                else:
                    hub.log.debug(
                        f"Unable to list tags for resource {resource_id} with error: {list_tags['comment']}"
                    )
                    result["comment"] = result["comment"] + list_tags["comment"]
                    result["result"] = list_tags["result"]

            result["comment"] = result["comment"] + (
                f"Created aws.organizations.policy '{name}'.",
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif before and update_tag:
        try:
            updated_tags = (
                await hub.exec.boto3.client.organizations.list_tags_for_resource(
                    ctx, ResourceId=policy_id
                )
            )

            if updated_tags["result"]:
                result["new_state"][
                    "tags"
                ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    updated_tags["ret"]["Tags"]
                )
            else:
                hub.log.debug(
                    f"Unable to list tags for resource {resource_id} with error: {updated_tags['comment']}"
                )
                result["comment"] = result["comment"] + updated_tags["comment"]
                result["result"] = updated_tags["result"]

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str) -> Dict[str, Any]:
    """Deletes the specified policy from your organization.

    Before you perform this operation, you must first detach the policy from all organizational units (OUs), roots, and accounts.
    This operation can be called only from the organization's management account.

    Args:
        name(str):
            The name of the policy.
        resource_id(str):
            The ID of the policy in Amazon Web Services.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_policy]:
          aws.organizations.policy.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy:
              aws.organizations.policy.absent:
                - name: 'idem_test_policy'
                - resource_id: 'p-123456789012'
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before = await hub.exec.boto3.client.organizations.describe_policy(
        ctx, PolicyId=resource_id
    )

    if not before:
        result["comment"] = result["comment"] + (
            f"aws.organizations.policy '{name}' already absent",
        )
    else:
        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
            before["ret"]["Policy"]
        )
        if ctx.get("test", False):
            result["comment"] = result["comment"] + (
                f"Would delete aws.organizations.policy '{name}'",
            )
            return result
        try:

            delete_ret = await hub.exec.boto3.client.organizations.delete_policy(
                ctx, PolicyId=resource_id
            )

            if not delete_ret["result"]:
                result["comment"] = result["comment"] + delete_ret["comment"]
                result["result"] = delete_ret["result"]
                return result

            result["comment"] = result["comment"] + (
                f"aws.organizations.policy {name} deleted.",
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS Organization Policies in a way that can be recreated/managed with the corresponding "present" function.

    This operation can be called only from the organization's management account
    or by a member account that is a delegated administrator for an AWS service.

    The only supported policy types by are ``SERVICE_CONTROL_POLICY`` and ``TAG_POLICY``.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.policy
    """
    result = {}

    list_scp_policies = await hub.exec.boto3.client.organizations.list_policies(
        ctx, Filter="SERVICE_CONTROL_POLICY"
    )

    if not list_scp_policies:
        hub.log.debug(
            f"Could not describe policy with error: {list_scp_policies['comment']}"
        )
        return {}

    list_all_policies = list_scp_policies["ret"]["Policies"]

    list_tag_policies = await hub.exec.boto3.client.organizations.list_policies(
        ctx, Filter="TAG_POLICY"
    )

    if not list_tag_policies:
        hub.log.debug(
            f"Could not describe policy with error: {list_tag_policies['comment']}"
        )
        return {}

    if list_tag_policies["ret"]["Policies"]:
        list_all_policies.extend(list_tag_policies["ret"]["Policies"])

    for policy in list_all_policies:
        policy_id = policy["Id"]

        policy_ret = await hub.exec.boto3.client.organizations.describe_policy(
            ctx, PolicyId=policy_id
        )

        if not policy_ret and not policy_ret["ret"]:
            hub.log.debug(
                f"Could not describe '{policy_id}' with error: {policy_ret['comment']}"
            )
            continue

        tags_ret = await hub.exec.boto3.client.organizations.list_tags_for_resource(
            ctx, ResourceId=policy_id
        )
        if not tags_ret["result"]:
            hub.log.debug(
                f"Unable to list tags for resource {policy_id} with error: {tags_ret['comment']}"
            )

        translated_resource = (
            hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
                policy_ret["ret"]["Policy"],
                tags_ret["ret"]["Tags"] if tags_ret else None,
            )
        )

        result[policy["Name"]] = {
            "aws.organizations.policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
