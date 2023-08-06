from typing import Dict

from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create

RESOURCE = "iam/users"


def list(session: Session = None, **filters):
    """
    List a array of users

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of users

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="user name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def retrieve(uuid: str, session: Session = None):
    """
    Retrieve a user by uuid

    Args:
      uuid (string): user uuid to retrieve
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
    Update a user by passing uuid and an model (Data to update)

    Args:
      uuid (string): user uuid to retrieve
      model (Dict): A dictionary with the data the will be updated on user
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
    Create a user by passing an model (Data)

    Args:
      model (Dict): A dictionary with the data the will be used to create an user
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json
    """
    result = _create(RESOURCE, payload=model, session=session)
    return result


def delete(uuid: str, session: Session = None):
    """
    Delete a user by passing uuid

    Args:
      uuid (string): user uuid to delete
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> delete("f8b85a7a-4540-4d46-a2ed-00e6134ee84a")
    """
    result = _delete(RESOURCE, id=uuid, session=session)
    return result


def me(session: Session = None):
    """
    Get the data from the user logged

    Args:
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> me()
    """
    result = _retrieve(RESOURCE, id="me", session=session)
    return result


def verifyUserByEmail(email: str, session: Session = None):
    """
    Verify user by email

    Args:
      email (string): email to validate
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> verifyUserByEmail("email@dominio.com")
    """
    result = _retrieve(RESOURCE, id="verifyUserByEmail",
                       session=session, email=email)
    return result
