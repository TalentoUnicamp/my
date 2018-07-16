def get_fields_and_properties(model, instance):
    field_names = [f.name for f in model._meta.fields]
    property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]
    return {name: getattr(instance, name) for name in field_names + property_names}
