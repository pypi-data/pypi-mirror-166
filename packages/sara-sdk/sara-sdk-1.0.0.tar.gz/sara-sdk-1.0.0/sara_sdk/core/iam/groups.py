from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create, attach, detach

RESOURCE = "iam/groups"


def list(session: Session = None, **filters):
    """
    List a array of groups

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of groups

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="group name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a group by uuid

    Args:
      uuid (string): group uuid to retrieve
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _retrieve(RESOURCE, id=uuid, session=session)
    return result


def update(uuid: str, model: Dict, session: Session = None):
    """
    Update a group by passing uuid and an model (Data to update)

    Args:
      uuid (string): group uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on group
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> update("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", { "name": "new name" })
    """
    result = _update(RESOURCE, id=uuid, payload=model, session=session)
    return result


def create(model: Dict, session: Session = None):
    """
    Create a group by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an group
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a group by passing uuid

    Args:
      uuid (string): group uuid to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session)
    return result


def attachUser(user: str, group: str, session: Session = None):
    """
    Attach a user to a group

    Args:
      user (string): user uuid to attach on group
      group (string): group uuid that the user is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachUser("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="user", this=user,
                    that=group, session=session)
    return result


def detachUser(user: str, group: str, session: Session = None):
    """
    Detach a user from a group

    Args:
      user (string): user uuid to detach from group
      group (string): group uuid that the user is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachUser("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="user", this=user,
                    that=group, session=session)
    return result


def attachPolicy(policy: str, group: str, session: Session = None):
    """
    Attach a policy to a group

    Args:
      policy (string): policy uuid to attach on group
      group (string): group uuid that the policy is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachPolicy("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="policy", this=policy,
                    that=group, session=session)
    return result


def detachPolicy(policy: str, group: str, session: Session = None):
    """
    Detach a policy from a group

    Args:
      policy (string): policy uuid to detach from group
      group (string): group uuid that the policy is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachPolicy("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="policy", this=policy,
                    that=group, session=session)
    return result
