def aggregate(agType, *args, **kwargs):
    import aggregates

    return generic(aggregates, agType, **kwargs)

def generic(module, member, *args, **kwargs):
    memberModule = getattr(module, member)
    className = member.title()

    return getattr(memberModule, className)(*args, **kwargs)
