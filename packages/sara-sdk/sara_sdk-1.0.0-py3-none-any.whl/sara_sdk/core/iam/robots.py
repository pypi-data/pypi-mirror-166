from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "iam/robots"


def list(session: Session = None, **filters):
    """
    List a array of robots

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of robots

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,fleet="3ddc1eb5-8433-4eca-a95d-ff2d688cc2fc")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a robot by uuid

    Args:
      uuid (string): Robot uuid to retrieve
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _retrieve(RESOURCE, id=uuid, session=session)
    return result


def update(uuid: str, model: Dict, session: Session = None,):
    """
    Update a robot by passing uuid and an model (Data to update)

    Args:
      uuid (string): Robot uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on robot
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> update("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", { "name": "new name" })
    """
    result = _update(RESOURCE, id=uuid, payload=model, session=session)
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a robot by passing uuid

    Args:
      uuid (string): Robot uuid to delete from client
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session)
    return result
