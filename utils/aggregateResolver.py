import ..aggregates

def resolve(self, type):
    agModule = getattr(aggregates, type)
    agClassName = '{}Aggregate'.format(type.title());

    return getattr(agModule, agClassName)()
