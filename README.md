# Code Block Capture Iterator

`CodeBlockCaptureIter` is a Python iterator that processes a stream of text chunks and **extracts JSON code blocks** while yielding the rest of the text normally.

It is designed to handle **chunked input** (e.g., from streaming APIs) where Markdown code fences (```json ... ```) may be split across boundaries.

## Features

- Detects and captures the first ` ```json ... ``` ` block.
- Stores the extracted code (without newlines) in `.code_block`.
- Yields the input text with code blocks removed.
- Handles arbitrarily split input chunks.

## Example

```python
from code_block_capture_iter import CodeBlockCaptureIter

chunks = [
    "Hell","o Wo","rld!","\n``","`jso","n\n{","\"fo","o\":"," \"b","ar\"","}\n`","``\nblub"
]

it = CodeBlockCaptureIter(iter(chunks))

result = "".join([chunk for chunk in it]).replace("\n", "")
print("Result text:", result)            # "Hello World!blub"
print("Captured code:", it.code_block)   # {"foo": "bar"}
```
