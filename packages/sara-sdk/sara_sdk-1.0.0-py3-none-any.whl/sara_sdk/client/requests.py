from json import dumps, loads
from time import time
from ..utils.url import urlencode
from ..error import Error, InternalServerError, UnknownError, AuthorizationError
from sys import version_info as python_version
import sara_sdk


class Response:
    """
    Response Class to receive data from the API

    Args:
        status (number): Number of the status code send by the API
        content (bytes): The content of the response in bytes

    Returns:
        Response: An instance of Response

    Example:
        >>> Response(status=200,content=bytes("content"))
    """

    def __init__(self, status, content):
        self.status = status
        self.content = content

    def json(self):
        """
        Convert the content to JSON format

        Args:
            None

        Returns:
            The content of the Response as JSON

        Example:
            >>> result = Response.json()
            >>> print(result)
                { key: "data" }
        """
        if self.content:
            return loads(self.content.decode("utf-8"))
        else:
            return {}


def fetch(method, path, payload=None, query=None, session=None, version="v1"):
    """
    Function to do requests on sara api

    Args:
        method (Request): method of request from the python-requests package
        path (string): the url path to where the request will be send
        payload (Dict): payload to send through the request
        query (string): query to insert on the end of url request
        session (Session): session where to get the authorization (only needed if doens't want
        to use the DEFAULT_SESSION)
        version (string): the version of the api

    Returns:
        Response: the response of the API

    Examples:
        >>> fetch(method=post, path="iam/robots")
    """
    url = sara_sdk.API_URL + version

    if query is not None:
        url = "{base_url}/{path}/{query}".format(
            base_url=url, path=path, query=urlencode(query))
    else:
        url = "{base_url}/{path}/".format(
            base_url=url, path=path)

    agent = "Python-{major}.{minor}.{micro}-SDK-{sdk_version}".format(
        major=python_version.major,
        minor=python_version.minor,
        micro=python_version.micro,
        sdk_version=sara_sdk.__version__,
    )

    if session is None:
        session = sara_sdk.DEFAULT_SESSION

    access_time = time()

    # if session has expired get a new access_token
    if access_time >= session.expires_in:
        session.auth()

    body = payload
    bearer_token = "Bearer {token}".format(token=session.access_token)

    try:
        request = method(
            url=url,
            data=body,
            headers={
                "Access-Time": str(access_time),
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": agent,
                "Accept-Language": "en-US",
                "Authorization": bearer_token
            },
            timeout=sara_sdk.__timeout__
        )
    except Exception as exception:
        raise UnknownError("{}: {}".format(
            exception.__class_.__name__, str(exception)))

    response = Response(status=request.status_code, content=request.content)

    if response.status == 500:
        raise InternalServerError()
    if response.status == 400:
        raise Error(response.status, response.json()["detail"])
    if response.status == 401:
        if(session.attemps == 0):
            session.attemps += 1
            session.auth()
            fetch(method=method, path=path, payload=payload,
                  query=query, session=session, version=version)
        else:
            raise AuthorizationError()
    if response.status >= 300:
        raise UnknownError(response.content)

    return response
