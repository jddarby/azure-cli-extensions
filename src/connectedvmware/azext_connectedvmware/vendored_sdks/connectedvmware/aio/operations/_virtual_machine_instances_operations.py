# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar, Union

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.polling import AsyncLROPoller, AsyncNoPolling, AsyncPollingMethod
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.async_arm_polling import AsyncARMPolling

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._virtual_machine_instances_operations import build_create_or_update_request_initial, build_delete_request_initial, build_get_request, build_list_request, build_restart_request_initial, build_start_request_initial, build_stop_request_initial, build_update_request_initial
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class VirtualMachineInstancesOperations:
    """VirtualMachineInstancesOperations async operations.

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

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    async def _create_or_update_initial(
        self,
        resource_uri: str,
        body: Optional["_models.VirtualMachineInstance"] = None,
        **kwargs: Any
    ) -> "_models.VirtualMachineInstance":
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.VirtualMachineInstance"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'VirtualMachineInstance')
        else:
            _json = None

        request = build_create_or_update_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._create_or_update_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    _create_or_update_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore


    @distributed_trace_async
    async def begin_create_or_update(
        self,
        resource_uri: str,
        body: Optional["_models.VirtualMachineInstance"] = None,
        **kwargs: Any
    ) -> AsyncLROPoller["_models.VirtualMachineInstance"]:
        """Implements virtual machine PUT method.

        The operation to create or update a virtual machine instance. Please note some properties can
        be set only during virtual machine instance creation.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :param body: Request payload.
        :type body: ~azure.mgmt.connectedvmware.models.VirtualMachineInstance
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either VirtualMachineInstance or the result
         of cls(response)
        :rtype:
         ~azure.core.polling.AsyncLROPoller[~azure.mgmt.connectedvmware.models.VirtualMachineInstance]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.VirtualMachineInstance"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._create_or_update_initial(
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
            deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'azure-async-operation'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_create_or_update.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore

    @distributed_trace_async
    async def get(
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> "_models.VirtualMachineInstance":
        """Gets a virtual machine.

        Retrieves information about a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: VirtualMachineInstance, or the result of cls(response)
        :rtype: ~azure.mgmt.connectedvmware.models.VirtualMachineInstance
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.VirtualMachineInstance"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str

        
        request = build_get_request(
            resource_uri=resource_uri,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore


    async def _update_initial(
        self,
        resource_uri: str,
        body: Optional["_models.VirtualMachineInstanceUpdate"] = None,
        **kwargs: Any
    ) -> Optional["_models.VirtualMachineInstance"]:
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.VirtualMachineInstance"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'VirtualMachineInstanceUpdate')
        else:
            _json = None

        request = build_update_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._update_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = None
        response_headers = {}
        if response.status_code == 200:
            deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)

        if response.status_code == 202:
            response_headers['Location']=self._deserialize('str', response.headers.get('Location'))
            

        if cls:
            return cls(pipeline_response, deserialized, response_headers)

        return deserialized

    _update_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore


    @distributed_trace_async
    async def begin_update(
        self,
        resource_uri: str,
        body: Optional["_models.VirtualMachineInstanceUpdate"] = None,
        **kwargs: Any
    ) -> AsyncLROPoller["_models.VirtualMachineInstance"]:
        """Updates a virtual machine.

        The operation to update a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :param body: Resource properties to update.
        :type body: ~azure.mgmt.connectedvmware.models.VirtualMachineInstanceUpdate
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either VirtualMachineInstance or the result
         of cls(response)
        :rtype:
         ~azure.core.polling.AsyncLROPoller[~azure.mgmt.connectedvmware.models.VirtualMachineInstance]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.VirtualMachineInstance"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._update_initial(
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
            deserialized = self._deserialize('VirtualMachineInstance', pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'azure-async-operation'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_update.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore

    async def _delete_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        delete_from_host: Optional[bool] = None,
        force: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str

        
        request = build_delete_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            delete_from_host=delete_from_host,
            force=force,
            template_url=self._delete_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
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

    _delete_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore


    @distributed_trace_async
    async def begin_delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        delete_from_host: Optional[bool] = None,
        force: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Deletes an virtual machine.

        The operation to delete a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :param delete_from_host: Whether to delete the VM from the vCenter.
        :type delete_from_host: bool
        :param force: Whether force delete was specified.
        :type force: bool
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._delete_initial(
                resource_uri=resource_uri,
                delete_from_host=delete_from_host,
                force=force,
                api_version=api_version,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'azure-async-operation'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_delete.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default"}  # type: ignore

    @distributed_trace
    def list(
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.VirtualMachineInstancesList"]:
        """Implements List virtual machine instances.

        Lists all of the virtual machine instances within the specified parent resource.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either VirtualMachineInstancesList or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.connectedvmware.models.VirtualMachineInstancesList]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.VirtualMachineInstancesList"]
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

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("VirtualMachineInstancesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
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


        return AsyncItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances"}  # type: ignore

    async def _stop_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        body: Optional["_models.StopVirtualMachineOptions"] = None,
        **kwargs: Any
    ) -> None:
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'StopVirtualMachineOptions')
        else:
            _json = None

        request = build_stop_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._stop_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        response_headers = {}
        response_headers['Location']=self._deserialize('str', response.headers.get('Location'))


        if cls:
            return cls(pipeline_response, None, response_headers)

    _stop_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/stop"}  # type: ignore


    @distributed_trace_async
    async def begin_stop(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        body: Optional["_models.StopVirtualMachineOptions"] = None,
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Implements the operation to stop a virtual machine.

        The operation to power off (stop) a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :param body: Virtualmachine stop action payload.
        :type body: ~azure.mgmt.connectedvmware.models.StopVirtualMachineOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._stop_initial(
                resource_uri=resource_uri,
                body=body,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'location'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_stop.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/stop"}  # type: ignore

    async def _start_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> None:
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str

        
        request = build_start_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            template_url=self._start_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        response_headers = {}
        response_headers['Location']=self._deserialize('str', response.headers.get('Location'))


        if cls:
            return cls(pipeline_response, None, response_headers)

    _start_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/start"}  # type: ignore


    @distributed_trace_async
    async def begin_start(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Implements the operation to start a virtual machine.

        The operation to start a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._start_initial(
                resource_uri=resource_uri,
                api_version=api_version,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'location'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_start.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/start"}  # type: ignore

    async def _restart_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> None:
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str

        
        request = build_restart_request_initial(
            resource_uri=resource_uri,
            api_version=api_version,
            template_url=self._restart_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        response_headers = {}
        response_headers['Location']=self._deserialize('str', response.headers.get('Location'))


        if cls:
            return cls(pipeline_response, None, response_headers)

    _restart_initial.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/restart"}  # type: ignore


    @distributed_trace_async
    async def begin_restart(  # pylint: disable=inconsistent-return-statements
        self,
        resource_uri: str,
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Implements the operation to restart a virtual machine.

        The operation to restart a virtual machine instance.

        :param resource_uri: The fully qualified Azure Resource manager identifier of the Hybrid
         Compute machine resource to be extended.
        :type resource_uri: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-03-01-preview")  # type: str
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._restart_initial(
                resource_uri=resource_uri,
                api_version=api_version,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = AsyncARMPolling(lro_delay, lro_options={'final-state-via': 'location'}, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_restart.metadata = {'url': "/{resourceUri}/providers/Microsoft.ConnectedVMwarevSphere/virtualMachineInstances/default/restart"}  # type: ignore
