# Exfer - External Inference

> [!WARNING]
> Extreme Work-In-Progress. Do not use yet. Feel free to follow/watch to be alerted
> to when it is available.
>
> Also, open to contributors if you want to help work on this.

Python library providing clients for external inference providers such as OpenAI, OpenRouter, Anthropic, Google, etc.

## Usage

Using Exfer can be dead-simple using the main class `Exfer`. Creating your own global singleton is recommended as Exfer doesn't
provide a pre-instantiated one. But making them is easy enough.

There are two options. Construct the Exfer yourself by adding `Provider` instances that you have customized, or let Exfer build them
out by checking the system environment for possible API keys and open ports (for local providers).

The simplest way is just:
```python
from exfer import Exfer

exference = Exfer.from_env()
```

Otherwise you can customize it yourself:
```python
from exfer import Exfer, Ollama, OpenAI

exference = Exfer(providers=[
	Ollama(url_override="http://localhost:9876"),
	OpenAI(api_key="ABCDEF123456789"),
])
```

Once you have your `Exfer` instance ready, you can start making calls. Either
synchronously, or asynchronously (given the model capabilities allow for it).

```python
from .common import exference # Just an example of a globally provided instance.

# Synchronous response, returns as a string the entire response body.
response = exference.generate('llama3.2')

# Asynchronous fragment generator gives parts of the response text as they become available.
for fragment in exference.generate('llama3.2', stream=True):
	print(fragment)

```

The `Exfer` class will attempt to find the first available provider that has the
given model available. Both models and providers use unique "keys" to make usage
easier.

If you don't want to have automatic provider selection, and instead want to specify
it yourself you can:

```python
response = exference.generate(model='llama3.2', provider='lmstudio')
```

# License

Copyright © 2025 Chris Pikul. Under MIT license. See [`LICENSE`](./LICENSE) for more details.