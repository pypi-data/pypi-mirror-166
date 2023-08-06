from dataclasses import dataclass
from requests import Session, Request
import json

"""
A simple api client for managing types and objects in Datagerry
"""

@dataclass
class Datagerry:
    """ base class for the api """

    def __init__(self, url, auth, verify, author_id: int):
        self.url = url
        """ ex: datagerry.domain.com """
        self.auth = auth
        """ base64 encoded *username:password* string """
        self.verify = verify
        """ path to self issued certificate or True/False value """
        self.session = Session()
        self.request = Request()
        self.author_id = author_id
        """ author id of the user authenticating, generally a user dedicated for automations. """

    def make_request(self):
        """ function called to send/recieve every requests """
        
        self.session.verify = self.verify
        self.request.headers = {
            "Content-type": "application/json",
            "Authorization": f"Basic {self.auth}",
        }
        self.request = self.request.prepare()

        response = self.session.send(self.request)
        self.request = Request()

        return response.json()

    def get_type_id(self, type_label):
        """ get the type id from a type label """

        query = [{"$match": {"label": type_label}}]

        self.request.method = "GET"
        self.request.url = self.url + f"/rest/types/"
        self.request.params = {
            "filter": json.dumps(query),
        }

        response = self.make_request()
        try:
            type_id = response["results"][0]["public_id"]
        except IndexError:
            type_id = []
        except Exception as e:
            type_id = repr(e)

        return type_id

    def get_object_id(self, type_label, object_label):
        """ get the object id from a *unique* object value """
        type_id = self.get_type_id(type_label)
        query = [
            {
                "$match": {
                    "$and": [
                        {"type_id": type_id},
                        {"fields": {"$elemMatch": {"value": object_label}}},
                    ]
                }
            }
        ]
        self.request.method = "GET"
        self.request.url = self.url + f"/rest/objects/"
        self.request.params = {
            "sort": "name",
            "limit": 100,
            "filter": json.dumps(query),
        }

        response = self.make_request()
        try:
            object_id = response["results"][0]["public_id"]
        except IndexError:
            object_id = response["results"]
        except Exception as e:
            object_id = repr(e)

        return object_id

    def get_types(self):
        """ returns all types """
        self.request.method = "GET"
        self.request.url = self.url + f"/rest/types/"
        self.request.params = {
            "limit": 100,
        }

        response = self.make_request()
        try:
            types = [result["label"] for result in response["results"]]
        except Exception as e:
            types = repr(e)

        return types

    def get_type_fields(self, type_label):
        """ returns fields for a given type label """

        type_id = self.get_type_id(type_label)

        # query = [{"$match": {"label": type_label}}]

        self.request.method = "GET"
        self.request.url = self.url + f"/rest/types/{type_id}"
        # self.request.params = {
        #     "filter": json.dumps(query),
        # }

        response = self.make_request()
        try:
            type_fields = response["result"]["fields"]
        except Exception as e:
            type_fields = repr(e)

        return type_fields

    def create_type(self, data):
        """ creates a new type, see the blueprints for more info on the data format """
        summary_fields = [ field["name"] for field in data["fields"]]
        data = {
            "name" : data["name"],
            "label" : data["label"],
            "description" : data["description"],
            "version" : "1.0.0",
            "status" : None,
            "active" : True,
            "clean_db" : True,
            "access" : {
                "groups" : "",
                "users" : ""
            },
            "author_id" : self.author_id,
            "render_meta" : {
                "icon" : data["icon"],
                "sections" : data["sections"],
                "externals" : [],
                "summary" : {
                    "fields" : summary_fields
                }
            },
            "fields" : data["fields"],
            "category_id" : None,
            "acl" : {
                "activated" : False,
                "groups" : {
                    "includes" : {}
                }
            }
        }

        self.request.method = "POST"
        self.request.url = self.url + f"/rest/types/"
        self.request.data = json.dumps(data)

        response = self.make_request()

        return response

    # def update_type(self, type_label, data):
    #     """ """

    #     type_id = self.get_type_id(type_label)

    #     summary_fields = [ field["name"] for field in data["fields"]]
    #     data = {
    #         "author_id" : self.author_id,
    #         "render_meta" : {
    #             "sections" : data["sections"],
    #             "summary" : {
    #                 "fields" : summary_fields
    #             }
    #         },
    #         "fields" : data["fields"],
    #     }

    #     self.request.method = "PUT"
    #     self.request.url = self.url + f"/rest/types/{type_id}"
    #     self.request.data = json.dumps(data)

    #     response = self.make_request()

    #     return response

    def delete_type(self, type_label):
        """ delete a type """

        type_id = self.get_type_id(type_label)

        self.request.method = "DELETE"
        self.request.url = self.url + f"/rest/types/{type_id}"

        response = self.make_request()

        return response

    def get_objects(self, type_label):
        """ lists all field values for all objects belonging to a type """

        type_id = self.get_type_id(type_label)
        query = [
            {
                "$match": {
                    "$and": [
                        {"type_id": type_id}
                    ]
                }
            }
        ]

        self.request.method = "GET"
        self.request.url = self.url + f"/rest/objects/"
        self.request.params = {
            "sort": "name",
            "limit": 100,
            "filter": json.dumps(query),
        }

        response = self.make_request()
        try:
            objects = [object_details["fields"] for object_details in response["results"]]
        except IndexError:
            objects = []
        except Exception as e:
            objects = repr(e)

        return objects

    def get_object_fields(self, type_label, object_label):
        """ returns the field values of a specific object """
        print("Get Object")
        object_id = self.get_object_id(type_label, object_label)

        self.request.method = "GET"
        self.request.url = self.url + f"/rest/objects/{object_id}"

        response = self.make_request()
        object_fields = response
        try:
            object_fields = response["fields"]
        except Exception as e:
            object_fields = repr(e)

        return object_fields

    def create_object(self, type_label: str, fields: list):
        """ creates a new object of a specified type. fields must match the type and is a dict of attribue:value """

        type_id = self.get_type_id(type_label)
        fields = [{"name": field, "value": fields[field]} for field in fields]
        data = {
            "author_id": self.author_id,
            "version": "0.0.1",
            "type_id": type_id,
            "active": True,
            "fields": fields,
            "views": 0,
        }

        self.request.method = "POST"
        self.request.url = self.url + f"/rest/objects/"
        self.request.data = json.dumps(data)

        response = self.make_request()

        return response

    def update_object(self, type_label, object_label, fields):
        """ updates an existing object of a specific type. simply provide a dict with attribute:values for the fields you wish to modify """
        
        type_id = self.get_type_id(type_label)
        object_id = self.get_object_id(type_label, object_label)
        fields = [{"name": field, "value": fields[field]} for field in fields]
        data = {
            "author_id": self.author_id,
            "version": "0.0.1",
            "type_id": type_id,
            "public_id": object_id,
            "fields": fields,
            "views": 0,
        }

        self.request.method = "PUT"
        self.request.url = self.url + f"/rest/objects/{object_id}"
        self.request.data = json.dumps(data)

        response = self.make_request()

        return response

    def delete_object(self, type_label, object_label):
        """ delete an existing object of a specific type """

        type_id = self.get_type_id(type_label)
        object_id = self.get_object_id(type_id, object_label)

        self.request.method = "DELETE"
        self.request.url = self.url + f"/rest/objects/{object_id}"

        response = self.make_request()

        return response
