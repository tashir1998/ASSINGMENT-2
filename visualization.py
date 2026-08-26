"""Visualization - draws a bar chart of student activity statistics."""

import matplotlib.pyplot as plt

from analytics import compute_stats

OUTPUT_FILE = "student_activity_chart.png"


def main():
    stats = compute_stats()

    categories = ["Logins", "Views", "Assignments", "Quizzes"]
    counts = [
        stats["total_logins"],
        stats["total_material_views"],
        stats["total_assignment_submissions"],
        stats["total_quiz_completions"],
    ]
    colors = ["blue", "green", "orange", "red"]

    fig, ax = plt.subplots()
    bars = ax.bar(categories, counts, color=colors)

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
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
