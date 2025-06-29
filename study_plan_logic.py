def generate_study_plan(
    test_format: str,
    current_score: float,
    target_score: float,
    daily_hours: int,
    total_weeks: int
) -> dict:
    """
    Generate an IELTS study plan.

    Args:
        test_format (str): 'Academic' or 'General Training'
        current_score (float): your current overall band score (e.g. 5.5)
        target_score (float): your target band score (e.g. 7.0)
        daily_hours (int): number of hours per day you can study
        total_weeks (int): total number of weeks until test day

    Returns:
        dict: nested dict { 'Week 1': { 'Monday': [ {Hour, Task, Resources}, ... ], ... }, ... }
    """
    # Define task pools by section
    reading_tasks = [
        "Reading practice",
        "Skim & scan articles",
        "Time yourself with real tests",
        "Learn academic vocabulary",
        "Improve speed-reading",
    ]
    listening_tasks = [
        "Listening practice",
        "Dictation exercises",
        "Note-taking from lectures",
        "Identify speaker intent",
        "Practice accents (UK/US/AU)",
    ]
    writing_tasks_academic = [
        "Writing Task 1 (Graph/Table)",
        "Writing Task 2 (Essay)",
        "Analyze model answers",
        "Grammar & coherence focus",
        "Write under timed conditions",
    ]
    writing_tasks_general = [
        "Writing Task 1 (Letter)",
        "Writing Task 2 (Essay)",
        "Formal vs informal tone",
        "Structure practice",
        "Improve clarity & cohesion",
    ]
    speaking_tasks = [
        "Speaking Part 1 practice",
        "Speaking Part 2 cue cards",
        "Speaking Part 3 discussion",
        "Record & self-review",
        "Improve fluency & pronunciation",
    ]
    general_tasks = [
        "Vocabulary building",
        "Grammar review",
        "Mock test & review",
        "Test strategy review",
        "Feedback analysis"
    ]

    # Build full task pool based on test format
    tasks = []
    if test_format == "Academic":
        tasks += reading_tasks[:3] + listening_tasks[:3] + writing_tasks_academic[:3]
    else:
        tasks += reading_tasks[2:] + listening_tasks[2:] + writing_tasks_general[:3]
    tasks += speaking_tasks + general_tasks

    # Map each task to one or more high-quality resources
    resources = {
        "Reading practice": [
            "Cambridge IELTS Official Practice Tests",
            "British Council Reading sample tasks"
        ],
        "Skim & scan articles": [
            "BBC Learning English",
            "The Guardian Online Articles"
        ],
        "Time yourself with real tests": [
            "IELTS Liz Listening lessons",
            "Official IELTS Listening on IDP website"
        ],
        "Writing Task 1 (Graph/Table)": [
            "Cambridge IELTS Writing Model Answers",
            "IELTS Simon Task 1 explanations"
        ],
        "Writing Task 2 (Essay)": [
            "IELTS Advantage Writing Task 2 guide",
            "British Council Writing samples"
        ],
        "Speaking Part 1 practice": [
            "IELTS Speaking part 1 questions",
            "YouTube mock interviews"
        ],
        "Speaking Part 2 cue cards": [
            "IELTS Speaking part 2 cue-card exercises",
            "British Council Speaking sample videos"
        ],
        "Speaking Part 3 discussion": [
            "Topic-based discussions",
            "IELTS Speaking Band Descriptors"
        ],
        "Vocabulary building": [
            "Academic Word List flashcards (Anki deck)",
            "IELTS Vocabulary by Cambridge"
        ],
        "Grammar review": [
            "English Grammar in Use (Murphy)",
            "Cambridge Grammar for IELTS"
        ],
        "Mock test & review": [
            "Full practice test from Cambridge IELTS series",
            "Record yourself & self-evaluate with official band descriptors"
        ],
        "Test strategy review": [
            "IELTS Official Guide",
            "IELTS Liz Strategy Videos"
        ],
        "Feedback analysis": [
            "Review past test results",
            "Track weak areas weekly"
        ]
    }

    # Prepare day names and a repeating cycle of tasks
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    task_cycle = iter(tasks * (daily_hours * total_weeks * len(days_of_week)))

    # Build the nested plan structure
    plan = {}
    for week_index in range(1, total_weeks + 1):
        week_key = f"Week {week_index}"
        plan[week_key] = {}
        for day in days_of_week:
            hourly_plan = []
            for hour_slot in range(1, daily_hours + 1):
                try:
                    task = next(task_cycle)
                except StopIteration:
                    task = "Review previous day's material"
                hourly_plan.append({
                    "Hour": hour_slot,
                    "Task": task,
                    "Resources": resources.get(task, ["No specific resources"])
                })
            plan[week_key][day] = hourly_plan

    return plan