from itertools import chain

def resolve(json, path):
    components = path.split('.')
    current = json

    for component in components[:]:
        components.pop(0)

        if component == '*' and len(components) == 0:
            if isinstance(current, dict):
                return unwrap(current.keys())
            else:
                return current
        elif component == '*':
            results = []

            if isinstance(current, list):
                for i in range(len(current)):
                    deepRes = resolve(current[i], '.'.join(components))
                    results.append(deepRes)

            elif isinstance(current, dict):
                for key in current.keys():
                    deepRes = resolve(current[key], '.'.join(components))
                    results.append(deepRes)

            return unwrap(results)
        else:
            current = current[component]

    return current

def unwrap(l):
    return l.pop() if len(l) == 1 else l
