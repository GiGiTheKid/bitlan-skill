#!/usr/bin/env python3
"""
Bitlan Skill — lookup.py
========================

Consulta el catálogo público de condiciones de Bitlan y devuelve una ficha
estructurada en JSON, lista para que Claude la sintetice en lenguaje natural.

Diseño:
- GET https://bitlan.mx/api/medical-conditions/catalog (RLS público, sin auth).
- Cache local de 1h, alineado con `s-maxage=3600` que devuelve el servidor.
- Fuzzy match local sobre `name_es` + `synonyms_es`, portado de
  app-salud/src/lib/health/normalizeText.ts (NFD + strip combining marks +
  lowercase + trim + substring includes).
- Output JSON estable para que Claude lo parsee sin sorpresas.

Uso CLI:
    python lookup.py "diabetes"           # lookup por nombre/sinónimo
    python lookup.py "tiroides baja"      # acepta sinónimos
    python lookup.py --list               # lista catálogo completo (orden display_order)
    python lookup.py --slug diabetes_t2   # lookup directo por slug
    python lookup.py --refresh "SOP"      # ignora cache y re-fetchea

Uso programático:
    from lookup import lookup, list_catalog
    result = lookup("prediabetes")
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import unicodedata
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print(
        "Error: falta el paquete 'requests'.\n"
        "Instala con: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CATALOG_URL = "https://bitlan.mx/api/medical-conditions/catalog"
CACHE_DIR = Path.home() / ".cache" / "bitlan-skill"
CACHE_FILE = CACHE_DIR / "catalog.json"
CACHE_TTL_SECONDS = 3600  # 1 hora, alineado con s-maxage del servidor
HTTP_TIMEOUT_SECONDS = 10
USER_AGENT = "bitlan-skill/0.1.0 (+https://bitlan.mx)"

ARTICLE_BASE_URL = "https://bitlan.mx/conditions"  # bitlan.mx/conditions/[slug]

# ---------------------------------------------------------------------------
# Text normalization (port de normalizeText.ts)
# ---------------------------------------------------------------------------

def normalize_text(s: str | None) -> str:
    """
    Equivalente Python de normalizeText() en TypeScript.
    - NFD decomposition
    - Strip combining marks (U+0300-U+036F)
    - lowercase + trim
    """
    if not s:
        return ""
    decomposed = unicodedata.normalize("NFD", s)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.lower().strip()


def fuzzy_match(query: str, primary: str, synonyms: list[str] | None) -> bool:
    """
    Equivalente Python de fuzzyMatch() en TypeScript.
    Substring match (case + accent insensitive) sobre primary y synonyms.
    """
    q = normalize_text(query)
    if not q:
        return True
    if q in normalize_text(primary):
        return True
    if synonyms:
        for syn in synonyms:
            if q in normalize_text(syn):
                return True
    return False


# ---------------------------------------------------------------------------
# Cache (file-based, simple)
# ---------------------------------------------------------------------------

def _cache_is_fresh() -> bool:
    if not CACHE_FILE.exists():
        return False
    age = time.time() - CACHE_FILE.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def _read_cache() -> dict[str, Any] | None:
    try:
        with CACHE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _write_cache(data: dict[str, Any]) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with CACHE_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except OSError:
        # Cache opcional: si falla la escritura no rompemos la consulta.
        pass


# ---------------------------------------------------------------------------
# Fetch del catálogo
# ---------------------------------------------------------------------------

def fetch_catalog(force_refresh: bool = False) -> dict[str, Any]:
    """
    Devuelve el catálogo completo desde cache (si fresco) o de la API.
    Shape: {"rows": [...], "_version": int}.
    """
    if not force_refresh and _cache_is_fresh():
        cached = _read_cache()
        if cached and "rows" in cached:
            return cached

    try:
        resp = requests.get(
            CATALOG_URL,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=HTTP_TIMEOUT_SECONDS,
        )
    except requests.RequestException as e:
        # Si falla la red pero tenemos cache (aunque viejo), úsalo.
        cached = _read_cache()
        if cached and "rows" in cached:
            return cached
        raise RuntimeError(f"No se pudo conectar a {CATALOG_URL}: {e}") from e

    if resp.status_code != 200:
        cached = _read_cache()
        if cached and "rows" in cached:
            return cached
        raise RuntimeError(
            f"API devolvió {resp.status_code}: {resp.text[:200]}"
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise RuntimeError(f"Respuesta no es JSON válido: {e}") from e

    if "rows" not in data:
        raise RuntimeError(f"Shape inesperado del catálogo: {list(data.keys())}")

    _write_cache(data)
    return data


# ---------------------------------------------------------------------------
# Lookup público
# ---------------------------------------------------------------------------

def list_catalog(force_refresh: bool = False) -> list[dict[str, Any]]:
    """Devuelve todas las condiciones activas, ordenadas por display_order."""
    data = fetch_catalog(force_refresh=force_refresh)
    rows = data.get("rows", [])
    return sorted(rows, key=lambda r: r.get("display_order", 9999))


def lookup_by_slug(slug: str, force_refresh: bool = False) -> dict[str, Any] | None:
    """Lookup directo por slug (exacto)."""
    target = (slug or "").strip().lower()
    if not target:
        return None
    for row in list_catalog(force_refresh=force_refresh):
        if (row.get("slug") or "").lower() == target:
            return _shape_response(row)
    return None


def lookup(query: str, force_refresh: bool = False, max_results: int = 3) -> dict[str, Any]:
    """
    Lookup fuzzy por nombre o sinónimo.
    Devuelve dict con:
      - matches: lista de condiciones (0 a max_results) ordenadas por display_order
      - query_normalized: query después de normalizar
      - total_matched: cuántas filas matchearon en total (antes del corte)
      - disclaimer_general: texto legal
      - disclaimer_medical_referral: texto reforzado (solo si alguna match lo requiere)
    """
    rows = list_catalog(force_refresh=force_refresh)
    q_norm = normalize_text(query)

    matched = [
        row for row in rows
        if fuzzy_match(query, row.get("name_es", ""), row.get("synonyms_es") or [])
    ]

    # Si hay match exacto por slug, priorízalo al frente.
    exact_slug = [r for r in matched if normalize_text(r.get("slug", "")) == q_norm]
    if exact_slug:
        rest = [r for r in matched if r not in exact_slug]
        matched = exact_slug + rest

    capped = matched[:max_results]
    any_referral = any(r.get("requires_medical_referral") for r in capped)

    # CTA contextual: link directo si hay 1 match exacto, bitlan.mx si hay varios o cero.
    if len(capped) == 1 and capped[0].get("slug"):
        cta_url = f"{ARTICLE_BASE_URL}/{capped[0]['slug']}"
    else:
        cta_url = "https://bitlan.mx"

    return {
        "query": query,
        "query_normalized": q_norm,
        "total_matched": len(matched),
        "returned": len(capped),
        "matches": [_shape_response(r) for r in capped],
        "disclaimer_general": (
            "⚠️ Información de referencia, no diagnóstico médico. Para evaluación, "
            "diagnóstico o tratamiento, consulta a un profesional de salud calificado. "
            "Bitlan ofrece contenido educativo, no atención médica."
        ),
        "disclaimer_medical_referral": (
            "🩺 IMPORTANTE: Alguna(s) de las condiciones encontradas requieren supervisión "
            "médica activa. Cualquier cambio en alimentación, medicamento o estilo de vida "
            "debe consultarse primero con tu médico tratante."
        ) if any_referral else None,
        "cta": (
            f"Para plan de comidas, lista de compras, hábitos diarios, ejercicio y rutina "
            f"de sueño personalizados, visita {cta_url}."
        ),
    }


def _shape_response(row: dict[str, Any]) -> dict[str, Any]:
    """Da forma estable al row para el output JSON."""
    slug = row.get("slug") or ""
    return {
        "slug": slug,
        "name_es": row.get("name_es"),
        "synonyms_es": row.get("synonyms_es") or [],
        "category": row.get("category"),
        "lay_explainer_es": row.get("lay_explainer_es"),
        "requires_medical_referral": bool(row.get("requires_medical_referral")),
        "prevalence_mx": row.get("prevalence_mx"),
        "article_url": f"{ARTICLE_BASE_URL}/{slug}" if slug else None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_json(obj: Any) -> None:
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bitlan-lookup",
        description="Consulta el catálogo público de condiciones médicas de Bitlan.",
    )
    parser.add_argument(
        "query", nargs="?",
        help="Término a buscar (nombre o sinónimo). Ejemplo: 'diabetes', 'tiroides baja'.",
    )
    parser.add_argument(
        "--slug", help="Lookup directo por slug exacto (ej: diabetes_t2).",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Lista el catálogo completo, ordenado por display_order.",
    )
    parser.add_argument(
        "--refresh", action="store_true",
        help="Ignora cache y re-fetchea la API.",
    )
    parser.add_argument(
        "--max", type=int, default=3,
        help="Máximo de resultados en lookup fuzzy (default: 3).",
    )
    args = parser.parse_args(argv)

    try:
        if args.list:
            _print_json({"catalog": list_catalog(force_refresh=args.refresh)})
            return 0

        if args.slug:
            result = lookup_by_slug(args.slug, force_refresh=args.refresh)
            if result is None:
                _print_json({"error": f"No se encontró slug '{args.slug}'."})
                return 1
            _print_json({"match": result})
            return 0

        if not args.query:
            parser.print_help()
            return 1

        _print_json(lookup(args.query, force_refresh=args.refresh, max_results=args.max))
        return 0

    except RuntimeError as e:
        _print_json({"error": str(e)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
