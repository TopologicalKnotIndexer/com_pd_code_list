"""Regenerate PD codes for the 1,783-name knot catalog with SageMath."""

from ast import literal_eval
from functools import cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
NAME_FILE = HERE / "HOMFLY-PT-reg.txt"
PRIME_PD_FILE = HERE / "pd_code_list.txt"
OUTPUT_FILE = HERE / "com_pd_code_list.txt"


@cache
def get_knot_name_list() -> list[str]:
    names: list[str] = []
    for line in NAME_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            names.append(stripped[1:-1].rsplit("|", 1)[1])
    return names


@cache
def get_prime_pd_codes() -> dict[str, list[list[int]]]:
    result: dict[str, list[list[int]]] = {}
    for line in PRIME_PD_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        name, raw_pd = stripped[1:-1].split("|", 1)
        value = literal_eval(raw_pd)
        if not isinstance(value, list):
            raise ValueError(f"PD code for {name} is not a list")
        result[name] = value
    return result


def _knot(pd_code: list[list[int]]):
    from sage.all import Knot

    return Knot(pd_code)


def get_connected_sum(pd_code_1: list, pd_code_2: list) -> list:
    return _knot(pd_code_1).connected_sum(_knot(pd_code_2)).pd_code()


def get_mirror_code(pd_code: list) -> list:
    return _knot(pd_code).mirror_image().pd_code()


@cache
def get_pd_code_by_prime_knot_name(knot_name: str) -> list:
    if "," in knot_name:
        raise ValueError("expected a prime knot name")
    mirrored = knot_name.startswith("m")
    base_name = knot_name[1:] if mirrored else knot_name
    try:
        pd_code = get_prime_pd_codes()[base_name]
    except KeyError as exc:
        raise KeyError(f"no prime PD code for {base_name}") from exc
    return get_mirror_code(pd_code) if mirrored else pd_code


def get_pd_code_by_knot_name(knot_name: str) -> list:
    components = [part.strip() for part in knot_name.split(",")]
    if not components or any(not part for part in components):
        raise ValueError("knot name contains an empty component")
    result = get_pd_code_by_prime_knot_name(components[0])
    for component in components[1:]:
        result = get_connected_sum(result, get_pd_code_by_prime_knot_name(component))
    return result


def get_pd_code_list_for_all_knots() -> str:
    return "".join(
        f"[{name}|{get_pd_code_by_knot_name(name)}]\n"
        for name in get_knot_name_list()
    )


if __name__ == "__main__":
    OUTPUT_FILE.write_text(get_pd_code_list_for_all_knots(), encoding="utf-8")
