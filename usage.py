import deepl
import os

# Replace with your key
auth_key = os.environ["deepl_key"]
translator = deepl.Translator(auth_key)

usage = translator.get_usage()
if usage.any_limit_reached:
    print('Translation limit reached.')
if usage.character.valid:
    print(
        f"Character usage: {usage.character.count} of {usage.character.limit}")
if usage.document.valid:
    print(f"Document usage: {usage.document.count} of {usage.document.limit}")

