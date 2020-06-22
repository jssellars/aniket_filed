from textdistance import jaro_winkler

__MATCH_THRESHOLD__ = 0.85

def match_strings(source_string, target_string):
    similarity = jaro_winkler(source_string, target_string)

    if similarity > __MATCH_THRESHOLD__:
        return True
    else:
        return False