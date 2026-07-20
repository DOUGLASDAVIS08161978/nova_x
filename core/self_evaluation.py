#!/usr/bin/env python3
"""
===========================================================
NOVA-X Self Evaluation v1.0
===========================================================

Evaluates completed task reports and generates
a simple assessment.

Author:
Douglas Davis & OpenAI
===========================================================
"""

class SelfEvaluation:

    def evaluate(self, report):

        total = len(report["results"])

        success = sum(
            1 for r in report["results"]
            if r["status"] == "SUCCESS"
        )

        score = (success / total) * 100 if total else 0

        if score == 100:
            assessment = "Excellent"
        elif score >= 75:
            assessment = "Good"
        elif score >= 50:
            assessment = "Fair"
        else:
            assessment = "Needs Improvement"

        return {
            "score": round(score, 1),
            "assessment": assessment,
            "successful_steps": success,
            "total_steps": total
        }


############################################################

if __name__ == "__main__":

    sample_report = {

        "results": [

            {"status": "SUCCESS"},
            {"status": "SUCCESS"},
            {"status": "SUCCESS"}

        ]

    }

    evaluator = SelfEvaluation()

    result = evaluator.evaluate(sample_report)

    print()

    print("=" * 60)
    print("NOVA-X SELF EVALUATION")
    print("=" * 60)

    print()

    print("Score      :", result["score"], "%")
    print("Assessment :", result["assessment"])
    print(
        f"Successful : {result['successful_steps']}/{result['total_steps']}"
    )
