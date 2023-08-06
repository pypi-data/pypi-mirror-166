from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "iam/actions"


def list(session: Session = None, **filters):
    """
    List a array of actions

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of actions

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="action name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a action by uuid

    Args:
      uuid (string): action uuid to retrieve
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _retrieve(RESOURCE, id=uuid, session=session)
    return result


def create(model: Dict, session: Session = None):
    """
    Create a action by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an action
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result
