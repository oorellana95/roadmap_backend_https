def set_object_attributes_from_kwargs(object_to_update, kwargs):
    for key, value in kwargs.items():
        setattr(object_to_update, key, value)
