"""
Smoke tests for scripts/lookup.py.

Estos tests asumen que la API de Bitlan está accesible. Si no, los marcados
con `@requires_network` se saltan automáticamente.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Permitir importar lookup.py desde tests/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import lookup as lk  # noqa: E402


# ---------------------------------------------------------------------------
# normalize_text — unit tests, sin red
# ---------------------------------------------------------------------------

class TestNormalizeText:
    def test_handles_none(self):
        assert lk.normalize_text(None) == ""

    def test_handles_empty(self):
        assert lk.normalize_text("") == ""

    def test_strips_accents(self):
        assert lk.normalize_text("Diabétes") == "diabetes"

    def test_lowercases(self):
        assert lk.normalize_text("DIABETES") == "diabetes"

    def test_trims(self):
        assert lk.normalize_text("  diabetes  ") == "diabetes"

    def test_combined(self):
        assert lk.normalize_text("  Azúcar Alta  ") == "azucar alta"


class TestFuzzyMatch:
    def test_matches_primary(self):
        assert lk.fuzzy_match("diabetes", "Diabetes tipo 2", ["azucar alta"])

    def test_matches_accent_insensitive(self):
        assert lk.fuzzy_match("azucar", "Diabetes tipo 2", ["azúcar alta"])

    def test_matches_synonym(self):
        assert lk.fuzzy_match("tiroides baja", "Hipotiroidismo", ["tiroides baja"])

    def test_no_match(self):
        assert not lk.fuzzy_match("gripe", "Diabetes tipo 2", ["azucar alta"])

    def test_empty_query_matches_all(self):
        assert lk.fuzzy_match("", "Cualquier cosa", [])

    def test_partial_substring(self):
        assert lk.fuzzy_match("diab", "Diabetes tipo 2", [])


# ---------------------------------------------------------------------------
# Sample del catálogo — usa reference/catalog-sample.json (sin red)
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_catalog():
    path = ROOT / "reference" / "catalog-sample.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


class TestSampleShape:
    def test_has_rows(self, sample_catalog):
        assert "rows" in sample_catalog
        assert len(sample_catalog["rows"]) >= 5

    def test_each_row_has_required_keys(self, sample_catalog):
        required = {"id", "slug", "name_es", "synonyms_es", "category",
                    "lay_explainer_es", "requires_medical_referral",
                    "display_order"}
        for row in sample_catalog["rows"]:
            missing = required - set(row.keys())
            assert not missing, f"Row {row.get('slug')} le faltan: {missing}"

    def test_diabetes_t1_requires_referral(self, sample_catalog):
        row = next(r for r in sample_catalog["rows"] if r["slug"] == "diabetes_t1")
        assert row["requires_medical_referral"] is True

    def test_diabetes_t2_does_not_require_referral(self, sample_catalog):
        row = next(r for r in sample_catalog["rows"] if r["slug"] == "diabetes_t2")
        assert row["requires_medical_referral"] is False


# ---------------------------------------------------------------------------
# Integración con API en vivo — opcional
# ---------------------------------------------------------------------------

requires_network = pytest.mark.skipif(
    "--no-network" in sys.argv,
    reason="Saltado con --no-network",
)


@requires_network
class TestLiveAPI:
    def test_fetch_catalog_returns_rows(self):
        data = lk.fetch_catalog(force_refresh=True)
        assert "rows" in data
        assert len(data["rows"]) > 0

    def test_lookup_diabetes(self):
        result = lk.lookup("diabetes", force_refresh=True)
        assert result["total_matched"] >= 1
        assert any("diabetes" in m["name_es"].lower() for m in result["matches"])

    def test_lookup_synonym(self):
        result = lk.lookup("tiroides baja", force_refresh=True)
        assert result["total_matched"] >= 1
        assert any(m["slug"] == "hipotiroidismo" for m in result["matches"])

    def test_lookup_accent_insensitive(self):
        result = lk.lookup("azucar alta", force_refresh=True)
        assert result["total_matched"] >= 1

    def test_lookup_no_match_returns_zero(self):
        result = lk.lookup("xyzqwerty123", force_refresh=True)
        assert result["total_matched"] == 0
        assert result["matches"] == []

    def test_disclaimer_always_present(self):
        result = lk.lookup("diabetes", force_refresh=True)
        assert "disclaimer_general" in result
        assert "no diagnóstico médico" in result["disclaimer_general"]

    def test_referral_disclaimer_when_required(self):
        result = lk.lookup("diabetes tipo 1", force_refresh=True)
        if any(m["requires_medical_referral"] for m in result["matches"]):
            assert result["disclaimer_medical_referral"] is not None
