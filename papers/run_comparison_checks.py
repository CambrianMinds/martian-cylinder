"""Run the existing comparison tests after the reconstruction-script move."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'independent-reconstruction/scripts'))
suite = unittest.defaultTestLoader.discover(
    str(ROOT/'audit/comparative-study/scripts'), pattern='test_analysis.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
