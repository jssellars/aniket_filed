import json
import uuid

from django.core import serializers
from interest.models import *


class Node(dict):
    def __init__(self, name, children=None):
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.id = str(uuid.uuid4())
        self.children = [] if not children else children

    def _searchNode(self, name):
        if (self.name == name):
            return self

        if not hasattr(self, 'children'):
            return "Not found"

        for child in self.children:
            found = child._searchNode(name)
            if found != "Not found":
                return found

        return "Not found"

    def addChild(self, parentName, child):
        # 'Name acts as soft id: A parent can not have two children with the same name'
        parent = self._searchNode(parentName)
        if parent == "Not found":
            raise Exception("Parent not found! Name: " + parentName)
        if not parent._hasChild(child.name):
            parent.children.append(child)

    def _hasChild(self, childName):
        if not hasattr(self, 'children'):
            return False
        for child in self.children:
            if child.name == childName:
                return True
        return False


class Leaf(Node):
    def __init__(self, name, properties):
        Node.__init__(self, name)
        for k, v in properties.items():
            self[k] = v
        del self.children


def flattenData(data):
    # 'Adds type to path and adds the leaf as an external property for simplified processing'
    extraNodes = {
        "Family Statuses": "Demographics",
        "Life Events": "Demographics",
        "Industries": "Demographics",
        "User Device": "Interests",
        "User Os": "Interests"
    }
    for nodeData in data:
        if 'type' in nodeData.keys():
            if nodeData['type'] and isinstance(nodeData['type'], str):
                node_type = " ".join(nodeData['type'].title().split("_"))
            else:
                node_type = ""
            if isinstance(nodeData['path'], list):
                if node_type not in nodeData['path']:
                    nodeData['path'].insert(0, node_type)
            else:
                nodeData['path'] = [node_type]
            # del nodeData['type']

        if node_type in extraNodes.keys():
            node_type = extraNodes[node_type]
            nodeData['path'].insert(0, node_type)

        if nodeData['name'] not in nodeData['path']:
            nodeData['path'].append(nodeData['name'])
        leafNode = nodeData['path'].pop()
        nodeData['leaf'] = leafNode
        del nodeData['name']

    return data


def get_interests_tree_handler(raw_interests=None):
    if not raw_interests:
        raw_results = json.loads(serializers.serialize('json', RawInterest.objects.all()))
    else:
        raw_results = raw_interests
    results = []
    for result in raw_results:
        if 'fields' in result.keys():
            result = result['fields']
        try:
            if isinstance(result['path'], str):
                result['path'] = json.loads(result['path'])
        except KeyError:
            pass
        except TypeError:
            pass
        results.append(result)

    results = flattenData(results)
    root = Node("Root")
    ignoredKeys = ["leaf", "name"]

    for nodeData in results:
        parentNode = "Root"
        properties = {}

        for k, v in nodeData.items():
            if k not in ignoredKeys:
                properties[k] = v

        for pathNode in nodeData['path']:
            root.addChild(parentNode, Node(pathNode))
            parentNode = pathNode

        leafName = nodeData['leaf']
        root.addChild(parentNode, Leaf(leafName, properties))

    return root['children']
