from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import attach, detach, retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "iam/policies"


def list(session: Session = None, **filters):
    """
    List a array of policies

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of policies

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="policy name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a policy by uuid

    Args:
      uuid (string): policy uuid to retrieve
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
    Update a policy by passing uuid and an model (Data to update)

    Args:
      uuid (string): policy uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on policy
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
    Create a policy by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an policy
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a policy by passing uuid

    Args:
      uuid (string): policy uuid to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session)
    return result


def attachAction(action: str, policy: str, session: Session = None):
    """
    Attach a action to a policy

    Args:
      action (string): action uuid to attach on policy
      policy (string): policy uuid that the action is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachAction("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="actions", this=action,
                    that=policy, session=session)
    return result


def detachAction(action: str, policy: str, session: Session = None):
    """
    Detach a action from a policy

    Args:
      action (string): action uuid to detach from policy
      policy (string): policy uuid that the action is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachAction("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="actions", this=action,
                    that=policy, session=session)
    return result
