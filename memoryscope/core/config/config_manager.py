import json
from dataclasses import fields
from pathlib import Path
from typing import Optional, Literal

import yaml

from memoryscope.constants.language_constants import DEFAULT_HUMAN_NAME
from memoryscope.core.config.arguments import Arguments
from memoryscope.enumeration.language_enum import LanguageEnum


class ConfigManager(object):

    def __init__(self,
                 config: dict = None,
                 config_path: Optional[str] = None,
                 arguments: Optional[Arguments] = None,
                 demo_config_name: str = "demo_config.yaml",
                 **kwargs):
        self.config: dict = {}
        self.kwargs = kwargs

        if config:
            self.config = config

        elif config_path:
            self.read_config(config_path)

        else:
            self.read_demo_config(demo_config_name)

        if arguments:
            self.update_config_by_arguments(arguments)

        elif kwargs:
            key_list = [x.name for x in fields(Arguments)]
            arguments = Arguments(**{k: v for k, v in kwargs.items() if k in key_list})
            self.update_config_by_arguments(arguments)

    def read_config(self, config_path: str):
        if config_path.endswith(".yaml"):
            with open(config_path) as f:
                self.config = yaml.load(f, yaml.FullLoader)

        elif config_path.endswith(".json"):
            with open(config_path) as f:
                self.config = json.load(f)

    def read_demo_config(self, demo_config_name: str):
        file_path = Path(__file__)
        demo_config_path = (file_path.parent / demo_config_name).__str__()
        with open(demo_config_path) as f:
            self.config = yaml.load(f, yaml.FullLoader)

    @staticmethod
    def update_global_by_arguments(config: dict, arguments: Arguments):
        config.update({
            "language": arguments.language,
            "thread_pool_max_workers": arguments.thread_pool_max_workers,
            "logger_name": arguments.logger_name,
            "logger_name_time_suffix": arguments.logger_name_time_suffix,
            "use_dummy_ranker": arguments.use_dummy_ranker,
        })

    @staticmethod
    def update_memory_chat_by_arguments(config: dict, arguments: Arguments):
        if arguments.memory_chat_type == "cli_chat":
            memory_chat_class = "chat.cli_memory_chat"
        elif arguments.memory_chat_type == "api_chat":
            memory_chat_class = "chat.api_memory_chat"
        else:
            raise NotImplementedError(f"known memory_chat_type={arguments.memory_chat_type}")
        config.update({
            "class": memory_chat_class,
            "human_name": DEFAULT_HUMAN_NAME[LanguageEnum(arguments.language)],
            "assistant_name": "AI",
        })

    @staticmethod
    def update_memory_service_by_arguments(config: dict, arguments: Arguments):
        config.update({
            "human_name": DEFAULT_HUMAN_NAME[LanguageEnum(arguments.language)],
            "assistant_name": "AI",
        })
        config["memory_operations"]["consolidate_memory"]["interval_time"] = \
            arguments.consolidate_memory_interval_time
        config["memory_operations"]["reflect_and_reconsolidate"]["interval_time"] = \
            arguments.reflect_and_reconsolidate_interval_time

    @staticmethod
    def update_worker_by_arguments(config: dict, arguments: Arguments):
        for worker_name, kv_dict in arguments.worker_params.items():
            if worker_name not in config:
                continue
            config[worker_name].update(kv_dict)

    @staticmethod
    def update_model_by_arguments(config: dict, arguments: Arguments):
        config["generation_model"].update({
            "module_name": arguments.generation_backend,
            "model_name": arguments.generation_model,
            **arguments.generation_params,
        })

        config["embedding_model"].update({
            "module_name": arguments.embedding_backend,
            "model_name": arguments.embedding_model,
            **arguments.embedding_params,
        })

        config["rank_model"].update({
            "module_name": arguments.rank_backend,
            "model_name": arguments.rank_model,
            **arguments.rank_params,
        })

    @staticmethod
    def update_memory_store_by_arguments(config: dict, arguments: Arguments):
        config.update({
            "index_name": arguments.es_index_name,
            "es_url": arguments.es_url,
            "retrieve_mode": arguments.retrieve_mode})

    def update_config_by_arguments(self, arguments: Arguments):
        # prepare global
        self.update_global_by_arguments(self.config["global"], arguments)

        # prepare memory chat
        memory_chat_conf_dict = self.config["memory_chat"]
        memory_chat_config = list(memory_chat_conf_dict.values())[0]
        self.update_memory_chat_by_arguments(memory_chat_config, arguments)

        # prepare memory service
        memory_service_conf_dict = self.config["memory_service"]
        memory_service_config = list(memory_service_conf_dict.values())[0]
        self.update_memory_service_by_arguments(memory_service_config, arguments)

        # prepare worker
        self.update_worker_by_arguments(self.config["worker"], arguments)

        # prepare model
        self.update_model_by_arguments(self.config["model"], arguments)

        # prepare memory store
        self.update_memory_store_by_arguments(self.config["memory_store"], arguments)

    def add_node_object(self, node: str, name: str, config: dict):
        self.config[node][name] = config

    def pop_node_object(self, node: str, name: str):
        return self.config[node].pop(name, None)

    def clear_node_all(self, node: str):
        self.config[node].clear()

    def dump_config(self, file_type: Literal["json", "yaml"], to_stream: bool = True, file_path: Optional[str] = None):
        if file_type == "json":
            content = json.dumps(self.config, indent=2, ensure_ascii=False)
        elif file_type == "yaml":
            content = yaml.dump(self.config, indent=2, allow_unicode=True)
        else:
            raise NotImplementedError

        if to_stream:
            print(content)

        if file_type:
            with open(file_path, "w") as f:
                f.write(content)
