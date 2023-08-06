from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "iam/apps"


def list(session: Session = None):
    """
    List a array of apps

    Args:
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list()
    """
    result = _list(RESOURCE, session=session)
    return result


def retrieve(id: str, session: Session = None):
    """
    Retrieve an app by id

    Args:
      id (string): app uuid to retrieve
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> retrieve("721o83iusldua3c2fls61p9i32")
    """
    result = _retrieve(RESOURCE, id=id, session=session)
    return result


def create(model: Dict, session: Session = None):
    """
    Create a app by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an app
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result


def delete(id: str, session: Session = None):
    """
    Delete a app by passing id

    Args:
      id (string): app id to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("721o83iusldua3c2fls61p9i32")
    """
    result = _delete(RESOURCE, id=id, session=session)
    return result
