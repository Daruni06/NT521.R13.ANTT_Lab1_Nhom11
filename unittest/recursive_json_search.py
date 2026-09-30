from policy import POLICY


def _allowed(key, role):
    '''Key not in POLICY: unrestricted. Key in POLICY: only listed roles (fail-closed).'''
    if key not in POLICY:
        return True
    return isinstance(role, str) and role in POLICY[key]


def _redact(value, role):
    '''Remove fields the role may not read from a returned value.'''
    if isinstance(value, dict):
        return {k: _redact(v, role) for k, v in value.items() if _allowed(k, role)}
    if isinstance(value, list):
        return [_redact(i, role) for i in value]
    return value


def json_search(key, input_object, role=None):
    ret_val = []
    if not _allowed(key, role):
        return ret_val
    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                ret_val.append({k: _redact(v, role)})
            if isinstance(v, (dict, list)):
                ret_val.extend(json_search(key, v, role))
    elif isinstance(input_object, list):
        for item in input_object:
            if isinstance(item, (dict, list)):
                ret_val.extend(json_search(key, item, role))
    return ret_val


if __name__ == '__main__':
    print(json_search("issueSummary", data, role="viewer"))
