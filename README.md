English | [**中文**](./README_ZH.md)

# MemoryScope

<p align="left">
  <img src="docs/images/logo_1.png" width="700px" alt="MemoryScope Logo">
</p>

Equip your LLM chatbot with a powerful and flexible long term memory system.

----
## News

- **[2024-07-29]** We release MemoryScope v0.1.0.2 now, which is also available in [PyPI](https://pypi.org/simple)!
----
## What is MemoryScope？

MemoryScope is a powerful and flexible long term memory system for LLM chatbots. It consists 
of a memory database and three customizable system operations, which can be flexibly combined to provide 
robust long term memory services for your LLM chatbot.

💾 Memory Database:
- MemoryScope comes with an *ElasticSearch (ES)* vector database to store all the 
memory pieces recorded in the system.

🛠️ System operations:
- Memory Retrieval: Upon arrival of a user query, this operation returns the semantically related memory pieces 
and/or those from the corresponding time if the query involves reference to time.
- Memory Consolidation: This operation takes in a batch of user queries and returns important user information
extracted from the queries as consolidated *observations* to be stored in the memory database.
- Reflection and Re-consolidation: At regular intervals, this operation performs reflection upon newly recorded *observations*
to form and update *insights*. Then, memory re-consolidation is performed to ensure contradictions and repetitions
among memory pieces are properly handled.

### Main Features

⚡ Low response-time (RT) for the user:
- Backend operations (Memory Consolidation, Reflection and Re-consolidation) are decoupled from the frontend operation
 (Memory Retrieval) in the system.
- While backend operations are usually (and are recommended to be) queued or executed at regular intervals, the 
system's response time (RT) for the user depends solely on the frontend operation, which is only ~500ms.

🌲 Hierarchical and coherent memory:
- The memory pieces stored in the system are in a hierarchical structure, with *insights* being the high level information
from the aggregation of similarly-themed *observations*.
- Contradictions and repetitions among memory pieces are handled periodically to ensure coherence of memory.
- Fictitious contents from the user are filtered out to avoid hallucinations by the LLM.

⏰ Time awareness:
- The system is time sensitive when performing both Memory Retrieval and Memory Consolidation. Therefore, it can retrieve
accurate relevant information when the query involves reference to time.


### Example Usages
- [Simple Usages](./examples/api/simple_usages_en.ipynb)
- [Advanced Customization](./examples/api/advanced_customization_en.ipynb)



## 🚀 Installation

### Quick Start (CLI)
Todo: Jingli add CLI here

### (1) Docker-Compose (Recommended)
1. Clone the project and edit the config.

    ```
    git clone https://...
    nano config/demo_config_cn.yaml
    ```

2. Edit `docker-compose.yml` to change environment variable.

    ```
    DASHSCOPE_API_KEY: "sk-0000000000"
    ```

3. Run `docker-compose up` to build and launch the memory-scope cli interface.


### (2) Docker

1. Clone the project and edit the config.

    ```
    git clone https://...
    nano config/demo_config_cn.yaml
    ```

2. Build the `Dockerfile` with command:
    ```
    sudo docker build --network=host -t memoryscope .
    ```

3. Run `ElasticSearch` Container with command:
    ```
    docker run -p 9200:9200 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        -e "xpack.license.self_generated.type=trial" \
        docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

4. Launch the built image with command:
    ```
    sudo docker run -it --rm --net=host memoryscope
    ```

## 💡 Contribute

Contributions are always encouraged!

We highly recommend install pre-commit hooks in this repo before committing pull requests.
These hooks are small house-keeping scripts executed every time you make a git commit,
which will take care of the formatting and linting automatically.
```shell
poetry install --with dev
pre-commit install
```



## 📖 Citation

Reference to cite if you use MemoryScope in a paper:

```
@software{MemoryScope,
author = {},
month = {08},
title = {{MemoryScope}},
url = {https://github.com/modelscope/MemoryScope},
year = {2024}
}
```