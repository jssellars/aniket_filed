import copy
from dataclasses import fields, _asdict_inner, _is_dataclass_instance
from enum import Enum, Flag, _decompose, auto
from typing import Any, Dict, Optional, Tuple, Type, Union

from humps import decamelize


def enrich_flag(cls: Type[Flag]) -> Type[Flag]:
    """Add NONE and ALL pseudo-members to Flag enumeration."""
    none_member = cls(0)
    none_member._name_ = "_NONE_"
    cls._member_map_[none_member._name_] = none_member
    # TODO: should be used when more than one member exists,
    #  but it's confusing when a single element enum is missing it
    # all_member = cls(0)
    # for member in cls:
    #     all_member |= member
    # all_member._name_ = "_ALL_"
    # cls._member_map_[all_member._name_] = all_member

    # TODO: components should output [] for _NONE_
    setattr(
        cls, "components", property(lambda self: [self] if self in cls else _decompose(cls, self.value)[0]),
    )
    setattr(cls, "names", property(lambda self: [i.name for i in self.components]))
    setattr(cls, "names_repr", property(lambda self: "|".join(self.names)))

    return cls


class Cat:
    """A catalog. Not a cat.

    It walks like a catalog and meows like a catalog,
    therefore it's a catalog as per duck typing standards."""

    def __init__(
        self,
        name_sdk: Optional[str],
        *items: Union[Enum],
        default_item: Union[Enum, None] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        # the following must be filled by enum decorator
        self.name: Optional[str] = None
        self.kind: Optional[str] = None
        # regular members
        self.name_sdk: Optional[str] = name_sdk
        self.items: Tuple["Cat", ...] = tuple(i.value if isinstance(i, Enum) else i for i in items)
        self.default_item: Optional["Cat", Enum] = default_item
        self.display_name: Optional[str] = display_name
        self.description: Optional[str] = description
        self.display_name_autogen: Optional[str] = None
        self.description_autogen: Optional[str] = None
        self.image_name_autogen: Optional[str] = None

    def as_dict(self, expand_items: bool = True) -> Dict:
        return Cat.as_cat_dict(self, expand_items)

    @classmethod
    def as_cat_dict(cls, obj, expand_cat_items: bool = True) -> Any:
        # Cat-specific
        if isinstance(obj, cls):
            result = {}
            for k, v in vars(obj).items():
                if k == "name_sdk" or v is None:
                    continue

                if k == "default_item" and isinstance(v, (Cat, Enum)):
                    result_value = v.name
                elif k == "items":
                    if expand_cat_items:
                        result_value = {i.name: i.as_dict() for i in v if isinstance(i, (Cat, Enum))}
                    else:
                        result_value = [i.name if isinstance(i, (Cat, Enum)) else i for i in v]
                else:
                    result_value = cls.as_cat_dict(v)

                result[k] = result_value

            return result

        if isinstance(obj, Enum):
            if hasattr(obj, "names_repr"):
                return cls.as_cat_dict(obj.names)

            return cls.as_cat_dict(obj.value)

        # From dataclass
        if _is_dataclass_instance(obj):
            return {f.name: _asdict_inner(getattr(obj, f.name), dict) for f in fields(obj)}

        if isinstance(obj, tuple) and hasattr(obj, "_fields"):
            return type(obj)(*[cls.as_cat_dict(v) for v in obj])

        if isinstance(obj, (list, tuple)):
            return type(obj)(cls.as_cat_dict(v) for v in obj)

        if isinstance(obj, dict):
            return type(obj)((cls.as_cat_dict(k), cls.as_cat_dict(v)) for k, v in obj.items())

        return copy.deepcopy(obj)

    def with_metadata_from(self, other: Enum) -> "Cat":
        other_value: Cat = other.value
        self.display_name = other_value.display_name or other_value.display_name_autogen
        self.description = other_value.description or other_value.description_autogen

        return self

    def enrich(self, kind: str, name: str) -> None:
        self.kind = kind
        self.name = name
        self.generate_metadata_post_init()

    def generate_metadata_post_init(self) -> None:
        self.display_name_autogen = self.name.replace("_", " ").title()
        self.description_autogen = self.name.replace("_", " ").casefold().capitalize() + "."
        self.image_name_autogen = f"{decamelize(self.kind)}__{self.name}".replace("_", "-").casefold()


@enrich_flag
class Contexts(Flag):
    SMART_CREATE = auto()
    # Reserved for future use
    # EDIT = auto()
    # SMART_CREATE_PLUS = auto()

    def as_cat_with_items(self, *items: Enum, default_item: Enum) -> Cat:
        result = Cat(None, *items, default_item=default_item)
        result.enrich(Contexts.__name__, self.name)

        return result

    @classmethod
    def all_with_items(cls, *items: Enum, default_item: Optional[Enum] = None) -> Dict["Contexts", Cat]:
        if default_item is None and items:
            default_item = items[0]

        return {i: i.as_cat_with_items(*items, default_item=default_item) for i in cls}


def cat_enum(cls: Type[Enum]) -> Type[Enum]:
    """Add Cat-specific data and methods to enum."""
    # non-Enum member handling
    contexts_attr_name = "contexts"
    joint_fields_attr_name = "joint_fields"
    cls._ignore_ = [joint_fields_attr_name, contexts_attr_name]

    try:
        getattr(cls, joint_fields_attr_name)
    except AttributeError:
        cls.joint_fields = []
    else:
        cls._member_map_.pop(joint_fields_attr_name)
        cls._member_names_.remove(joint_fields_attr_name)

    try:
        contexts = getattr(cls, contexts_attr_name)
    except AttributeError:
        members = list(cls._member_map_)
        cls.contexts = Contexts.all_with_items(*members, default_item=members[0])
    else:
        cls._member_map_.pop(contexts_attr_name)
        cls._member_names_.remove(contexts_attr_name)
        cls.contexts = contexts.value

    def contexts_as_dict(cls_) -> Dict:
        return {
            flag.name: cat.as_dict(expand_items=False)
            for context, cat in cls_.contexts.items()
            for flag in context.components
        }

    setattr(
        cls, "contexts_as_dict", classmethod(contexts_as_dict),
    )

    def as_dict(cls_) -> Dict:
        result = {member_.name: member_.value.as_dict() for member_ in cls_}
        result[contexts_attr_name] = cls_.contexts_as_dict()

        return result

    setattr(
        cls, "as_dict", classmethod(as_dict),
    )

    # Enum member handling, members have Cat type value
    for member in cls:
        if isinstance(member.value, Cat):
            member.value.enrich(cls.__name__, member.name)

    return cls
