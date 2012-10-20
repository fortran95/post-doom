def formatTitle(title):
    # Title is combined with letters, numbers, _, with no others.
    title = title.strip()
    if len(title) > 256:
        return False
    legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-0123456789'
    ret = ''
    for each in title:
        if each in legal:
            ret += each
        else:
            ret += '_'
    return ret
