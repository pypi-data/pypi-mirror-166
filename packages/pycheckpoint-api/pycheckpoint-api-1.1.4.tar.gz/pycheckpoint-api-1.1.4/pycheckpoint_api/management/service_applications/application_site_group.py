from typing import List, Union

from box import Box

from pycheckpoint_api.models import Color
from pycheckpoint_api.utils import sanitize_secondary_parameters

from ..abstract.network_object import NetworkObject
from ..exception import MandatoryFieldMissing


class ApplicationSiteGroup(NetworkObject):
    def add(
        self,
        name: str,
        members: Union[str, List[str]] = None,
        tags: Union[str, List[str]] = None,
        **kw
    ) -> Box:
        """
        Create new object.

        Args:
            name (str): Object name. Must be unique in the domain.
            members (Union[str, List[str]], optional): Collection of Service objects identified by the name or UID.
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
            >>> management.service_applications.application_site_group.add(
            ... name="New Application Site Group 1",
            ... members=[
            ...     "facebook",
            ...     "Social Networking",
            ...     "New Application Site 1",
            ...     "New Application Site Category 1",
            ... ],
            ... tags=["t1"],)
        """

        # Main request parameters
        payload = {"name": name}
        if members is not None:
            payload["members"] = members
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

        return self._post("add-application-site-group", json=payload)

    def show(
        self, uid: str = None, name: str = None, show_as_ranges: bool = False, **kw
    ) -> Box:
        """
        Retrieve existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.
            show_as_ranges (bool, optional, optional): When true, the group's matched content is displayed as ranges of IP\
            addresses rather than network objects. Objects that are not represented using IP addresses are presented as \
            objects. The 'members' parameter is omitted from the response and instead the 'ranges' parameter is displayed.\
            Defaults to False.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> Management.service_applications.application_site_group.show(
            ... uid="ed997ff8-6709-4d71-a713-99bf01711cd5")
        """
        return self.show_object(
            endpoint="show-application-site-group", uid=uid, name=name, **kw
        )

    def set(
        self,
        uid: str = None,
        name: str = None,
        members: Union[dict, str, List[str]] = None,
        new_name: str = None,
        tags: Union[str, List[str]] = None,
        **kw
    ) -> Box:
        """
        Edit existing object using object name or uid.

        Args:
            uid (str, optional): Object unique identifier.
            name (str, optional): Object name.
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
            >>> management.service_applications.application_site_group.set(
            ... uid="5a2d5c36-1998-2022-acce-a5c3b699d522",
            ... new_name="New Application Site Group 1",
            ... members=["https"],
            ... groups=["My Service Group1", "My Service Group2"],
            ... tags=["t1"],)
        """

        # Main request parameters
        payload = {}
        if uid is not None:
            payload["uid"] = uid
        elif name is not None:
            payload["name"] = name
        else:
            raise MandatoryFieldMissing("uid or name")

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

        return self._post("set-application-site-group", json=payload)

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
            >>> Management.service_applications.application_site_group.delete(
            ... uid="ed997ff8-6709-4d71-a713-99bf01711cd5")
        """
        return self.delete_object(
            endpoint="delete-application-site-group", uid=uid, name=name, **kw
        )

    def show_application_site_groups(
        self,
        filter_results: str = None,
        limit: int = 50,
        offset: int = 0,
        order: List[dict] = None,
        **kw
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
            show_as_ranges (bool, optional): When true, the group's matched content is displayed as ranges of IP addresses \
            rather than network objects. Objects that are not represented using IP addresses are presented as objects.\
            The 'members' parameter is omitted from the response and instead the 'ranges' parameter is displayed.\
            Defaults to False.

        Keyword Args:
            **details_level (str, optional):
                The level of detail for some of the fields in the response can vary from showing only the UID value\
                of the object to a fully detailed representation of the object.
            **domains_to_process (List[str], optional):
                Indicates which domains to process the commands on. It cannot be used with the details_level full,\
                must be run from the System Domain only and with ignore_warnings true.\
                Valid values are: CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
            **dereference_group_members (bool, optional):
                Indicates whether to dereference "members" field by details level for every object in reply.
            **show_membership (bool, optional):
                Indicates whether to calculate and show "groups" field for every object in reply.

        Returns:
            :obj:`Box`: The response from the server

        Examples:
            >>> Management.service_applications.application_site_group.show_application_site_groups()
        """
        return self.show_objects(
            endpoint="show-application-site-groups",
            filter_results=filter_results,
            limit=limit,
            offset=offset,
            order=order,
            extra_secondary_parameters={
                "dereference_group_members": bool,
                "show_membership": bool,
                "domains_to_process": List[str],
            },
            **kw
        )
