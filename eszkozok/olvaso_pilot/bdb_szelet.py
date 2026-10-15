"""A BDB-szeletelő élesben a szerver mellett él: `eszkozok/olvaso_szerver/bdb_szelet.py` (DT-F99c (a), felhasználói döntés 2026-10-15).

Ez a fájl csak betöltő: a pilot (`adat.py`, `meres.py`, `teszt_olvaso_pilot.py`) és az M0 mérőeszköz (`bdb_szelet_m0.py`) a régi
`import bdb_szelet` úton is az éles modult kapja, kódmásolás nélkül. A modul minden nevét (a `_`-sal kezdődőket is) átveszi.
"""
import importlib.util
import os

_UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'olvaso_szerver', 'bdb_szelet.py')
_spec = importlib.util.spec_from_file_location('bdb_szelet_eles', _UT)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
globals().update({k: v for k, v in vars(_m).items() if not (k.startswith('__') and k.endswith('__'))})
