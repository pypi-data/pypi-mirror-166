# -*- coding: utf-8 -*-
from getpass import getpass
import logging

import requests

__all__ = ("InUse",)

logger = logging.getLogger("inuse")


class BaseEndpoint:
    def __init__(self, name, request):
        self.name = name
        self.request = request

    def __repr__(self):
        return f"<{self.name.title()} Endpoint>"

    def _list_url(self):
        return self.name

    def _detail_url(self, pk, route=""):
        return f"{self.name}/{pk}/{route}" if route else f"{self.name}/{pk}"

    def list(self, **kwargs):
        return self.request(method="GET", url=self._list_url(), **kwargs).json()

    def create(self, **kwargs):
        return self.request(method="POST", url=self._list_url(), **kwargs).json()

    def update(self, pk, **kwargs):
        return self.request(method="PUT", url=self._detail_url(pk), **kwargs).json()

    def partial_update(self, pk, **kwargs):
        return self.request(method="PATCH", url=self._detail_url(pk), **kwargs).json()

    def retrieve(self, pk, **kwargs):
        return self.request(method="GET", url=self._detail_url(pk), **kwargs).json()

    def destroy(self, pk, **kwargs):
        return self.request(method="DELETE", url=self._detail_url(pk), **kwargs)

    def get_or_none(self, params, **kwargs):
        ret = self.list(params=params, **kwargs)
        assert len(ret) <= 1
        if ret:
            return ret[0]

    def get_or_create(self, params, data, **kwargs):
        ret = self.list(params=params, **kwargs)
        assert len(ret) <= 1
        if ret:
            return ret[0]
        else:
            return self.create(data=data, **kwargs)

    def update_or_create(self, params, data, **kwargs):
        ret = self.list(params=params, **kwargs)
        assert len(ret) <= 1
        if ret:
            return self.update(ret[0]["pk"], data=data, **kwargs)
        else:
            return self.create(data=data, **kwargs)


class InUse:
    def __init__(self, base_url, version="internal"):
        self.version = version
        self.base_url = base_url
        self.session = None

        self.indices = BaseEndpoint("indices", self.request)
        self.manufacturers = BaseEndpoint("manufacturers", self.request)
        self.machine_models = BaseEndpoint("machine-models", self.request)
        self.producers = BaseEndpoint("producers", self.request)
        self.sites = BaseEndpoint("sites", self.request)
        self.lines = BaseEndpoint("lines", self.request)
        self.machines = BaseEndpoint("machines", self.request)
        self.properties = BaseEndpoint("properties", self.request)
        self.multispans = BaseEndpoint("multispans", self.request)
        self.csvs = BaseEndpoint("csvs", self.request)
        self.posts = BaseEndpoint("records", self.request)
        self.triggers = BaseEndpoint("tasks", self.request)
        self.synoptics = BaseEndpoint("synoptics", self.request)
        self.files = BaseEndpoint("files", self.request)
        self.agents = BaseEndpoint("agents", self.request)
        self.groups = BaseEndpoint("groups", self.request)
        self.favorites = BaseEndpoint("favorites", self.request)
        self.notifications = BaseEndpoint("notifications", self.request)
        self.alerts = BaseEndpoint("alerts", self.request)
        self.sandboxes = BaseEndpoint("sandboxes", self.request)
        self.property_drafts = BaseEndpoint("property-drafts", self.request)

    def __repr__(self):
        return f"<InUse ({self.base_url})>"

    def login(self, username, password=None):
        if password is None:
            password = getpass("Enter password:")
        self.session = requests.Session()
        ret = self.session.post(
            f"{self.base_url}/api-token-auth/",
            {"email": username, "password": password},
        )
        token = ret.json()["token"]
        logger.info("successfully authenticated")
        self.session.headers.update({"Authorization": f"JWT {token}"})

    def logout(self):
        del self.session
        logger.info("successfully logged out")

    def request(self, method, url, *args, **kwargs):
        if not self.session:
            raise ValueError(
                "Client is not authenticated yet. Please call `login(username, password)` first."
            )
        prefix = {"internal": "/api"}[self.version]
        response = self.session.request(
            method, f"{self.base_url}{prefix}/{url}", *args, **kwargs
        )
        response.raise_for_status()
        return response
