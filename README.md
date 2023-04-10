# OpenAI Python Cli Client
**Warning: The OpenAI Service is not available in China Mainland (include HongKong), if you are in these aeras, beware of being banned by OpenAI.**
## Azure OpenAI Service
### Required Config File
*The default config file is in $HOME/.config/chatgpt-py/config_azure.json, There is an example of config file.*
```json
{"api_type": "azure", "api_base": " https://example.com/", "api_version": "api_version", "api_key": "api_key", "engine": "your_model", "max_tokens": max_tokens, "temperature": temperature, "timeout": timeout}
```
## OpenAI Service
### Required Config File
*The default config file is in $HOME/.config/chatgpt-py/config_openai.json, There is an example of config file.*
```json
{"api_type": "openai", "api_key": "api_key", "engine": "model_name", "max_tokens": max_tokens, "temperature": temperature, "timeout": timeout}
```
## Referenced Docs
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-studio)  
- [Text Completion](https://platform.openai.com/docs/guides/completion)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions/create)
