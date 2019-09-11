def validate_punctuation(value):
    if not value:
        return ""
    return value.translate(
        value.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
    ).strip()
