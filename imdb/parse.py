def list_nullable(cell: str):
    return "{" + cell + "}" if cell != "\\N" else ""


def id(cell: str):
    return cell[2:].lstrip("0")


def id_list_nullable(cell: str):
    if cell == "\\N":
        return ""
    else:
        return "{" + ",".join(map(id, cell.split(","))) + "}"


def text_nullable(cell: str):
    return cell if cell != "\\N" else ""


int_nullable = text_nullable


def boolean_nullable(cell: str):
    return bool(int(cell)) if cell != "\\N" else ""


def characters(cell: str):
    import json

    if cell == "\\N":
        return ""

    def format_string(s: str):
        if "," in s or '"' in s:
            return '"{}"'.format(s.replace('"', '""'))
        else:
            return s

    return "{" + ",".join(map(format_string, json.loads(cell))) + "}"
