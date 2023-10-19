# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING

from msrest import Serializer

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.polling import LROPoller, NoPolling, PollingMethod
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.arm_polling import ARMPolling

from .. import models as _models
from .._vendor import _convert_request, _format_url_section

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Iterable, Optional, TypeVar, Union
    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False
# fmt: off

def build_create_request_initial(
    resource_uri,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default")  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceUri": _SERIALIZER.url("resource_uri", resource_uri, 'str', skip_quote=True),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        _header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="PUT",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_get_request(
    resource_uri,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default")  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceUri": _SERIALIZER.url("resource_uri", resource_uri, 'str', skip_quote=True),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_delete_request_initial(
    resource_uri,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default")  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceUri": _SERIALIZER.url("resource_uri", resource_uri, 'str', skip_quote=True),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="DELETE",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_list_request(
    resource_uri,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents")  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceUri": _SERIALIZER.url("resource_uri", resource_uri, 'str', skip_quote=True),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )

# fmt: on
class VMInstanceGuestAgentsOperations(object):
    """VMInstanceGuestAgentsOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.connectedvmware.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def _create_initial(
        self,
        resource_uri,  # type: str
        body=None,  # type: Optional["_models.GuestAgent"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.GuestAgent"
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.GuestAgent"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'GuestAgent')
        else:
            _json = None

        request = build_create_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._create_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('GuestAgent', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('GuestAgent', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    _create_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default"}  # type: ignore


    @distributed_trace
    def begin_create(
        self,
        resource_uri,  # type: str
        body=None,  # type: Optional["_models.GuestAgent"]
        **kwargs  # type: Any
    ):
        # type: (...) -> LROPoller["_models.GuestAgent"]
        """Implements GuestAgent PUT method.

        Create Or Update GuestAgent.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :param body: Request payload.
        :type body: ~azure.mgmt.connectedvmware.models.GuestAgent
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either GuestAgent or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.connectedvmware.models.GuestAgent]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.GuestAgent"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = self._create_initial(
                resource_uri=resource_uri,
                body=body,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            response = pipeline_response.http_response
            deserialized = self._deserialize('GuestAgent', pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized


        if polling is True: polling_method = ARMPolling(lro_delay, lro_options={'final-state-via': 'azure-async-operation'}, **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_create.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default"}  # type: ignore

    @distributed_trace
    def get(
        self,
        resource_uri,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.GuestAgent"
        """Gets GuestAgent.

        Implements GuestAgent GET method.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: GuestAgent, or the result of cls(response)
        :rtype: ~azure.mgmt.connectedvmware.models.GuestAgent
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.GuestAgent"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        
        request = build_get_request(
            resource_uri=resource_uri,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('GuestAgent', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default"}  # type: ignore


    def _delete_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        
        request = build_delete_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            template_url=self._delete_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        response_headers = {}
        if response.status_code == 202:
            response_headers['Location']=self._deserialize('str', response.headers.get('Location'))
            

        if cls:
            return cls(pipeline_response, None, response_headers)

    _delete_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default"}  # type: ignore


    @distributed_trace
    def begin_delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> LROPoller[None]
        """Deletes an GuestAgent.

        Implements GuestAgent DELETE method.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = self._delete_initial(
                resource_uri=resource_uri,
                api_version=api_version,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = ARMPolling(lro_delay, **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_delete.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents/default"}  # type: ignore

    @distributed_trace
    def list(
        self,
        resource_uri,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["_models.GuestAgentList"]
        """Implements GET GuestAgent in a vm.

        Returns the list of GuestAgent of the given vm.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either GuestAgentList or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.connectedvmware.models.GuestAgentList]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.GuestAgentList"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_request(
                    resource_uri=resource_uri,
                    api_version=api_version,
                    template_url=self.list.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_request(
                    resource_uri=resource_uri,
                    api_version=api_version,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize("GuestAgentList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response


        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/guestAgents"}  # type: ignore
