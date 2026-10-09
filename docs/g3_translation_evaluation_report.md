# G3 Translation Evaluation Report

Generated deterministically from 40 corpus sentences. This evaluates rule behavior; it is not a linguistic gold-standard score.

- Phrase recognition: 3/3
- Unknown-term rate: 20/148
- Unavailable-sign rate: 100/110
- Mean translation compute: 0.104 ms
- Outcomes: {"HEURISTIC":21,"SUPPORTED":5,"UNCERTAIN":14}
- Failure taxonomy: {"missing sign motion":35,"temporal ordering":3,"insufficient linguistic evidence":3,"question handling":4,"negation handling":3,"grammar gap":6,"lexical gap":3,"unknown vocabulary":8}
- G3 targeted improvements: baseline unknown terms 30 -> 20.

## Sign coverage

- Linguistic concepts: 14
- Playable motions: 3
- Incomplete/not-authored: 11
- Missing motion frequency: {"i":15,"water":16,"drink":7,"you":17,"need":9,"help":12,"me":12,"tomorrow":6,"how":1,"not":3,"thank_you":2}

## Decision evidence

The report shows whether the limiting factor is linguistic coverage or avatar motion coverage. The current corpus is expected to surface substantially more unavailable motion concepts than playable ones; do not infer an ML requirement from these rule/asset gaps alone.
