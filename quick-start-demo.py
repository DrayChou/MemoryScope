import os
from memoryscope import cli
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('DASHSCOPE_API_KEY', None) is None \
        and os.environ.get('OPENAI_API_KEY', None) is None:
    raise RuntimeError(f"""
Missing api key(dashscope api key or openai api key.
`https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key` or
`https://openai.com/`""")

cli()
