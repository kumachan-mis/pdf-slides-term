import os
import json
from typing import List, Dict, Any, Union, Callable, Generic

from .util import create_dir_name_from_config, create_file_name_from_paths
from ..configs import RankingMethodLayerConfig
from py_slides_term.methods.rankingdata.base import RankingData


class RankingMethodLayerCache(Generic[RankingData]):
    def __init__(self, cache_dir: str):
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: List[str],
        config: RankingMethodLayerConfig,
        from_json: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            obj = json.load(json_file)

        return from_json(obj)

    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: RankingMethodLayerConfig,
    ):
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(ranking_data.to_json(), json_file, ensure_ascii=False, indent=2)
