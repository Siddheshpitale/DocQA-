MIN_SIMILARITY = 0.35
DROP_THRESHOLD = 0.25


def dynamic_retrieve(results):
    selected = []

    for i, r in enumerate(results):
        if r["score"] < MIN_SIMILARITY:
            break

        if i > 0:
            prev_score = results[i - 1]["score"]
            if (prev_score - r["score"]) > DROP_THRESHOLD:
                break

        selected.append(r)
    
    if len(selected) < 3 and len(results) >= 3:
        selected = results[:3]

    return selected
