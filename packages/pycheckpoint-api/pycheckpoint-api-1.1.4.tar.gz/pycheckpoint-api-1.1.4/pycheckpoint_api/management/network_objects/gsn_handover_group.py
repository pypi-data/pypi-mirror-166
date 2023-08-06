from typing import List, Union

from box import Box

from pycheckpoint_api.models import Color
from pycheckpoint_api.utils import sanitize_secondary_parameters

from ..abstract.network_object import NetworkObject
from ..exception import MandatoryFieldMissing


class GSNHandoverGroup(NetworkObject):
    def add(
        self,
        name: str,
        enforce_gtp: bool = None,
        gtp_rate: int = None,
        members: Union[str, List[str]] = None,
        tags: Union[str, List[str]] = None,
        **kw,
    ) -> Box:
        """
        Create new object.

        Args:
            name (str): Object name. Must be unique in the domain.
            enforce_gtp (bool, optional): Enable enforce GTP signal packet rate limit from this group.
            gtp_rate (int, optional): Limit of the GTP rate in PDU/sec.
            members (Union[str, List[str]], optional): Collection of Network objects identified by the name or UID.
            tags (Union(str,List[str]), optional): Collection of tag identifiers.

        Keyword Args:
            **set_if_exists (bool, optional):
                If another object with the same identifier already exists, it will be updated.
                The command behaviour will be the same as if originally a set command was called.
                Pay attention that original object's fields will be overwritten by the fields provided in the request payload!
            **color (Color, optional):
                Color of the object. Should be one of existing colors.
            **comments (str, optional):
                Comments string.
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **groups (Union(str,List[str]), optional):
                Collection of group identifiers.
            **ignore_warnings (bool, optional):
                Apply changes ignoring warnings. Defaults to False
            **ignore_errors (bool, optional):
                Apply changes ignoring errors. You won't be able to publish such a changes.
                If ignore_warnings flag was omitted - warnings will also be ignored. Defaults to False

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.network_objects.gsn_handover_group.add(name="My object")
        """

        # Main request parameters
        payload = {"name": name}
        if enforce_gtp is not None:
            payload["enforce-gtp"] = enforce_gtp
        if gtp_rate is not None:
            payload["gtp-rate"] = gtp_rate
        if members is not None:
            payload["members"] = members
        if tags is not None:
            payload["tags"] = tags

        # Secondary parameters
        secondary_parameters = {
            "set-if-exists": bool,
            "color": Color,
            "comments": str,
            "details_level": str,
            "groups": Union[str, List[str]],
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("add-gsn-handover-group", json=payload)

    def show(self, uid: str = None, name: str = None, **kw) -> Box:
        """
        Retrieve existing object using object name or uid.

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
            >>> firewall.network_objects.gsn_handover_group.show(uid="f140a9d1-4167-456a-931d-abdaa4c8aa7e")
        """
        return self.show_object(
            endpoint="show-gsn-handover-group", uid=uid, name=name, **kw
        )

    def set(
        self,
        uid: str = None,
        name: str = None,
        enforce_gtp: bool = None,
        gtp_rate: int = None,
        members: Union[dict, str, List[str]] = None,
        new_name: str = None,
        tags: Union[str, List[str]] = None,
        **kw,
    ) -> Box:
        """
        Edit existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.
            enforce_gtp (bool, optional): Enable enforce GTP signal packet rate limit from this group.
            gtp_rate (int, optional): Limit of the GTP rate in PDU/sec.
            members (Union[dict, str, List[str]], optional): Collection of Network objects identified by the name or UID.
            new_name (str, optional): New name of the object.
            tags (Union(str,List[str]), optional): Collection of tag identifiers.

        Keyword Args:
            **color (Color, optional):
                Color of the object. Should be one of existing colors.
            **comments (str, optional):
                Comments string.
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **groups (Union(str,List[str]), optional):
                Collection of group identifiers.
            **ignore_warnings (bool, optional):
                Apply changes ignoring warnings. Defaults to False
            **ignore_errors (bool, optional):
                Apply changes ignoring errors. You won't be able to publish such a changes.
                If ignore_warnings flag was omitted - warnings will also be ignored. Defaults to False

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.network_objects.gsn_handover_group.set(uid="f140a9d1-4167-456a-931d-abdaa4c8aa7e",
            new_name="gsnhandovergroup")
        """

        # Main request parameters
        payload = {}
        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

        if enforce_gtp is not None:
            payload["enforce-gtp"] = enforce_gtp
        if gtp_rate is not None:
            payload["gtp-rate"] = gtp_rate
        if members is not None:
            payload["members"] = members
        if new_name is not None:
            payload["new-name"] = new_name
        if tags is not None:
            payload["tags"] = tags

        # Secondary parameters
        secondary_parameters = {
            "color": Color,
            "comments": str,
            "details_level": str,
            "groups": Union[str, List[str]],
            "ignore_warnings": bool,
            "ignore_errors": bool,
        }
        payload.update(sanitize_secondary_parameters(secondary_parameters, **kw))

        return self._post("set-gsn-handover-group", json=payload)

    def delete(self, uid: str = None, name: str = None, **kw) -> Box:
        """
        Delete existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.

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
            >>> firewall.network_objects.gsn_handover_group.delete(uid="f140a9d1-4167-456a-931d-abdaa4c8aa7e")
        """
        return self.delete_object(
            endpoint="delete-gsn-handover-group", uid=uid, name=name, **kw
        )

    def show_gsn_handover_groups(
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
            filter_results (str, optional): Search expression to filter objects by.\
            The provided text should be exactly the same as it would be given in SmartConsole Object Explorer.\
            The logical operators in the expression ('AND', 'OR') should be provided in capital letters.\
            he search involves both a IP search and a textual search in name, comment, tags etc.
            limit (int, optional): The maximal number of returned results. Defaults to 50 (between 1 and 500)
            offset (int, optional): Number of the results to initially skip. Defaults to 0
            order (List[dict], optional): Sorts results by the given field. By default the results are sorted in the \
            descending order by the session publish time.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> firewall.network_objects.group.show_groups()
        """
        return self.show_objects(
            endpoint="show-gsn-handover-groups",
            filter_results=filter_results,
            limit=limit,
            offset=offset,
            order=order,
            extra_secondary_parameters={
                "dereference_group_members": bool,
                "show_membership": bool,
            },
            **kw,
        )
