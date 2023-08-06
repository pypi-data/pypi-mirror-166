# pyinuse

`pyinuse` is the official Python client for [InUse](https://inuse.eu/) API.

It provides the following main API methods:

- list
- create
- update
- partial_update
- retrieve
- destroy

For main end points such as:

- manufacturers
- machine_models
- machines
- producers
- sites
- lines
- machines
- properties
- multispans
- csvs
- posts
- triggers
- synoptics
- files
- agents
- groups
- favorites
- notifications
- alerts
- sandboxes

Please refer to InUse API documentation (Accessible from the Studio) for more details.

## API versioning

The actual API version is the **internal** API (not versioned) and is subject to changes. A versioned public API will be created in a later stage and used in this python client.

## Example of usage

```python
# Library used to type a password in a secured way.
import getpass
# Client library for the InUse API.
from pyinuse import InUse
# Library for logging
import logging
logging.basicConfig(format="%(asctime)s, %(name)s, %(levelname)s, %(message)s", level=logging.INFO)

manufacturer_code="mycompany" # replace with your manufacturer code

# login
inuse = InUse(base_url=f"https://studio.{manufacturer_code}.productinuse.com")
inuse.login(input("Username? "), getpass.getpass("Password? "))

# get my manufacturer
# each endpoint is accessible by its name as an attribute of InUse instance
manufacturer = inuse.manufacturers.list()[0]

# create a new machine_model
machine_model = inuse.machine_models.update_or_create(
    params={"manufacturer": manufacturer["pk"], "code": "my-machine-model"},
    data={
        "manufacturer": manufacturer["pk"],
        "code": "my-machine-model",
        "name": "my machine model",
    },
)

# logout once you're done
inuse.logout()
```
