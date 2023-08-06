from requests import get, post, delete as _delete, patch
from ..client.requests import fetch


def retrieve(resource, id, session=None, **kwargs):
    """
    Retrieve function to request a GET passing id to the API

    Args:
        resource (string): the route to access on the api
        id (string): uuid to the resource
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        kwargs (any): will be used as query to the route

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> retrieve(resource="iam/robots", "09594aae-7e88-4c8b-b4e5-095c6e785509")
    """
    path = "{endpoint}/{id}".format(endpoint=resource, id=id)
    json = fetch(method=get, path=path, query=kwargs, session=session).json()
    return json


def list_paginated(resource, session=None, version="v1", **kwargs):
    """
    List function to request a GET to receive a list of objects

    Args:
        resource (string): the route to access on the api
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        kwargs (any): will be used as query to the route

    Returns:
        Json: The json of the content results of the response sended by the api

    Example:
        >>> list(resource="iam/robots")
    """
    page = kwargs.get("page", 1)

    while True:
        json = fetch(method=get, path=resource, query={
                     **kwargs, "page": page}, session=session, version=version).json()
        yield json.get("results", [])
        if json.get("next") is None:
            break
        page += 1


def list(resource, session=None, version="v1", **kwargs):
    """
    List function to request a GET to receive a list of objects

    Args:
        resource (string): the route to access on the api
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        kwargs (any): will be used as query to the route

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> list(resource="iam/robots")
    """
    json = fetch(method=get, path=resource,
                 query=kwargs, session=session, version=version).json()
    return json


def create(resource, payload, session=None, version="v1", **kwargs):
    """
    Create function to request a POST to create a new instance of resource

    Args:
        resource (string): the route to access on the api
        payload (Dict): A dict with data to use to create the new resource
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        kwargs (any): will be used as query to the route

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> create(resource="iam/robots", **kwargs)
    """
    json = fetch(method=post, path=resource, session=session,
                 query=kwargs, payload=payload, version=version).json()
    return json


def delete(resource, id, session=None, version="v1"):
    """
    Delete function to request a DELETE passing id to the API

    Args:
        resource (string): the route to access on the api
        id (string): uuid to the resource
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        kwargs (any): will be used as query to the route

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> delete(resource="iam/robots", "09594aae-7e88-4c8b-b4e5-095c6e785509")
    """
    path = "{endpoint}/{id}".format(endpoint=resource, id=id)
    json = fetch(method=_delete, path=path,
                 session=session, version=version).json()
    return json


def update(resource, id, payload, session=None, version="v1"):
    """
    Delete function to request a DELETE passing id to the API

    Args:
        resource (string): the route to access on the api
        id (string): uuid to the resource
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        payload (Dict): A dict with data to use to update the resource

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> delete(resource="iam/robots", "09594aae-7e88-4c8b-b4e5-095c6e785509", **payload)
    """
    path = "{endpoint}/{id}".format(endpoint=resource, id=id)
    json = fetch(method=patch, path=path,
                 payload=payload, session=session, version=version).json()
    return json


def attach(resource, type, this, that, session=None, version="v1"):
    """
    Attach function to attach something (this) to other entity (that)

    Args:
        resource (string): the route to access on the api
        type (string): type of entity that is going to be attach
        this (string): an uuid from the thing that is going to be attach to the entity
        that (string): uuid from the entity
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> attach("iam/groups", "user", "9871a24a-89ff-4ba1-a350-458244e8244d", "00ea03f1-5b2e-4787-8aa6-745961c6d506")
    """
    body = {
        type: this
    }

    # Workaround to userGroup route
    if type == "user" and resource == "iam/groups":
        type = "UserGroup"

    if type == "actions" and resource == "iam/policies":
        type = "Permissions"

    path = "{endpoint}/{that}/attach{type}".format(
        endpoint=resource, that=that, type=type.capitalize())

    if resource == "iam/clients":
        body = {
            type: this,
            'client': that
        }
        path = "{endpoint}/attach{type}".format(
            endpoint=resource, type=type.capitalize())

    json = fetch(method=post, path=path, payload=body,
                 session=session, version=version).json()
    return json


def detach(resource, type, this, that, session=None, version="v1"):
    """
    Attach function to detach something (this) from other entity (that)

    Args:
        resource (string): the route to access on the api
        type (string): type of entity that is going to be detach
        this (string): an uuid from the thing that is going to be detach from the entity
        that (string): uuid from the entity
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)

    Returns:
        Json: The json of the content of the response sended by the api

    Example:
        >>> detach("iam/groups", "user", "9871a24a-89ff-4ba1-a350-458244e8244d", "00ea03f1-5b2e-4787-8aa6-745961c6d506")
    """

    body = {
        type: this
    }

    # Workaround to userGroup route
    if type == "user" and resource == "iam/groups":
        type = "UserGroup"

    if type == "actions" and resource == "iam/policies":
        type = "Action"

    path = "{endpoint}/{that}/attach{type}".format(
        endpoint=resource, that=that, type=type.capitalize())

    if resource == "iam/clients":
        body = {
            type: this,
            'client': that
        }
        path = "{endpoint}/attach{type}".format(
            endpoint=resource, type=type.capitalize())

    json = fetch(method=_delete, path=path,
                 payload=body, session=session, version="v1").json()
    return json
