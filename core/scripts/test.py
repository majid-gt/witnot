# Run this in Django shell: python manage.py shell

from core.models import Question

# Starting index of URLs (51.png) and ending (100.png)
start = 51
end = 100

# Fetch all questions ordered by ID (or some field)
questions = Question.objects.all().order_by('id')

# Make sure we have 50 questions to update
if len(questions) != (end - start + 1):
    print(f"Warning: Expected {end - start + 1} questions, found {len(questions)}")

# Assign URLs
for i, question in enumerate(questions, start=start):
    url = f"https://ik.imagekit.io/enokimkfy/pics/{i}.png"
    question.image = url  # if using ImageField, this will work if you store URL as file name
    question.save()
    print(f"Updated Question {question.id} → {url}")
