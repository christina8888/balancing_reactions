from chempy import balance_stoichiometry


def balance(user_input_reac, user_input_prod):
    try:
        reac, prod = balance_stoichiometry(user_input_reac.split(), user_input_prod.split())
    except Exception:
        result = "Неверный ввод реактантов или продуктов"
        return result

    left = []
    right = []

    for key, value in reac.items():
        _ = [str(value), key]
        joined = ' '.join(_)
        left.append(joined)

    for key, value in prod.items():
        _ = [str(value), key]
        joined = ' '.join(_)
        right.append(joined)

    sep1 = ' -> '
    sep2 = ' + '

    left_sep = sep2.join(left)
    right_sep = sep2.join(right)

    result = left_sep + sep1 + right_sep

    return result
