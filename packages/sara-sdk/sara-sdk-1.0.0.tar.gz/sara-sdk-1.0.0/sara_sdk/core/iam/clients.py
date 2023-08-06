from sara_sdk.common.session import Session
from ...utils.rest import retrieve as _retrieve, list as _list, update as _update, delete as _delete, create as _create, attach, detach

RESOURCE = "iam/clients"


def list(session: Session = None, **filters):
    """
    List a array of clients

    Args:
      session (Session): Used only if want to use a different session instead default
      filters (Any): filters to pass to filter the list of clients

    Returns:
      result (json): returns the result of the request as json

    Example:
      >>> list(page=1,page_size=10,name="client name")
    """
    result = _list(resource=RESOURCE, session=session, **filters)
    return result


def attachRobot(robot: str, client: str, session: Session = None):
    """
    Attach a robot to a client

    Args:
      robot (string): robot uuid to attach on client
      client (string): client uuid that the robot is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachRobot("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="robot", this=robot,
                    that=client, session=session)
    return result


def detachRobot(robot: str, client: str, session: Session = None):
    """
    Detach a robot from a client

    Args:
      robot (string): robot uuid to detach from client
      client (string): client uuid that the robot is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachRobot("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="robot", this=robot,
                    that=client, session=session)
    return result


def attachUser(user: str, client: str, session: Session = None):
    """
    Attach a user to a client

    Args:
      user (string): user uuid to attach on client
      client (string): client uuid that the user is going to be attached
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> attachUser("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = attach(RESOURCE, type="user", this=user,
                    that=client, session=session)
    return result


def detachUser(user: str, client: str, session: Session = None):
    """
    Detach a user from a client

    Args:
      user (string): user uuid to detach from client
      client (string): client uuid that the user is, to be detached of
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> detachUser("f8b85a7a-4540-4d46-a2ed-00e6134ee84a", f3a4d78a-4540-4d46-a2ed-00e613a65d4a)
    """
    result = detach(RESOURCE, type="user", this=user,
                    that=client, session=session)
    return result


def slug(slug: str, session=None):
    """
    Get the data of an client by passing the slug

    Args:
      slug (str): slug of the client
      session (Session): Used only if want to use a different session instead default

    Returns:
      result (json): returns the result of request as json

    Example:
      >>> slug("test-client")
    """
    result = _list("iam/slugs", session=session, pk=slug)
    return result
