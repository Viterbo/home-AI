estoy intentando hacer:
```bash
npm run stop
npm run start
```

Eso levanta todo regenerando únicamente el homeai_agents el cual actualmente falla su compilación. Puedes verlo al ejecutar:
```bash
$ docker logs homeai_agents
[INIT] Initializing CrewAI Ollama LLM
Unable to initialize LLM with model 'llama3.1:8b'. The model did not match any supported native provider (openai, anthropic, claude, azure, azure_openai, google, gemini, bedrock, aws), and the LiteLLM fallback package is not installed.

To fix this, either:
  1. Install LiteLLM for broad model support: uv add 'crewai[litellm]'
or
pip install litellm

For more details, see: https://docs.crewai.com/en/learn/llm-connections
Traceback (most recent call last):
  File "/usr/local/bin/uvicorn", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1161, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1082, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1443, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 788, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 433, in main
    run(
  File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 606, in run
    server.run()
  File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 75, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/uvicorn/_compat.py", line 30, in asyncio_run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 79, in serve
    await self._serve(sockets)
  File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 86, in _serve
    config.load()
  File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 441, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/app/app/main.py", line 29, in <module>
    llm = LLM(
          ^^^^
  File "/usr/local/lib/python3.11/site-packages/crewai/llm.py", line 437, in __new__
    raise ImportError(error_msg) from None
ImportError: Unable to initialize LLM with model 'llama3.1:8b'. The model did not match any supported native provider (openai, anthropic, claude, azure, azure_openai, google, gemini, bedrock, aws), and the LiteLLM fallback package is not installed.

To fix this, either:
  1. Install LiteLLM for broad model support: uv add 'crewai[litellm]'
or
pip install litellm

For more details, see: https://docs.crewai.com/en/learn/llm-connections

```
