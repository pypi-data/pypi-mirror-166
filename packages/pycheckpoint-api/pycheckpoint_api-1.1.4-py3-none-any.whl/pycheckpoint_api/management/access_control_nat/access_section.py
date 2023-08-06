from typing import Union

from box import Box
from restfly.endpoint import APIEndpoint

from pycheckpoint_api.utils import sanitize_secondary_parameters

from ..exception import MandatoryFieldMissing


class AccessSection(APIEndpoint):
    def add(
        self,
        layer: str,
        position: Union[int, str, dict],
        name: str = None,
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
            name (str, optional): Section name.

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
            >>> management.access_control_nat.access_section.add(
            ... layer="Network",
            ... position=1,
            ... name="New Section 1",)
        """

        # Main request parameters
        payload = {"layer": layer, "position": position}

        if name is not None:
            payload["name"] = name

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("add-access-section", json=payload)

    def show(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        **kw,
    ) -> Box:
        """
        Retrieve existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            uid (str, optional): Object unique identifier. Mandatory if "rule_number" or "name" are not set.
            name (str, optional): Object name. Mandatory if "rule_number" or "uid" are not set.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_section.show(
            ... uid="aa5d88e9-a589-abba-1471-5d6988519a26",
            ... layer="MyLayer")
        """
        # Main request parameters
        payload = {"layer": layer}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        # Secondary parameters
        secondary_parameters = {"details_level": str}

        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("show-access-section", json=payload)

    def set(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        new_name: str = None,
        **kw,
    ) -> Box:
        """
        Edit existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            uid (str, optional): Object unique identifier.
            new_name (str, optional): New name of the object.
            name (str, optional): Rule name.

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
            >>> management.access_control_nat.access_section.set(
            ... layer="Network",
            ... uid="aa5d88e9-a589-abba-1471-5d6988519a26",
            ... new_name="New Section 1",)
        """

        # Main request parameters
        payload = {"layer": layer}

        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        if new_name is not None:
            payload["new-name"] = new_name

        # Secondary parameters
        secondary_parameters = {
            "details_level": str,
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("set-access-section", json=payload)

    def delete(
        self,
        layer: str,
        uid: str = None,
        name: str = None,
        **kw,
    ) -> Box:
        """
        Delete existing object using object name or uid.

        Args:
            layer (str): Layer that the rule belongs to identified by the name or UID.
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> management.access_control_nat.access_section.delete(
            ... layer="Network",
            ... uid="aa5d88e9-a589-abba-1471-5d6988519a26")
        """
        # Main request parameters
        payload = {"layer": layer}

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

        return self._post("delete-access-section", json=payload)
