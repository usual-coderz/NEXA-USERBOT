def generate_schedule(tasks, start_time):
    schedule = []
    current = start_time

    for task in tasks:
        duration = task.get("duration", 1)

        schedule.append({
            "task": task.get("name"),
            "start": current,
            "end": current + duration
        })

        current += duration

    return schedule