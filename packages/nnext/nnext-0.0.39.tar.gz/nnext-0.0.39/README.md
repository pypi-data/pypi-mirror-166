
# <a href="https://nnext.ai/"><img src="https://d135j1zm1liera.cloudfront.net/nnext-logo-wide.png" height="100" alt="Apollo Client"></a>

## About

This repository houses the source code for the python client associated with NNext.

NNext is a
* ⚡ blazingly fast
* 🔍 nearest-neighbors vector search engine

<a href="https://tiny.one/nnext-slk-comm-gh"><img src="https://img.shields.io/badge/chat-slack-orange.svg?logo=slack&style=flat"></a>
<a href="https://twitter.com/intent/follow?screen_name=nnextai"><img src="https://img.shields.io/badge/Follow-nnextai-blue.svg?style=flat&logo=twitter"></a>

[Installation](#installation) |  [Quick Start](#quick-start) | [Documentation](#documentation)

## Installation
To install the pynnext client, activate a virtual environment, and install via pip:

```zsh
pip install nnext
```

## Quick Start

Here's a quick example showcasing how you can create an index, insert vectors/documents and search among them via NNext.

Let's begin by installing the NNext server.

```zsh
docker run -p 6040:6040 -p 6041:6041 \
	-v ~/.nnext/data:/.nnext/data \
	nnext/nnext
```

## Documentation
More documentation is available here:

https://nnext.ai/docs