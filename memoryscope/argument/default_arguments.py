DEFAULT_GLOBAL_ARGUMENTS = {
    "language": "en",
    "thread_pool_max_workers": 5,
    "logger_name": "memoryscope",
    "logger_name_time_suffix": "%Y%m%d_%H%M%S"
}

DEFAULT_MEMORY_CHAT_ARGUMENTS = {
    "cli_memory_chat": {
        "class": "chat.cli_memory_chat",
        "memory_service": "memoryscope_service",
        "generation_model": "generation_model"
    }
}

DEFAULT_MEMORY_SERVICE_ARGUMENTS = {
    "memoryscope_service": {
        "class": "memory.service.memory_scope_service",
        "memory_operations": {
            "read_message": {
                "class": "memory.operation.frontend_operation",
                "workflow": "read_message",
                "description": "read short memory"
            },
            "retrieve_memory": {
                "class": "memory.operation.frontend_operation",
                "workflow": "set_query,[extract_time|retrieve_obs_ins,semantic_rank],fuse_rerank",
                "description": "retrieve long-term memory"
            },
            "list_memory": {
                "class": "memory.operation.frontend_operation",
                "workflow": "set_query,retrieve_top_memory,print_memory",
                "description": "read all long-term memory of the user"
            },
            "delete_memory": {
                "class": "memory.operation.frontend_operation",
                "workflow": "set_query,retrieve_all_memory,delete_memory",
                "description": "delete a single long-term memory"
            },
            "delete_all": {
                "class": "memory.operation.frontend_operation",
                "workflow": "set_query,retrieve_all_memory,delete_all",
                "description": "delete all long-term memory"
            },
            "add_memory": {
                "class": "memory.operation.frontend_operation",
                "workflow": "add_memory",
                "description": "add a single observation"
            },
            "consolidate_memory": {
                "class": "memory.operation.consolidate_memory_op",
                "workflow": "info_filter,[get_observation|get_observation_with_time|load_today_memory],contra_repeat,"
                            "store_memory",
                "description": "summary user's observation memory",
                "interval_time": 1
            },
            "reflect_and_reconsolidate": {
                "class": "memory.operation.backend_operation",
                "workflow": "load_obs_and_insight,get_reflection_subject,update_insight,long_contra_repeat,"
                            "store_memory",
                "description": "summary user's insight memory",
                "interval_time": 15
            }
        }
    }
}

DEFAULT_WORKER_ARGUMENTS = {
    "dummy": {
        "class": "memory.worker.dummy_worker",
        "generation_model": "generation_model",
        "embedding_model": "embedding_model",
        "rank_model": "rank_model"
    },
    "read_message": {
        "class": "memory.worker.frontend.read_message_worker"
    },
    "set_query": {
        "class": "memory.worker.frontend.set_query_worker"
    },
    "retrieve_obs_ins": {
        "class": "memory.worker.frontend.retrieve_memory_worker",
        "retrieve_obs_top_k": 100,
        "retrieve_ins_top_k": 100
    },
    "extract_time": {
        "class": "memory.worker.frontend.extract_time_worker",
        "generation_model": "generation_model"
    },
    "semantic_rank": {
        "class": "memory.worker.frontend.semantic_rank_worker",
        "rank_model": "rank_model"
    },
    "fuse_rerank": {
        "class": "memory.worker.frontend.fuse_rerank_worker",
        "fuse_score_threshold": 0.01,
        "fuse_ratio_dict": {
            "conversation": 0.5,
            "observation": 1,
            "obs_customized": 1.2,
            "insight": 2
        },
        "fuse_time_ratio": 2,
        "fuse_rerank_top_k": 10
    },
    "retrieve_top_memory": {
        "class": "memory.worker.frontend.retrieve_memory_worker",
        "retrieve_obs_top_k": 100,
        "retrieve_ins_top_k": 100,
        "retrieve_expired_top_k": 100
    },
    "print_memory": {
        "class": "memory.worker.frontend.print_memory_worker"
    },
    "retrieve_all_memory": {
        "class": "memory.worker.frontend.retrieve_memory_worker",
        "retrieve_obs_top_k": 1000,
        "retrieve_ins_top_k": 1000,
        "retrieve_expired_top_k": 1000
    },
    "delete_memory": {
        "class": "memory.worker.backend.update_memory_worker",
        "method": "delete_memory"
    },
    "delete_all": {
        "class": "memory.worker.backend.update_memory_worker",
        "method": "delete_all"
    },
    "add_memory": {
        "class": "memory.worker.backend.update_memory_worker",
        "method": "from_query"
    },
    "info_filter": {
        "class": "memory.worker.backend.info_filter_worker",
        "generation_model": "generation_model"
    },
    "load_today_memory": {
        "class": "memory.worker.backend.load_memory_worker",
        "retrieve_today_top_k": 100
    },
    "get_observation": {
        "class": "memory.worker.backend.get_observation_worker",
        "generation_model": "generation_model"
    },
    "get_observation_with_time": {
        "class": "memory.worker.backend.get_observation_with_time_worker",
        "generation_model": "generation_model"
    },
    "contra_repeat": {
        "class": "memory.worker.backend.contra_repeat_worker",
        "generation_model": "generation_model"
    },
    "store_memory": {
        "class": "memory.worker.backend.update_memory_worker",
        "method": "from_memory_key",
        "memory_key": "all"
    },
    "load_obs_and_insight": {
        "class": "memory.worker.backend.load_memory_worker",
        "retrieve_not_reflected_top_k": 100,
        "retrieve_not_updated_top_k": 100,
        "retrieve_insight_top_k": 100
    },
    "get_reflection_subject": {
        "class": "memory.worker.backend.get_reflection_subject_worker",
        "generation_model": "generation_model",
        "reflect_obs_cnt_threshold": 10
    },
    "update_insight": {
        "class": "memory.worker.backend.update_insight_worker",
        "generation_model": "generation_model",
        "rank_model": "rank_model"
    },
    "long_contra_repeat": {
        "class": "memory.worker.backend.long_contra_repeat_worker",
        "generation_model": "generation_model"
    }
}

DEFAULT_MONITOR_ARGUMENTS = {
    "class": "storage.dummy_monitor"
}
