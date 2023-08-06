from copy import deepcopy
from typing import Dict, List, Optional, Tuple, cast

from great_expectations.core.batch import (
    BatchDefinition,
    BatchRequest,
    BatchSpec,
    IDDict,
)
from great_expectations.core.batch_spec import SqlAlchemyDatasourceBatchSpec
from great_expectations.datasource.data_connector.batch_filter import (
    BatchFilter,
    build_batch_filter,
)
from great_expectations.datasource.data_connector.data_connector import DataConnector
from great_expectations.datasource.data_connector.util import (
    batch_definition_matches_batch_request,
)
from great_expectations.execution_engine import (
    ExecutionEngine,
    SqlAlchemyExecutionEngine,
)
from great_expectations.util import deep_filter_properties_iterable

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

try:
    from sqlalchemy.sql import Selectable
except ImportError:
    Selectable = None


class ConfiguredAssetSqlDataConnector(DataConnector):
    """
    A DataConnector that requires explicit listing of SQL tables you want to connect to.
    """

    def __init__(
        self,
        name: str,
        datasource_name: str,
        execution_engine: Optional[ExecutionEngine] = None,
        include_schema_name: bool = False,
        splitter_method: Optional[str] = None,
        splitter_kwargs: Optional[dict] = None,
        sampling_method: Optional[str] = None,
        sampling_kwargs: Optional[dict] = None,
        assets: Optional[Dict[str, dict]] = None,
        batch_spec_passthrough: Optional[dict] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        ConfiguredAssetDataConnector for connecting to data on a SQL database

        Args:
            name (str): The name of this DataConnector
            datasource_name (str): The name of the Datasource that contains it
            execution_engine (ExecutionEngine): An ExecutionEngine
            include_schema_name (bool): Should the data_asset_name include the schema as a prefix?
            splitter_method (str): A method to split the target table into multiple Batches
            splitter_kwargs (dict): Keyword arguments to pass to splitter_method
            sampling_method (str): A method to downsample within a target Batch
            sampling_kwargs (dict): Keyword arguments to pass to sampling_method
            batch_spec_passthrough (dict): dictionary with keys that will be added directly to batch_spec
        """
        if execution_engine:
            execution_engine = cast(SqlAlchemyExecutionEngine, execution_engine)

        super().__init__(
            name=name,
            id=id,
            datasource_name=datasource_name,
            execution_engine=execution_engine,
            batch_spec_passthrough=batch_spec_passthrough,
        )

        self._include_schema_name = include_schema_name
        self._splitter_method = splitter_method
        self._splitter_kwargs = splitter_kwargs
        self._sampling_method = sampling_method
        self._sampling_kwargs = sampling_kwargs

        self._assets = {}

        self._refresh_data_assets_cache(assets=assets)

        self._data_references_cache = {}

    @property
    def execution_engine(self) -> SqlAlchemyExecutionEngine:
        return cast(SqlAlchemyExecutionEngine, self._execution_engine)

    @property
    def include_schema_name(self) -> bool:
        return self._include_schema_name

    @property
    def splitter_method(self) -> Optional[str]:
        return self._splitter_method

    @property
    def splitter_kwargs(self) -> Optional[dict]:
        return self._splitter_kwargs

    @property
    def sampling_method(self) -> Optional[str]:
        return self._sampling_method

    @property
    def sampling_kwargs(self) -> Optional[dict]:
        return self._sampling_kwargs

    @property
    def assets(self) -> Optional[Dict[str, dict]]:
        return self._assets

    def add_data_asset(
        self,
        name: str,
        config: dict,
    ) -> None:
        """
        Add data_asset to DataConnector using data_asset name as key, and data_asset config as value.
        """
        name = self._update_data_asset_name_from_config(
            data_asset_name=name, data_asset_config=config
        )
        self._assets[name] = config

    def get_batch_definition_list_from_batch_request(self, batch_request: BatchRequest):
        """
        Retrieve batch_definitions that match batch_request

        First retrieves all batch_definitions that match batch_request
            - if batch_request also has a batch_filter, then select batch_definitions that match batch_filter.
            - NOTE : currently sql data connectors do not support sorters.

        Args:
            batch_request (BatchRequestBase): BatchRequestBase (BatchRequest without attribute validation) to process

        Returns:
            A list of BatchDefinition objects that match BatchRequest
        """
        self._validate_batch_request(batch_request=batch_request)

        if len(self._data_references_cache) == 0:
            self._refresh_data_references_cache()

        batch_definition_list: List[BatchDefinition] = []
        try:
            sub_cache = self._get_data_reference_list_from_cache_by_data_asset_name(
                data_asset_name=batch_request.data_asset_name
            )
        except KeyError:
            raise KeyError(
                f"data_asset_name {batch_request.data_asset_name} is not recognized."
            )

        for batch_identifiers in sub_cache:
            batch_definition = BatchDefinition(
                datasource_name=self.datasource_name,
                data_connector_name=self.name,
                data_asset_name=batch_request.data_asset_name,
                batch_identifiers=IDDict(batch_identifiers),
                batch_spec_passthrough=batch_request.batch_spec_passthrough,
            )
            if batch_definition_matches_batch_request(batch_definition, batch_request):
                batch_definition_list.append(batch_definition)

        # <WILL> 20220725 - In the case of file_data_connectors, this step is enabled, but sql_data_connectors
        # currently do not support sorters. This step can be enabled once sorting is implemented for sql_data_connectors
        # if len(self.sorters) > 0:
        #     batch_definition_list = self._sort_batch_definition_list(
        #         batch_definition_list=batch_definition_list
        #     )
        if batch_request.data_connector_query is not None:
            data_connector_query_dict = batch_request.data_connector_query.copy()
            if (
                batch_request.limit is not None
                and data_connector_query_dict.get("limit") is None
            ):
                data_connector_query_dict["limit"] = batch_request.limit

            batch_filter_obj: BatchFilter = build_batch_filter(
                data_connector_query_dict=data_connector_query_dict
            )
            batch_definition_list = batch_filter_obj.select_from_data_connector_query(
                batch_definition_list=batch_definition_list
            )

        return batch_definition_list

    def get_available_data_asset_names(self) -> List[str]:
        """
        Return the list of asset names known by this DataConnector.

        Returns:
            A list of available names
        """
        return list(self.assets.keys())

    def get_unmatched_data_references(self) -> List[str]:
        """
        Returns the list of data_references unmatched by configuration by looping through items in _data_references_cache
        and returning data_reference that do not have an associated data_asset.

        Returns:
            list of data_references that are not matched by configuration.
        """
        return []

    def get_available_data_asset_names_and_types(self) -> List[Tuple[str, str]]:
        """
        Return the list of asset names and types known by this DataConnector.

        Returns:
        A list of tuples consisting of available names and types
        """
        return [(asset["table_name"], asset["type"]) for asset in self.assets.values()]

    def build_batch_spec(
        self, batch_definition: BatchDefinition
    ) -> SqlAlchemyDatasourceBatchSpec:
        """
        Build BatchSpec from batch_definition by calling DataConnector's build_batch_spec function.

        Args:
            batch_definition (BatchDefinition): to be used to build batch_spec

        Returns:
            BatchSpec built from batch_definition
        """

        data_asset_name: str = batch_definition.data_asset_name
        if (
            data_asset_name in self.assets
            and self.assets[data_asset_name].get("batch_spec_passthrough")
            and isinstance(
                self.assets[data_asset_name].get("batch_spec_passthrough"), dict
            )
        ):
            # batch_spec_passthrough from data_asset
            batch_spec_passthrough = deepcopy(
                self.assets[data_asset_name]["batch_spec_passthrough"]
            )
            batch_definition_batch_spec_passthrough = (
                deepcopy(batch_definition.batch_spec_passthrough) or {}
            )
            # batch_spec_passthrough from Batch Definition supersedes batch_spec_passthrough from data_asset
            batch_spec_passthrough.update(batch_definition_batch_spec_passthrough)
            batch_definition.batch_spec_passthrough = batch_spec_passthrough

        batch_spec: BatchSpec = super().build_batch_spec(
            batch_definition=batch_definition
        )

        return SqlAlchemyDatasourceBatchSpec(batch_spec)

    def _refresh_data_assets_cache(
        self,
        assets: Optional[Dict[str, dict]] = None,
    ) -> None:
        self._assets = {}

        if assets:
            data_asset_name: str
            data_asset_config: dict
            for data_asset_name, data_asset_config in assets.items():
                aux_config: dict = {
                    "splitter_method": data_asset_config.get(
                        "splitter_method", self.splitter_method
                    ),
                    "splitter_kwargs": data_asset_config.get(
                        "splitter_kwargs", self.splitter_kwargs
                    ),
                    "sampling_method": data_asset_config.get(
                        "sampling_method", self.sampling_method
                    ),
                    "sampling_kwargs": data_asset_config.get(
                        "sampling_kwargs", self.sampling_kwargs
                    ),
                }

                deep_filter_properties_iterable(
                    properties=aux_config,
                    inplace=True,
                )
                data_asset_config.update(aux_config)
                data_asset_config.update(
                    {
                        "type": data_asset_config.get("type"),
                        "table_name": data_asset_config.get(
                            "table_name", data_asset_name
                        ),
                    }
                )

                self.add_data_asset(name=data_asset_name, config=data_asset_config)

    def _update_data_asset_name_from_config(
        self, data_asset_name: str, data_asset_config: dict
    ) -> str:
        schema_name: str = data_asset_config.get("schema_name")
        include_schema_name: bool = data_asset_config.get(
            "include_schema_name", self.include_schema_name
        )

        if schema_name is not None and include_schema_name:
            schema_name = f"{schema_name}."
        else:
            schema_name = ""

        data_asset_name: str = f"{schema_name}{data_asset_name}"

        """
        In order to support "SimpleSqlalchemyDatasource", which supports "data_asset_name_prefix" and
        "data_asset_name_suffix" as part of "tables" (reserved key for configuring "ConfiguredAssetSqlDataConnector" for
        a table), these configuration attributes can exist in "data_asset_config" and must be handled appropriately.
        """
        data_asset_name_prefix: str = data_asset_config.get(
            "data_asset_name_prefix", ""
        )
        data_asset_name_suffix: str = data_asset_config.get(
            "data_asset_name_suffix", ""
        )

        data_asset_name: str = (
            f"{data_asset_name_prefix}{data_asset_name}{data_asset_name_suffix}"
        )

        return data_asset_name

    def _refresh_data_references_cache(self) -> None:
        self._data_references_cache = {}

        for data_asset_name in self.assets:
            data_asset_config = self.assets[data_asset_name]
            batch_identifiers_list = (
                self._get_batch_identifiers_list_from_data_asset_config(
                    data_asset_name=data_asset_name,
                    data_asset_config=data_asset_config,
                )
            )

            # TODO Abe 20201029 : Apply sorters to batch_identifiers_list here
            # TODO Will 20201102 : add sorting code here
            self._data_references_cache[data_asset_name] = batch_identifiers_list

    def _get_batch_identifiers_list_from_data_asset_config(
        self,
        data_asset_name: str,
        data_asset_config: dict,
    ) -> List[dict]:
        table_name: str = data_asset_config.get("table_name", data_asset_name)

        schema_name: str = data_asset_config.get("schema_name")
        if schema_name is not None:
            table_name = f"{schema_name}.{table_name}"

        batch_identifiers_list: List[dict]
        splitter_method_name: Optional[str] = data_asset_config.get("splitter_method")
        if splitter_method_name is not None:
            splitter_kwargs: Optional[dict] = data_asset_config.get("splitter_kwargs")
            batch_identifiers_list = (
                self.execution_engine.get_data_for_batch_identifiers(
                    table_name=table_name,
                    splitter_method_name=splitter_method_name,
                    splitter_kwargs=splitter_kwargs,
                )
            )
        else:
            batch_identifiers_list = [{}]

        return batch_identifiers_list

    def _get_data_reference_list_from_cache_by_data_asset_name(
        self, data_asset_name: str
    ) -> List[dict]:
        return self._data_references_cache[data_asset_name]

    def _generate_batch_spec_parameters_from_batch_definition(
        self, batch_definition: BatchDefinition
    ) -> dict:
        """
        Build BatchSpec parameters from batch_definition with the following components:
            1. data_asset_name from batch_definition
            2. batch_identifiers from batch_definition
            3. data_asset from data_connector

        Args:
            batch_definition (BatchDefinition): to be used to build batch_spec

        Returns:
            dict built from batch_definition
        """
        data_asset_name: str = batch_definition.data_asset_name
        table_name: str = self._get_table_name_from_batch_definition(batch_definition)
        return {
            "data_asset_name": data_asset_name,
            "table_name": table_name,
            "batch_identifiers": batch_definition.batch_identifiers,
            **self.assets[data_asset_name],
        }

    def _get_table_name_from_batch_definition(
        self, batch_definition: BatchDefinition
    ) -> str:
        """
        Helper method called by _generate_batch_spec_parameters_from_batch_definition() to parse table_name from
        data_asset_name in cases where schema is included.

        data_asset_name in those cases are [schema].[table_name].

        function will split data_asset_name on [schema]. and return the resulting table_name.
        """
        data_asset_name: str = batch_definition.data_asset_name
        data_asset_dict: dict = self.assets[data_asset_name]
        table_name: str = data_asset_dict["table_name"]
        schema_name: Optional[str] = None
        if "schema_name" in data_asset_dict:
            schema_name = data_asset_dict["schema_name"]

        if schema_name is not None and schema_name not in table_name:
            table_name = f"{schema_name}.{table_name}"

        return table_name

    def _map_data_reference_to_batch_definition_list(
        self, data_reference, data_asset_name: Optional[str] = None  #: Any,
    ) -> Optional[List[BatchDefinition]]:
        # Note: This is a bit hacky, but it works. In sql_data_connectors, data references *are* dictionaries,
        # allowing us to invoke `IDDict(data_reference)`
        return [
            BatchDefinition(
                datasource_name=self.datasource_name,
                data_connector_name=self.name,
                data_asset_name=data_asset_name,
                batch_identifiers=IDDict(data_reference),
            )
        ]
