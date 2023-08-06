from typing import Dict
import json
from sara_sdk.common.session import Session
from ...utils.rest import list as _list, list_paginated as _list_paginated, create as _create

RESOURCE = "missions"


def list(session: Session = None, **filters):
    """
    List a array of missions

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of missions

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="mission name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def list_paginated(session: Session = None, **filters):
    """
    List iterator of pages of missions

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of missions

    Returns:
      result (json): returns the result of the request as json by page

    Example:
      >>> next(list(page=1,page_size=10,name="mission name"))
    """
    result = _list_paginated(resource=RESOURCE, session=session,
                             version="v2", **filters)
    return result


def last(robot: str, session: Session = None):
    """
    Retrieve the last mission by robot id

    Args:
      robot (UUID): robot to return a mission
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _list(RESOURCE+"/last", session=session,
                   version="v2", robot_id=robot)
    return result


def create(robot: str, stages: Dict, session: Session = None):
    """
    Create a mission by passing an model (Data)

    Args:
      robot (UUID): robot uuid to create mission
      stages (Dict): A dictionary with the data the will be used to create an mission
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    model = {
        "robot": robot,
        "stages": json.dumps(stages)
    }
    result = _create(RESOURCE, payload=model, session=session, version="v2")
    return result
