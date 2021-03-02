import typing
import uuid


class Node(dict):
    def __init__(self, name, children=None):
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.id = str(uuid.uuid4())
        self.children = [] if not children else children

    def __search_node(self, name):
        if self.name == name:
            return self

        if not hasattr(self, "children"):
            return "Not found"

        for child in self.children:
            found = child.__search_node(name)
            if found != "Not found":
                return found

        return "Not found"

    def add_child(self, parent_name, child):
        # 'Name acts as soft id: A parent can not have two children with the same name'
        parent = self.__search_node(parent_name)
        if parent == "Not found":
            raise Exception("Parent not found! Name: " + parent_name)
        if not parent.__has_child(child.name):
            parent.children.append(child)

    def __has_child(self, child_name):
        if not hasattr(self, "children"):
            return False
        for child in self.children:
            if child.name == child_name:
                return True
        return False


class Leaf(Node):
    def __init__(self, name, properties):
        Node.__init__(self, name)
        for k, v in properties.items():
            self[k] = v
        del self.children


def flatten_data(data):
    # 'Adds type to path and adds the leaf as an external property for simplified processing'
    extra_nodes = {
        "Family Statuses": "Demographics",
        "Life Events": "Demographics",
        "Industries": "Demographics",
        "User Device": "Interests",
        "User Os": "Interests",
    }
    for node_data in data:
        node_type = ""
        if "type" in node_data.keys():
            if node_data["type"] and isinstance(node_data["type"], str):
                node_type = " ".join(node_data["type"].title().split("_"))
            else:
                node_type = ""
            if "path" in node_data.keys() and isinstance(node_data["path"], list):
                if node_type not in node_data["path"]:
                    node_data["path"].insert(0, node_type)
            else:
                node_data["path"] = [node_type]
            # del node_data['type']

        if node_type in extra_nodes.keys():
            node_type = extra_nodes[node_type]
            node_data["path"].insert(0, node_type)

        if node_data["name"] not in node_data["path"]:
            node_data["path"].append(node_data["name"])
        leaf_node = node_data["path"].pop()
        node_data["leaf"] = leaf_node
        del node_data["name"]

    return data


def map_interests(raw_interests: typing.List[typing.Dict] = None):
    if not raw_interests:
        raise ValueError("Invalid interests list. ")
    else:
        raw_results = raw_interests
    results = []
    for result in raw_results:
        if "fields" in result.keys():
            result = result["fields"]
        if "path" not in result.keys():
            result["path"] = ["Uncategorised"]
        if "key" not in result.keys() and "id" in result.keys():
            result["key"] = result.get("id")
        elif "key" not in result.keys() and "id" not in result.keys():
            result["key"] = str(uuid.uuid4())
        results.append(result)

    results = flatten_data(results)
    root = Node("Root")
    ignored_keys = ["leaf", "name"]

    for node_data in results:
        parent_node = "Root"
        properties = {}

        for k, v in node_data.items():
            if k not in ignored_keys:
                properties[k] = v

        for path_node in node_data["path"]:
            root.add_child(parent_node, Node(path_node))
            parent_node = path_node

        leaf_name = node_data["leaf"]
        root.add_child(parent_node, Leaf(leaf_name, properties))

    return root.children
