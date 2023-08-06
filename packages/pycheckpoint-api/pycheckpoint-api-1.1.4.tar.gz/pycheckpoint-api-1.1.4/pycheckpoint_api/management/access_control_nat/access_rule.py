import logging
import time
from typing import List, Union

from box import Box
from restfly.endpoint import APIEndpoint

from pycheckpoint_api.utils import sanitize_secondary_parameters

from ..exception import MandatoryFieldMissing

logger = logging.getLogger(__name__)


class AccessRule(APIEndpoint):
    def add(
        self,
        layer: str,
        position: Union[int, str, dict],
        name: str = None,
        action: str = "Drop",
        action_settings: dict = None,
        content: dict = None,
        content_direction: str = None,
        content_negate: bool = None,
        custom_fields: dict = None,
        destination: Union[str, List[str]] = None,
        destination_negate: bool = None,
        enabled: bool = None,
        inline_layer: str = None,
        install_on: Union[str, List[str]] = None,
        service: Union[str, List[str]] = None,
        service_negate: bool = None,
        service_resource: str = None,
        source: Union[str, List[str]] = None,
        source_negate: bool = None,
        time: Union[str, List[str]] = None,
        track: dict = None,
        user_check: dict = None,
        vpn: Union[str, dict, List[dict]] = None,
        **kw,
    ) -> Box:
        """
        Create new object.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            position (Union[int, str, dict]): Position in the rulebase. If an integer is provided, it will add the rule\
            at the specific position. If a string is provided, it will add the rule at the position mentioned in the\
            valid values ("top" or "bottom"). Otherwise, you can provide a dictionnary to explain more complex position\
            (see the API documentation).
            name (str, optional): Rule name.
            action (str, optional): "Accept", "Drop", "Ask", "Inform", "Reject", "User Auth", "Client Auth", "Apply Layer".
            action_settings (dict, optional): Action settings.
            content (dict, optional): List of processed file types that this rule applies on.
            content_direction (str, optional): On which direction the file types processing is applied. ("any", "up" or "down")
            content_negate (bool, optional): True if negate is set for data.
            custom_fields (dict, optional): Custom fields.
            destination (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            destination_negate (bool, optional): True if negate is set for destination.
            enabled (bool, optional): Enable/Disable the rule.
            inline_layer (str, optional): Inline Layer identified by the name or UID. Relevant only if "Action" was set to
            "Apply Layer".
            install_on (Union[str, List[str]], optional): Which Gateways identified by the name or UID to install the policy on
            service (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            service_negate (bool, optional): True if negate is set for service.
            service_resource (str, optional): Resource of the service identified by the name or UID. When a service-resource\
            exists, the service parameter should contains exactly one service element.
            source (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            source_negate (bool, optional): True if negate is set for source.
            time (Union[str, List[str]], optional): List of time objects. For example: "Weekend", "Off-Work", "Every-Day".\
            Default is Any.
            track (dict, optional): Track Settings.
            user_check (dict, optional): User check settings.
            vpn (Union[str, dict, List[dict]], optional): Communities or Directional. See the API documentation for more\
            information

        Keyword Args:
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
            >>> management.access_control_nat.access_rule.add(
            ... layer="Network",
            ... position=1,
            ... name="Rule 1",
            ... action="Drop",
            ... action_settings={"enable-identity-captive-portal": False},
            ... content={},
            ... content_direction="any",
            ... content_negate=False,
            ... custom_fields={"field-1": "", "field-2": "", "field-3": ""},
            ... destination="Any",
            ... destination_negate=False,
            ... enabled=True,
            ... inline_layer="Inline",
            ... install_on="",
            ... service="smtp",
            ... service_negate=False,
            ... service_resource="",
            ... source="Any",
            ... source_negate=False,
            ... time=[{"uid": "aa785d6d-7785-aad5-36a3-ab2d74c966ee"}],
            ... track="",
            ... user_check="",
            ... vpn={"community": ["MyIntranet"]},)
        """

        # Main request parameters
        payload = {"layer": layer, "position": position}

        if name is not None:
            payload["name"] = name
        if action is not None:
            payload["action"] = action
        if action_settings is not None:
            payload["action-settings"] = action_settings
        if content is not None:
            payload["content"] = content
        if content_direction is not None:
            payload["content-direction"] = content_direction
        if content_negate is not None:
            payload["content-negate"] = content_negate
        if custom_fields is not None:
            payload["custom-fields"] = custom_fields
        if destination is not None:
            payload["destination"] = destination
        if destination_negate is not None:
            payload["destination-negate"] = destination_negate
        if enabled is not None:
            payload["enabled"] = enabled
        if inline_layer is not None:
            payload["inline-layer"] = inline_layer
        if install_on is not None:
            payload["install-on"] = install_on
        if service is not None:
            payload["service"] = service
        if service_negate is not None:
            payload["service-negate"] = service_negate
        if service_resource is not None:
            payload["service-resource"] = service_resource
        if source is not None:
            payload["source"] = source
        if source_negate is not None:
            payload["source-negate"] = source_negate
        if time is not None:
            payload["time"] = time
        if track is not None:
            payload["track"] = track
        if user_check is not None:
            payload["user-check"] = track
        if vpn is not None:
            payload["vpn"] = vpn

        # Secondary parameters
        secondary_parameters = {
            "comments": str,
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("add-access-rule", json=payload)

    def show(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        rule_number: int = None,
        show_as_ranges: bool = False,
        show_hits: bool = None,
        hits_settings: dict = None,
        **kw,
    ) -> Box:
        """
        Retrieve existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            rule_number (int, optional): Rule number. Mandatory if "uid" or "name" are not set.
            uid (str, optional): Object unique identifier. Mandatory if "rule_number" or "name" are not set.
            name (str, optional): Object name. Mandatory if "rule_number" or "uid" are not set.
            show_as_ranges (bool, optional): When true, the source, destination and services & applications parameters
            are displayed as ranges of IP addresses and port numbers rather than network objects.
            Objects that are not represented using IP addresses or port numbers are presented as objects.
            In addition, the response of each rule does not contain the parameters: source, source-negate,
            destination, destination-negate, service and service-negate, but instead it contains the
            parameters: source-ranges, destination-ranges and service-ranges.
            Note: Requesting to show rules as ranges is limited up to 20 rules per request, otherwise an
            error is returned. If you wish to request more rules, use the offset and limit parameters to
            limit your request.
            show_hits (bool, optional): N/A
            hits_settings (bool, optional): N/A

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_rule.show(
            ... uid="1df8a4b0-fa8b-428b-b649-626b74bf7f81",
            ... layer="MyLayer",
            ... show_as_ranges=False,
            ... show_hits=True,
            ... hits_settings="",)
        """
        # Main request parameters
        payload = {"layer": layer}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        elif rule_number is not None:
            payload["rule-number"] = rule_number
        else:
            raise MandatoryFieldMissing("uid or name or rule_number")

        if show_as_ranges is not None:
            payload["show-as-ranges"] = show_as_ranges
        if show_hits is not None:
            payload["show-hits"] = show_hits
        if hits_settings is not None:
            payload["hits-settings"] = hits_settings

        # Secondary parameters
        secondary_parameters = {"details_level": str}

        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("show-access-rule", json=payload)

    def set(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        rule_number: int = None,
        new_name: str = None,
        new_position: Union[int, str, dict] = None,
        action: str = "Drop",
        action_settings: dict = None,
        content: dict = None,
        content_direction: str = None,
        content_negate: bool = None,
        custom_fields: dict = None,
        destination: Union[str, List[str]] = None,
        destination_negate: bool = None,
        enabled: bool = None,
        inline_layer: str = None,
        install_on: Union[str, List[str]] = None,
        service: Union[str, List[str]] = None,
        service_negate: bool = None,
        service_resource: str = None,
        source: Union[str, List[str]] = None,
        source_negate: bool = None,
        time: Union[str, List[str]] = None,
        track: dict = None,
        user_check: dict = None,
        vpn: Union[str, dict, List[dict]] = None,
        **kw,
    ) -> Box:
        """
        Edit existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            uid (str, optional): Object unique identifier.
            new_name (str, optional): New name of the object.
            position (Union[int, str, dict], optional): Position in the rulebase. If an integer is provided, it will add the\
            rule at the specific position. If a string is provided, it will add the rule at the position mentioned in the\
            valid values ("top" or "bottom"). Otherwise, you can provide a dictionnary to explain more complex position\
            (see the API documentation).
            name (str, optional): Rule name.
            action (str, optional): "Accept", "Drop", "Ask", "Inform", "Reject", "User Auth", "Client Auth", "Apply Layer".
            action_settings (dict, optional): Action settings.
            content (dict, optional): List of processed file types that this rule applies on.
            content_direction (str, optional): On which direction the file types processing is applied. ("any", "up" or "down")
            content_negate (bool, optional): True if negate is set for data.
            custom_fields (dict, optional): Custom fields.
            destination (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            destination_negate (bool, optional): True if negate is set for destination.
            enabled (bool, optional): Enable/Disable the rule.
            inline_layer (str, optional): Inline Layer identified by the name or UID. Relevant only if "Action" was set to\
            "Apply Layer".
            install_on (Union[str, List[str]], optional): Which Gateways identified by the name or UID to install the policy on
            service (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            service_negate (bool, optional): True if negate is set for service.
            service_resource (str, optional): Resource of the service identified by the name or UID. When a service-resource\
            exists, the service parameter should contains exactly one service element.
            source (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            source_negate (bool, optional): True if negate is set for source.
            time (Union[str, List[str]], optional): List of time objects. For example: "Weekend", "Off-Work", "Every-Day".\
            Default is Any.
            track (dict, optional): Track Settings.
            user_check (dict, optional): User check settings.
            vpn (Union[str, dict, List[dict]], optional): Communities or Directional. See the API documentation for more\
            information

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
            >>> management.access_control_nat.access_rule.set(
            ... uid="1df8a4b0-fa8b-428b-b649-626b74bf7f81",
            ... new_name="Rule 1",
            ... new_position=3,
            ... layer="Network",
            ... action="Drop",
            ... action_settings={"enable-identity-captive-portal": False},
            ... content={},
            ... content_direction="any",
            ... content_negate=False,
            ... custom_fields={"field-1": "", "field-2": "", "field-3": ""},
            ... destination="Any",
            ... destination_negate=False,
            ... enabled=True,
            ... inline_layer="Inline",
            ... install_on="Policy Targets",
            ... service="smtp",
            ... service_negate=False,
            ... service_resource="",
            ... source="Any",
            ... source_negate=False,
            ... time=[{"uid": "aa785d6d-7785-aad5-36a3-ab2d74c966ee"}],
            ... track="",
            ... user_check="",
            ... vpn={"community": ["MyIntranet"]},)
        """

        # Main request parameters
        payload = {"layer": layer}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        elif rule_number is not None:
            payload["rule-number"] = rule_number
        else:
            raise MandatoryFieldMissing("uid or name or rule_number")

        if action is not None:
            payload["action"] = action
        if action_settings is not None:
            payload["action-settings"] = action_settings
        if content is not None:
            payload["content"] = content
        if content_direction is not None:
            payload["content-direction"] = content_direction
        if content_negate is not None:
            payload["content-negate"] = content_negate
        if custom_fields is not None:
            payload["custom-fields"] = custom_fields
        if destination is not None:
            payload["destination"] = destination
        if destination_negate is not None:
            payload["destination-negate"] = destination_negate
        if enabled is not None:
            payload["enabled"] = enabled
        if inline_layer is not None:
            payload["inline-layer"] = inline_layer
        if install_on is not None:
            payload["install-on"] = install_on
        if service is not None:
            payload["service"] = service
        if service_negate is not None:
            payload["service-negate"] = service_negate
        if service_resource is not None:
            payload["service-resource"] = service_resource
        if source is not None:
            payload["source"] = source
        if source_negate is not None:
            payload["source-negate"] = source_negate
        if time is not None:
            payload["time"] = time
        if track is not None:
            payload["track"] = track
        if user_check is not None:
            payload["user-check"] = track
        if vpn is not None:
            payload["vpn"] = vpn
        if new_name is not None:
            payload["new-name"] = new_name
        if new_position is not None:
            payload["new-position"] = new_position

        # Secondary parameters
        secondary_parameters = {
            "comments": str,
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("set-access-rule", json=payload)

    def delete(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        rule_number: int = None,
        **kw,
    ) -> Box:
        """
        Delete existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.
            rule_number (int, optional): Rule number.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_rule.delete(
            ... layer="Network",
            ... uid="1df8a4b0-fa8b-428b-b649-626b74bf7f81")
        """
        # Main request parameters
        payload = {"layer": layer}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        elif rule_number is not None:
            payload["rule-number"] = rule_number
        else:
            raise MandatoryFieldMissing("uid or name or rule_number")

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("delete-access-rule", json=payload)

    def show_access_rulebase(
        self,
        name: str = None,
        uid: str = None,
        show_all: bool = False,
        filter_results: str = None,
        filter_settings: dict = None,
        limit: int = 50,
        offset: int = 0,
        order: List[dict] = None,
        package: str = None,
        show_as_ranges: bool = False,
        show_hits: bool = None,
        use_object_dictionnary: bool = None,
        hits_settings: dict = None,
        **kw,
    ) -> Box:
        """Shows the entire Access Rules layer. This layer is divided into sections. An Access Rule may be within a section,
        or independent of a section (in which case it is said to be under the "global" section). The reply features
        a list of objects. Each object may be a section of the layer, with all its rules in, or a rule itself,
        for the case of rules which are under the global section. An optional "filter" field may be added in order
        to filter out only those rules that match a search criteria.

        Args:
            name (str, optional): Object name. Must be unique in the domain.
            uid (str, optional): Object unique identifier.
            show_all (bool, optional): Indicates if you want to shown all objects or not. If yes, `offset` will be ignored.\
            Defaults to False
            filter_results (str, optional): Search expression to filter objects by.\
            The provided text should be exactly the same as it would be given in SmartConsole Object Explorer.\
            The logical operators in the expression ('AND', 'OR') should be provided in capital letters.\
            he search involves both a IP search and a textual search in name, comment, tags etc.
            filter_settings (str, optional): Sets filter preferences.
            limit (int, optional): The maximal number of returned results. Defaults to 50 (between 1 and 500)
            offset (int, optional): Number of the results to initially skip. Defaults to 0
            order (List[dict], optional): Sorts results by the given field. By default the results are sorted in the \
            descending order by the session publish time.
            package (str, optional): Name of the package.
            show_as_ranges (bool, optional): When true, the source, destination and services & applications parameters are\
            displayed as ranges of IP addresses and port numbers rather than network objects. Objects that are not represented\
            using IP addresses or port numbers are presented as objects. In addition, the response of each rule does not\
            contain the parameters: source, source-negate, destination, destination-negate, service and service-negate,\
            but instead it contains the parameters: source-ranges, destination-ranges and service-ranges.\
            Note: Requesting to show rules as ranges is limited up to 20 rules per request, otherwise an error is returned.\
            If you wish to request more rules, use the offset and limit parameters to limit your request.
            show_hits (bool, optional): N/A
            use_object_dictionnary (bool, optional): N/A
            hits_settings (dict, optional): N/A

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **show_membership (bool, optional):
                Indicates whether to calculate and show "groups" field for every object in reply.
            **dereference_group_members (bool, optional):
                Indicates whether to dereference "members" field by details level for every object in reply.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.access_control_nat.access_rule.show_access_rulebase()

        """

        if show_all:
            return self._show_all_access_rulebase(
                name=name,
                uid=uid,
                filter_results=filter_results,
                filter_settings=filter_settings,
                limit=limit,
                order=order,
                package=package,
                show_as_ranges=show_as_ranges,
                show_hits=show_hits,
                use_object_dictionnary=use_object_dictionnary,
                hits_settings=hits_settings,
                **kw,
            )
        else:
            return self._show_partial_access_rulebase(
                name=name,
                uid=uid,
                filter_results=filter_results,
                filter_settings=filter_settings,
                limit=limit,
                offset=offset,
                order=order,
                package=package,
                show_as_ranges=show_as_ranges,
                show_hits=show_hits,
                use_object_dictionnary=use_object_dictionnary,
                hits_settings=hits_settings,
                **kw,
            )

    def _show_partial_access_rulebase(
        self,
        name: str = None,
        uid: str = None,
        filter_results: str = None,
        filter_settings: dict = None,
        limit: int = 50,
        offset: int = 0,
        order: List[dict] = None,
        package: str = None,
        show_as_ranges: bool = False,
        show_hits: bool = None,
        use_object_dictionnary: bool = None,
        hits_settings: dict = None,
        **kw,
    ) -> Box:
        """Retrieve partially objects

        Args:
            name (str, optional): Object name. Must be unique in the domain.
            uid (str, optional): Object unique identifier.
            filter_results (str, optional): Search expression to filter objects by.\
            The provided text should be exactly the same as it would be given in SmartConsole Object Explorer.\
            The logical operators in the expression ('AND', 'OR') should be provided in capital letters.\
            he search involves both a IP search and a textual search in name, comment, tags etc.
            filter_settings (str, optional): Sets filter preferences.
            limit (int, optional): The maximal number of returned results. Defaults to 50 (between 1 and 500)
            offset (int, optional): Number of the results to initially skip. Defaults to 0
            order (List[dict], optional): Sorts results by the given field. By default the results are sorted in the \
            descending order by the session publish time.
            package (str, optional): Name of the package.
            show_as_ranges (bool, optional): When true, the source, destination and services & applications parameters are\
            displayed as ranges of IP addresses and port numbers rather than network objects. Objects that are not represented\
            using IP addresses or port numbers are presented as objects. In addition, the response of each rule does not\
            contain the parameters: source, source-negate, destination, destination-negate, service and service-negate,\
            but instead it contains the parameters: source-ranges, destination-ranges and service-ranges.\
            Note: Requesting to show rules as ranges is limited up to 20 rules per request, otherwise an error is returned.\
            If you wish to request more rules, use the offset and limit parameters to limit your request.
            show_hits (bool, optional): N/A
            use_object_dictionnary (bool, optional): N/A
            hits_settings (dict, optional): N/A

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **show_membership (bool, optional):
                Indicates whether to calculate and show "groups" field for every object in reply.
            **dereference_group_members (bool, optional):
                Indicates whether to dereference "members" field by details level for every object in reply.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.access_control_nat.access_rule._show_partial_access_rulebase()
        """
        # Main request parameters
        payload = {}
        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        if filter_results is not None:
            payload["filter"] = filter_results
        if filter_settings is not None:
            payload["filter-settings"] = filter_settings
        if limit is not None:
            payload["limit"] = limit
        if offset is not None:
            payload["offset"] = offset
        if order is not None:
            payload["order"] = order
        if package is not None:
            payload["package"] = package
        if show_as_ranges is not None:
            payload["show-as-ranges"] = show_as_ranges
        if show_hits is not None:
            payload["show-hits"] = show_hits
        if use_object_dictionnary is not None:
            payload["use-object-dictionnary"] = use_object_dictionnary
        if hits_settings is not None:
            payload["hits-settings"] = hits_settings

        # Secondary parameters
        secondary_parameters = {
            "dereference_group_members": bool,
            "details_level": str,
            "show_membership": bool,
        }

        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("show-access-rulebase", json=payload)

    def _show_all_access_rulebase(
        self,
        name: str = None,
        uid: str = None,
        filter_results: str = None,
        filter_settings: dict = None,
        limit: int = 50,
        order: List[dict] = None,
        package: str = None,
        show_as_ranges: bool = False,
        show_hits: bool = None,
        use_object_dictionnary: bool = None,
        hits_settings: dict = None,
        **kw,
    ) -> Box:
        """Retrieve all objects

        Args:
            name (str, optional): Object name. Must be unique in the domain.
            uid (str, optional): Object unique identifier.
            filter_results (str, optional): Search expression to filter objects by.\
            The provided text should be exactly the same as it would be given in SmartConsole Object Explorer.\
            The logical operators in the expression ('AND', 'OR') should be provided in capital letters.\
            he search involves both a IP search and a textual search in name, comment, tags etc.
            filter_settings (str, optional): Sets filter preferences.
            limit (int, optional): The maximal number of returned results. Defaults to 50 (between 1 and 500)
            offset (int, optional): Number of the results to initially skip. Defaults to 0
            order (List[dict], optional): Sorts results by the given field. By default the results are sorted in the \
            descending order by the session publish time.
            package (str, optional): Name of the package.
            show_as_ranges (bool, optional): When true, the source, destination and services & applications parameters are\
            displayed as ranges of IP addresses and port numbers rather than network objects. Objects that are not represented\
            using IP addresses or port numbers are presented as objects. In addition, the response of each rule does not\
            contain the parameters: source, source-negate, destination, destination-negate, service and service-negate,\
            but instead it contains the parameters: source-ranges, destination-ranges and service-ranges.\
            Note: Requesting to show rules as ranges is limited up to 20 rules per request, otherwise an error is returned.\
            If you wish to request more rules, use the offset and limit parameters to limit your request.
            show_hits (bool, optional): N/A
            use_object_dictionnary (bool, optional): N/A
            hits_settings (dict, optional): N/A

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **show_membership (bool, optional):
                Indicates whether to calculate and show "groups" field for every object in reply.
            **dereference_group_members (bool, optional):
                Indicates whether to dereference "members" field by details level for every object in reply.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.access_control_nat.access_rule._show_all_access_rulebase()
        """
        all_rules = None

        # Get a timer
        timer_start = time.time()

        # Made a first request to determine the total number of objects
        resp = self._show_partial_access_rulebase(
            name=name,
            uid=uid,
            filter_results=filter_results,
            filter_settings=filter_settings,
            limit=limit,
            offset=0,
            order=order,
            package=package,
            show_as_ranges=show_as_ranges,
            show_hits=show_hits,
            use_object_dictionnary=use_object_dictionnary,
            hits_settings=hits_settings,
            **kw,
        )

        # Add the first results
        all_rules = resp

        # Evaluate the number of requests to be done
        number_requests = int(resp.total / limit) + 1

        logger.info(
            "access-rules - Total: "
            + str(resp.total)
            + " - Number of requests to do: "
            + str(number_requests)
            + " (limit set to "
            + str(limit)
            + "/request) - In progress..."
        )
        logger.debug(
            "access-rules - 1/"
            + str(number_requests)
            + " (limit set to "
            + str(limit)
            + "/request) exported... (offset:0)"
        )

        for i in range(1, number_requests):
            resp = self._show_partial_access_rulebase(
                name=name,
                uid=uid,
                filter_results=filter_results,
                filter_settings=filter_settings,
                limit=limit,
                offset=i * limit,
                order=order,
                package=package,
                show_as_ranges=show_as_ranges,
                show_hits=show_hits,
                use_object_dictionnary=use_object_dictionnary,
                hits_settings=hits_settings,
                **kw,
            )

            logger.debug(
                "access-rules - "
                + str(i + 1)
                + "/"
                + str(number_requests)
                + " (limit set to "
                + str(limit)
                + "/request) exported... (offset:"
                + str(i)
                + ")"
            )

            all_rules.rulebase += resp.rulebase

        # Finalize the output
        all_rules.to = all_rules.total

        # End timer
        timer_diff = time.time() - timer_start

        timer_text = ""

        if round(timer_diff % 60) != 0:
            timer_text = (
                str(int(timer_diff / 60)) + "min " + str(round(timer_diff % 60)) + "s"
            )  # pragma: no cover
        else:
            timer_text = "<1s"

        logger.info(
            "access-rules - Total: "
            + str(resp.total)
            + " - Number of requests done: "
            + str(number_requests)
            + " (limit set to "
            + str(limit)
            + "/request) - Done in "
            + timer_text
        )

        return all_rules
