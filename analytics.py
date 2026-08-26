"""Analytics - reads stored student activity events from MongoDB and
computes summary statistics.
"""

from db import get_collection

ACTIVITY_TYPES = [
    "login",
    "view_material",
    "assignment_submission",
    "quiz_completion",
]


def compute_stats():
    collection = get_collection()

    counts = {}
    for activity_type in ACTIVITY_TYPES:
        counts[activity_type] = collection.count_documents(
            {"activity_type": activity_type}
        )

    most_active = list(
        collection.aggregate(
            [
                {"$group": {"_id": "$student_id", "activity_count": {"$sum": 1}}},
                {"$sort": {"activity_count": -1}},
                {"$limit": 1},
            ]
        )
    )
    most_active_student = most_active[0] if most_active else None

    return {
        "total_logins": counts["login"],
        "total_material_views": counts["view_material"],
        "total_assignment_submissions": counts["assignment_submission"],
        "total_quiz_completions": counts["quiz_completion"],
        "most_active_student": most_active_student,
    }


def main():
    stats = compute_stats()
    print("Student Activity Analytics")
    print("---------------------------")
    print(f"Total Logins:                {stats['total_logins']}")
    print(f"Total Material Views:        {stats['total_material_views']}")
    print(f"Total Assignment Submissions:{stats['total_assignment_submissions']}")
    print(f"Total Quiz Completions:      {stats['total_quiz_completions']}")
    if stats["most_active_student"]:
        print(
            f"Most Active Student:         {stats['most_active_student']['_id']} "
            f"({stats['most_active_student']['activity_count']} activities)"
        )
    else:
        print("Most Active Student:         No data")
    return stats


if __name__ == "__main__":
    main()
