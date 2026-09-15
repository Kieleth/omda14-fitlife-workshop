"""Comprueba el entorno local sin leer claves ni llamar a un LLM."""

import csv
from dataclasses import dataclass
from importlib import import_module, metadata
from pathlib import Path
import platform
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parent
PACKAGES = {
    "streamlit": "streamlit",
    "openai": "openai",
    "pandas": "pandas",
    "python-dotenv": "dotenv",
}
DATASETS = {
    "fitlife_members.csv": (
        16334,
        {"member_id", "month", "center", "plan", "price_paid", "signup_date",
         "acquisition_channel", "tenure_months", "visits_this_month",
         "group_classes_attended", "uses_app", "has_personal_trainer",
         "cost_to_serve", "status", "churn_reason"},
    ),
    "fitlife_context.csv": (
        36,
        {"month", "competitor_lowcost_price", "campaign_active", "service_incident",
         "monthly_fixed_costs", "avg_occupancy_rate", "acquisition_cost_avg"},
    ),
}


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def expected_packages(root: Path) -> dict[str, str]:
    path = root / "requirements.in"
    if not path.is_file():
        raise FileNotFoundError(f"Falta {path.name}. Recupera el archivo del repositorio.")
    versions = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-z-]+)==([0-9.]+)", line)
        if match is None:
            raise ValueError(f"Formato de dependencia no válido en {path.name}: {line!r}")
        name, version = match.groups()
        if name in versions:
            raise ValueError(f"Dependencia duplicada en {path.name}: {name}")
        versions[name] = version
    if versions.keys() != PACKAGES.keys():
        raise ValueError("requirements.in debe declarar streamlit, openai, pandas y python-dotenv.")
    return versions


def check_dataset(root: Path, filename: str, expected_rows: int, columns: set[str]) -> Check:
    path = root / "data" / filename
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            fields = reader.fieldnames
            if fields is None or len(fields) != len(set(fields)) or set(fields) != columns:
                return Check(filename, False, "Las columnas no coinciden con FitLife. Recupera el CSV del repositorio.")
            rows = 0
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    return Check(filename, False, f"Fila {reader.line_num} incompleta o con campos de más. Recupera el CSV original.")
                rows += 1
    except (OSError, UnicodeError, csv.Error) as error:
        return Check(filename, False, f"No se puede leer data/{filename}: {error}. Recupera el CSV del repositorio.")
    if rows != expected_rows:
        return Check(filename, False, f"Se esperaban {expected_rows} filas y hay {rows}. Recupera el CSV original.")
    return Check(filename, True, f"{rows:,} filas y {len(columns)} columnas verificadas.")


def run_checks(root: Path = ROOT) -> list[Check]:
    versions = expected_packages(root)
    version_file = root / ".python-version"
    target_python = version_file.read_text(encoding="utf-8").strip()
    if re.fullmatch(r"3\.\d+", target_python) is None:
        raise ValueError(".python-version debe indicar una versión de Python como 3.13.")
    current_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    git_path = shutil.which("git")
    checks = [
        Check("Python", current_python == target_python,
              f"Python {platform.python_version()}. El taller usa Python {target_python}. Intérprete: {sys.executable}"),
        Check("Entorno aislado", sys.prefix != sys.base_prefix,
              "Usa el Python de .venv indicado en SETUP.md para instalar y ejecutar el taller."),
        Check("Git", git_path is not None,
              "Git encontrado." if git_path else "Instala Git siguiendo SETUP.md y vuelve a abrir la terminal."),
    ]
    for name, module in PACKAGES.items():
        try:
            installed = metadata.version(name)
            import_module(module)
        except (metadata.PackageNotFoundError, ImportError, OSError) as error:
            checks.append(Check(name, False, f"No se puede cargar {name}: {error}. Repite la instalación completa de requirements.txt en .venv."))
        else:
            checks.append(Check(name, installed == versions[name],
                                f"Instalada {installed}; versión del taller: {versions[name]}."
                                + (" Repite la instalación de requirements.txt." if installed != versions[name] else "")))
    for name, (rows, columns) in DATASETS.items():
        checks.append(check_dataset(root, name, rows, columns))
    return checks


def main() -> int:
    checks = run_checks()
    for check in checks:
        print(f"{'OK' if check.ok else 'ERROR'} | {check.name}: {check.detail}")
    ok = all(check.ok for check in checks)
    print("Entorno local preparado. Falta abrir y probar la app de Streamlit."
          if ok else "Instalación incompleta. Corrige los errores antes de clase.")
    print("Este chequeo no prueba una conexión con un LLM ni lee tu API key.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
