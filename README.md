# genius-url
A URL builder for genius :D

## Usage
```
from gurl import genius_url

@genius_url
def any_function_you_want():
  url = create.your.cool.url/in.this/way.lol
  ...
```

## Example
```python
from gurl import genius_url

@genius_url
def do_request():
    # note that this is an expression, not a string!
    url = www.httpbin.org/anything/test/'[special-path]'/'!!'/index.html

    print("[+] request to", url)
    return url.request(method='GET')

print(do_request().json())
```
