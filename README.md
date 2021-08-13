# genius-url
A URL builder for genius :D

## Usage

### Step 0x01
Just import it.
```python
from gurl import genius_url
```

### Step 0x02
Using `@genius_url` as a function decorator, then you are able to build any url in this way!
```python
@genius_url
def any_function_you_want():
  url = create.your.cool.url/in_this/way.lol
  ...
```

## Example
```python
from gurl import genius_url

@genius_url
def do_request():
    # note that this is an expression, not a string!
    url = www.httpbin.org/anything/test/'[special-path]'/index.html

    print("[+] request to", url)
    return url (method='POST')

print(do_request().json())
```
