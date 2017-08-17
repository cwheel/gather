def aggregate(type, **kwargs):
    import aggregates

    agModule = getattr(aggregates, type)
    agClassName = '{}Aggregate'.format(type.title())

    return getattr(agModule, agClassName)(**kwargs)
