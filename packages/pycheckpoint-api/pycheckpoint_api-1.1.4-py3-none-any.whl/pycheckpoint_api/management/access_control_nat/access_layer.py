from typing import List, Union

from box import Box
from restfly.endpoint import APIEndpoint

from pycheckpoint_api.models import Color
from pycheckpoint_api.utils import sanitize_secondary_parameters

from ..exception import MandatoryFieldMissing


class AccessLayer(APIEndpoint):
    def add(
        self,
        name: str,
        add_default_rule: bool = True,
        applications_and_url_filtering: bool = False,
        content_awareness: bool = False,
        detect_using_x_forward_for: bool = False,
        firewall: bool = True,
        implicit_cleanup_action: str = "drop",
        mobile_access: bool = False,
        shared: bool = False,
        tags: Union[str, List[str]] = None,
        **kw,
    ) -> Box:
        """
        Create new object.

        Args:
            name (str): Layer name.
            add_default_rule (bool, optional): Indicates whether to include a cleanup rule in the new layer.
            applications_and_url_filtering (bool, optional): Whether to enable Applications & URL Filtering blade on the layer.
            content_awareness (bool, optional): Whether to enable Content Awareness blade on the layer.
            detect_using_x_forward_for (bool, optional): Whether to use X-Forward-For HTTP header, which is added by the proxy
            server to keep track of the original source IP.
            firewall (bool, optional): Whether to enable Firewall blade on the layer.
            implicit_cleanup_action (str, optional): The default "catch-all" action for traffic that does not match any\
            explicit or implied rules in the layer. Valid values are "drop" or "accept"
            mobile_access (bool, optional): Whether to enable Mobile Access blade on the layer.
            shared (bool, optional): Whether this layer is shared.
            tags (Union[str, List[str]], optional): Collection of tag identifiers.

        Keyword Args:
            **color (Color, optional):
                Color of the object. Should be one of existing colors.
            **comments (str, optional):
                Comments string.
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **ignore_warnings (bool, optional):
                Apply changes ignoring warnings. Defaults to False
            **ignore_errors (bool, optional):
                Apply changes ignoring errors. You won't be able to publish such a changes.
                If ignore_warnings flag was omitted - warnings will also be ignored. Defaults to False

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_layer.add(
            ... name="New Layer 1",
            ... add_default_rule=True,
            ... applications_and_url_filtering=False,
            ... content_awareness=False,
            ... detect_using_x_forward_for=True,
            ... firewall=True,
            ... mobile_access=False,
            ... shared=False,
            ... tags=["t1"])
        """

        # Main request parameters
        payload = {"name": name}

        if add_default_rule is not None:
            payload["add-default-rule"] = add_default_rule
        if applications_and_url_filtering is not None:
            payload["applications-and-url-filtering"] = applications_and_url_filtering
        if content_awareness is not None:
            payload["content-awareness"] = content_awareness
        if detect_using_x_forward_for is not None:
            payload["detect-using-x-forward-for"] = detect_using_x_forward_for
        if firewall is not None:
            payload["firewall"] = firewall
        if implicit_cleanup_action is not None:
            payload["implicit-cleanup-action"] = implicit_cleanup_action
        if mobile_access is not None:
            payload["mobile-access"] = mobile_access
        if shared is not None:
            payload["shared"] = shared
        if tags is not None:
            payload["tags"] = tags

        # Secondary parameters
        secondary_parameters = {
            "color": Color,
            "comments": str,
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("add-access-layer", json=payload)

    def show(
        self,
        uid: str = None,
        name: str = None,
        **kw,
    ) -> Box:
        """
        Retrieve existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier. Mandatory if "rule_number" or "name" are not set.
            name (str, optional): Object name. Mandatory if "rule_number" or "uid" are not set.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_layer.show(
            ... uid="81530aad-bc98-4e8f-a62d-079424ddd955")
        """
        # Main request parameters
        payload = {}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        # Secondary parameters
        secondary_parameters = {"details_level": str}

        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("show-access-layer", json=payload)

    def set(
        self,
        uid: str = None,
        name: str = None,
        new_name: str = None,
        add_default_rule: bool = True,
        applications_and_url_filtering: bool = False,
        content_awareness: bool = False,
        detect_using_x_forward_for: bool = False,
        firewall: bool = True,
        implicit_cleanup_action: str = "drop",
        mobile_access: bool = False,
        shared: bool = False,
        tags: Union[str, List[str]] = None,
        **kw,
    ) -> Box:
        """
        Edit existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            new_name (str, optional): New name of the object.
            name (str, optional): Rule name.
            add_default_rule (bool, optional): Indicates whether to include a cleanup rule in the new layer.
            applications_and_url_filtering (bool, optional): Whether to enable Applications & URL Filtering blade on the layer.
            content_awareness (bool, optional): Whether to enable Content Awareness blade on the layer.
            detect_using_x_forward_for (bool, optional): Whether to use X-Forward-For HTTP header, which is added by the proxy
            server to keep track of the original source IP.
            firewall (bool, optional): Whether to enable Firewall blade on the layer.
            implicit_cleanup_action (str, optional): The default "catch-all" action for traffic that does not match any\
            explicit or implied rules in the layer. Valid values are "drop" or "accept"
            mobile_access (bool, optional): Whether to enable Mobile Access blade on the layer.
            shared (bool, optional): Whether this layer is shared.
            tags (Union[str, List[str]], optional): Collection of tag identifiers.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **ignore_warnings (bool, optional):
                Apply changes ignoring warnings. Defaults to False
            **ignore_errors (bool, optional):
                Apply changes ignoring errors. You won't be able to publish such a changes.
                If ignore_warnings flag was omitted - warnings will also be ignored. Defaults to False

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_layer.set(
            ... name="New Layer 1",
            ... add_default_rule=True,
            ... applications_and_url_filtering=False,
            ... content_awareness=False,
            ... detect_using_x_forward_for=True,
            ... firewall=True,
            ... mobile_access=False,
            ... shared=False,
            ... tags=["t1"])
        """

        # Main request parameters
        payload = {}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        if new_name is not None:
            payload["new-name"] = new_name
        if add_default_rule is not None:
            payload["add-default-rule"] = add_default_rule
        if applications_and_url_filtering is not None:
            payload["applications-and-url-filtering"] = applications_and_url_filtering
        if content_awareness is not None:
            payload["content-awareness"] = content_awareness
        if detect_using_x_forward_for is not None:
            payload["detect-using-x-forward-for"] = detect_using_x_forward_for
        if firewall is not None:
            payload["firewall"] = firewall
        if implicit_cleanup_action is not None:
            payload["implicit-cleanup-action"] = implicit_cleanup_action
        if mobile_access is not None:
            payload["mobile-access"] = mobile_access
        if shared is not None:
            payload["shared"] = shared
        if tags is not None:
            payload["tags"] = tags

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("set-access-layer", json=payload)

    def delete(
        self,
        uid: str = None,
        name: str = None,
        **kw,
    ) -> Box:
        """
        Delete existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_layer.delete(
            ... layer="Network",
            ... uid="81530aad-bc98-4e8f-a62d-079424ddd955")
        """
        # Main request parameters
        payload = {}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("delete-access-layer", json=payload)

    def show_access_layers(
        self,
        filter_results: str = None,
        limit: int = 50,
        offset: int = 0,
        order: List[dict] = None,
        **kw,
    ) -> Box:
        """
        Retrieve all objects.

        Args:
            filter_results (str): Search expression to filter objects by.\
            The provided text should be exactly the same as it would be given in SmartConsole Object Explorer.\
            The logical operators in the expression ('AND', 'OR') should be provided in capital letters.\
            he search involves both a IP search and a textual search in name, comment, tags etc.
            limit (int): The maximal number of returned results. Defaults to 50 (between 1 and 500)
            offset (int): Number of the results to initially skip. Defaults to 0

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **domains_to_process (List[str], optional):
                Indicates which domains to process the commands on. It cannot be used with the details_level full,\
                must be run from the System Domain only and with ignore_warnings true.\
                Valid values are: CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_layer.show_access_layers()
        """

        # Main request parameters
        payload = {}
        if filter_results is not None:
            payload["filter"] = filter_results
        if limit is not None:
            payload["limit"] = limit
        if offset is not None:
            payload["offset"] = offset
        if order is not None:
            payload["order"] = order

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
            "domains_to_process": List[str],
        }

        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("show-access-layers", json=payload)
