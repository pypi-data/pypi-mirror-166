from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create, attach, detach

RESOURCE = "iam/fleets"


def list(session: Session = None, **filters):
    """
    List a array of fleets

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of fleets

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="fleetname")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a fleet by uuid

    Args:
      uuid (string): fleet uuid to retrieve
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
    Update a fleet by passing uuid and an model (Data to update)

    Args:
      uuid (string): fleet uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on fleet
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
    Create a fleet by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an fleet
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a fleet by passing uuid

    Args:
      uuid (string): fleet uuid to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session)
    return result


def attachRobot(robot: str, fleet: str, session: Session = None):
    """
    Attach a robot to a fleet

    Args:
      robot (string): robot uuid to attach on fleet
      fleet (string): fleet uuid that the robot is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachRobot("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="robot", this=robot,
                    that=fleet, session=session)
    return result


def detachRobot(robot: str, fleet: str, session: Session = None):
    """
    Detach a robot from a fleet

    Args:
      robot (string): robot uuid to detach from fleet
      fleet (string): fleet uuid that the robot is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachRobot("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="robot", this=robot,
                    that=fleet, session=session)
    return result
