from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Any, Callable, Dict, Optional

CHALLENGES: Dict[int, Dict[int, Callable[[Path], Any]]] = {}


def challenge(day: int, part: Optional[int] = None):
    if day in CHALLENGES:
        existing_day = CHALLENGES[day]
    else:
        existing_day = {}
        CHALLENGES[day] = existing_day
    if part is None:
        part = len(existing_day)
    elif part in existing_day:
        raise ValueError(f"Day {day} part {part} is already assigned to {existing_day[part].__name__}")

    def wrapper(func: Callable[[Path], Any]) -> Callable[[Path], Any]:
        existing_day[part] = func
        return func

    return wrapper


# Automatically load all modules in the `aoc2022` package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([str(package_dir)]):  # type: ignore
    # import the module and iterate through its attributes
    if module_name != "__main__":
        module = import_module(f"{__name__}.{module_name}")
