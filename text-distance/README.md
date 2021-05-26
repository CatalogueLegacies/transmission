# Text Distance

This directory contains four files:

- `15pairs_16text-distance-metrics.txt` - the results of computing 16 different text distance functions (from the [Python textdistance package](https://pypi.org/project/textdistance/)) on 15 pairs of descriptions that were selected to exhibit varying degrees of copying and editing/addition. (local name is trial1_JB_handpickedpairs_RESULTS.txt).
- `RatcliffObershelp_sequenceMatcher_comparison.txt` - for each of 21 descriptions this gives four scores for 21 pairs (including a comparison of description with itself): (i) ratcliff_obershelp; (ii) SequenceMatcher.ratio; (iii) SequenceMatcher.quickratio (a quick estimate of the highest possible value); and (iv) SequenceMatcher.realquickratio (a very quick estimate of the highest possible value) . (local name is trial2_21LWLdescriptions_RESULTS_1.txt).
- `pairwiseComparisonResults.tsv` - a selection of 1649 LWL-BMSat pairs with sequenceMatcher.ratio > 0.5. Each tab-separated lines contains: sequenceMatcher.ratio; the length (in characters) of the LWL description; a Boolean value which is true if the string ‘British Museum online’ appears in the LWL description (case insensitive match); the LWL description; and, the BMSat description. (local name is trial3_LWL_X_BMSat_RESULTS.tsv )
- `pairwiseComparison.py` - the Python script used to make `pairwiseComparisonResults.tsv`. (local name is trial3_LWL_X_BMSat.py). NB this code is not properly commented (yet).
