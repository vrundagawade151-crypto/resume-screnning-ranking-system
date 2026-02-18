def calculate_score(resume_text, job_skills):

    score = 0

    skills = job_skills.lower().split(",")

    for skill in skills:

        if skill.strip() in resume_text:
            score += 10

    return score
