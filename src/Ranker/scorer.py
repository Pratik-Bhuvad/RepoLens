"""
scorer.py — Ranker Layer: Scorer
----------------------------------
Second pass. Calculates a score for each repo that passed gate.py.
Score is a float between 0.0 and 1.0.
Each field's contribution is normalized then multiplied by its weight.
 
Job: attach a score to each repo. Nothing else.
Input:  list of gated repo dicts
Output: same list with 'score' and 'score_breakdown' added to each repo
"""

import math
from .weights import SCORE_WEIGHTS
