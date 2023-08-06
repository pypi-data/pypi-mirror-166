from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list_paginated as _list_paginated, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "missions/steps"


def list(session: Session = None, **filters):
    """
    List a array of steps

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of steps

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="step name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def list_paginated(session: Session = None, **filters):
    """
    List iterator of pages of steps

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of steps

    Returns:
      result (json): returns the result of the request as json by page

    Example:
      >>> next(list(page=1,page_size=10,name="step name"))
    """
    result = _list_paginated(resource=RESOURCE, session=session,
                             version="v2", **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a step by uuid

    Args:
      uuid (string): step uuid to retrieve
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _retrieve(RESOURCE, id=uuid, session=session, version="v2")
    return result


def update(uuid: str, model: Dict, session: Session = None):
    """
    Update a step by passing uuid and an model (Data to update)

    (Only super step can do it!)

    Args:
      uuid (string): step uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on step
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> update("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", { "name": "new name" })
    """
    result = _update(RESOURCE, id=uuid, payload=model,
                     session=session,  version="v2")
    return result


def create(model: Dict, session: Session = None):
    """
    Create a step by passing an model (Data)

    (Only super step can do it!)

    Args:
      model (Dict): A dictionary with the data the will be used to create an step
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session, version="v2")
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a step by passing uuid

    (Only super step can do it!)

    Args:
      uuid (string): step uuid to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session, version="v2")
    return result
