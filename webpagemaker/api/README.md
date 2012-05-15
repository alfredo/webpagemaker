The WPM API supports the following endpoints. Unless specified otherwise, all
`POST` requests accept content type `application/x-www-form-urlencoded`
for their parameters.

All API calls are currently anonymous--no auth is needed.

## Create Page

Publishes an HTML page to the server.

**Endpoint:** `/api/page`

**HTTP Method:** `POST`

### Parameters

* `html` is the HTML content of the page to publish.
* `original-url` (optional) specifies the absolute URL which the HTML is
a remix of. The protocol of the URL must be http or https.

### Return Value

**Content Type:** `text/plain`

An absolute path to read the published page, e.g. `/p/1`.

## Read Page

Returns the sanitized HTML of a previously published page, including nofollow on links.

**Endpoint:** `/p/{id}`

**HTTP Method:** `GET`

### Return Value

**Content Type:** `text/html`

The [bleach][]-sanitized HTML for the page corresponding to `{id}`.

  [bleach]: http://pypi.python.org/pypi/bleach


## Remix Page

Similar to above, returns the sanitized HTML of a previously published page, but without nofollow.

**Endpoint:** `/p/{id}?code=1`

**HTTP Method:** `GET`

### Return Value

**Content Type:** `text/plain`

Sanitized version of a page, but without nofollow.

## Read Configuration

Returns the sanitization configuration of the server, including what tags and 
attributes the sanitizer allows. Can be used by the front-end to provide fast 
feedback to the end-user regarding whether some of their HTML will be 
stripped.

**Endpoint:** `/api/config`

**HTTP Method:** `GET`

### Return Value

**Content-Type:** `application/json`

* `allowed_tags` is a list of lowercase tags that the sanitizer allows. Example: `['a', 'img']`.

* `allowed_attributes` is an object with tag names as keys and lists of
allowed attributes as values. `*` is a wildcard key to allow an attribute on
any tag. Example: `{'*': ['class'], 'img': ['src', 'alt']}`.
