
def calculate_rubric(scores, weights, max_marks=20):
    if set(scores) != set(weights):
        raise ValueError("Scores and weights must match.")

    if not weights or abs(sum(weights.values()) - 100) > 0.000001:
        raise ValueError("Rubric weights must total 100%.")

    if max_marks <= 0:
        raise ValueError("Maximum marks must be positive.")

    details = {}
    total = 0

    for criterion, weight in weights.items():
        score = scores[criterion]

        if not 0 <= score <= 100:
            raise ValueError(f"Invalid score for {criterion}.")

        marks = (score / 100) * (weight / 100) * max_marks

        details[criterion] = {
            "percentage": score,
            "weight": weight,
            "marks": round(marks, 2),
        }

        total += marks

    return {
        "total_score": round(total, 2),
        "maximum_marks": max_marks,
        "criteria": details,
    }
