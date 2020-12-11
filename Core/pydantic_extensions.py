import re
from typing import Dict, Type, Any, Callable

from pydantic import BaseModel, validate_model, root_validator


def copy_and_update_model_with_validation(model: BaseModel, update: Dict) -> BaseModel:
    result = model.copy(update=update)
    data, fields, error = validate_model(type(model), result.dict())
    if error:
        raise error

    return result


def patch_model(model_type: Type[BaseModel], field: str, update: Dict) -> BaseModel:
    return replace_in_class(get_field_default(model_type, field), **update)


def get_field_default(model_type: Type[BaseModel], field: str) -> Any:
    return model_type.__fields__[field].default


def replace_in_model_orig(model: BaseModel, **replace: Any) -> BaseModel:
    return type(model)(**{**model.dict(), **replace})


def replace_in_class(model: BaseModel, **replace: Any) -> BaseModel:
    return type(model)(**{**{k: v for k, v in vars(model).items() if not k.startswith("_")}, **replace})


def format_templates_validator():
    def format_templates(cls, values):
        return {k: format_templates_recursive(v, values) for k, v in values.items()}

    """
    class Example(BaseModel):
        _format_templates_validator = format_templates_validator
    """
    return root_validator(allow_reuse=True)(format_templates)


def patch(other_model_type: Type[BaseModel]) -> Callable:
    """
    @patch
    class Example(BaseModel):
        ...
    """
    def decorator(cls: Type[BaseModel]) -> Type[BaseModel]:
        patched_fields = {k: v for k, v in other_model_type.__fields__.items() if v.default}
        for k, v in cls.__fields__.items():
            if k not in patched_fields:
                continue

            v.default = patched_fields[k].default
            cls.__fields__[k] = v

        return cls

    return decorator


def patch_alternate(cls) -> Callable:
    """
    @patch_alternate
    class Example(BaseModel):
        _format_templates_validator = format_templates_validator
    """
    setattr(cls, "_format_templates_validator", format_templates_validator)

    return cls


def get_model_with_formatted_templates(cls: Type[BaseModel]) -> Type[BaseModel]:
    values = {k: v.default for k, v in cls.__fields__.items()}

    for k, v in values.items():
        cls.__fields__[k].default = format_templates_recursive(v, values)

    return cls


def get_value_by_template_id(values: Dict, template_id: str) -> Any:
    env = values["environment"]
    env_domain_url = values["environment_domain_url"] or env

    return dict(
        domain=values["domain"],
        env=env,
        Env=env.title(),
        env_domain_url=env_domain_url,
        Env_domain_url=env_domain_url.title(),
        app_domain=values["name"].domain,
        app_name=values["name"].name,
        app_kind=values["name"].kind,
    ).get(template_id)


def format_templates_recursive(value, all_values):
    if isinstance(value, BaseModel):
        for field in value.__fields__:
            setattr(value, field, format_templates_recursive(getattr(value, field), all_values))

        return value

    if isinstance(value, dict):
        return type(value)(**{k: format_templates_recursive(v, all_values) for k, v in value.items()})

    if isinstance(value, (tuple, list)):
        return type(value)(format_templates_recursive(i, all_values) for i in value)

    if isinstance(value, str):
        return format_template(value, all_values)

    return value


TEMPLATE_PATTERN = re.compile(r"\{\w+\}")


def format_template(v, values):
    is_domain_url = values["domain"] in v
    for match in re.findall(TEMPLATE_PATTERN, v):
        templated_id = match[1:-1]
        if is_domain_url and templated_id == "env":
            templated_id = "env_domain_url"
        value = get_value_by_template_id(values, templated_id)
        if value:
            v = v.replace("{" + templated_id + "}", value)

    return v


def patch_field_defaults(non_model_class):
    """
    @patch_field_defaults(pydantic_model)
    class Example:
        ...
    """
    def decorator(cls):
        for k, v in non_model_class.__dict__.items():
            if not k.startswith("_"):
                cls.__fields__[k].default = v

        return cls

    return decorator
