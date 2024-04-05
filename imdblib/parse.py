def list_nullable(cell: str):
    return "{" + cell + "}" if cell != "\\N" else ""


def id(cell: str):
    return cell[2:].lstrip("0")


def id_list_nullable(cell: str):
    if cell == "\\N":
        return ""
    else:
        return "{" + ",".join(map(id, cell.split(","))) + "}"


def text(cell: str):
    return '"{}"'.format(cell.replace('"', '""'))


def text_nullable(cell: str):
    return text(cell) if cell != "\\N" else ""


int_nullable = text_nullable


def boolean_nullable(cell: str):
    return bool(int(cell)) if cell != "\\N" else ""


def characters(cell: str):
    r"""
    characters table is too hard to serialize, it contains a JSON array string
    and some contain quote and comma on it, idk how to escape for postgres tsv

    solution: https://briandfoy.github.io/importing-array-values-into-postgres-from-csv/

    """
    if cell == "\\N":
        return ""

    import json

    try:
        arr = json.loads(cell)
    except Exception as _:
        raise Exception(f"json failed loading: '{cell}'")

    formatted_elements: list[str] = []
    for element in arr:
        # Escape double quotes and wrap the element in double quotes
        formatted_element = "'" + element.replace('"', '""') + "'"
        formatted_elements.append(formatted_element)

    # Join the formatted elements into a PostgreSQL array string
    formatted_cell = '"{' + ",".join(formatted_elements) + '}"'

    return formatted_cell
