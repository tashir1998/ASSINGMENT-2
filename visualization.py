"""Visualization - reads student activity statistics from MongoDB and
draws a bar chart.
"""

import matplotlib.pyplot as plt
from pymongo import MongoClient

# TODO: replace <db_password> with the real password for fatehanasrin7976_db_user
MONGO_URI = "mongodb+srv://fatehanasrin7976_db_user:<db_password>@cluster0.idqmng1.mongodb.net/?appName=Cluster0"
MONGO_DB_NAME = "student_activity_db"
MONGO_COLLECTION = "student_events"

OUTPUT_FILE = "student_activity_chart.png"

ACTIVITY_TYPES = [
    "login",
    "view_material",
    "assignment_submission",
    "quiz_completion",
]


def compute_stats():
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB_NAME][MONGO_COLLECTION]

    counts = {
        activity_type: collection.count_documents({"activity_type": activity_type})
        for activity_type in ACTIVITY_TYPES
    }
    client.close()
    return counts


def main():
    counts = compute_stats()

    categories = ["Logins", "Views", "Assignments", "Quizzes"]
    values = [
        counts["login"],
        counts["view_material"],
        counts["assignment_submission"],
        counts["quiz_completion"],
    ]
    colors = ["blue", "green", "orange", "red"]

    fig, ax = plt.subplots()
    bars = ax.bar(categories, values, color=colors)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
        )

    ax.set_title("Student Activity Analytics")
    ax.set_xlabel("Activity Type")
    ax.set_ylabel("Count")

    fig.savefig(OUTPUT_FILE)
    print(f"Chart saved to {OUTPUT_FILE}")
    plt.show()


if __name__ == "__main__":
    main()
