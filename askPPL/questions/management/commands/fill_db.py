from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike, QuestionTag
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Наполняю базу тестовыми данными. ratio = [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']

        users = []
        for i in range(ratio):
            u = User(username=fake.user_name() + str(i), email=fake.email())
            u.set_password('testpass123')
            users.append(u)
        users = User.objects.bulk_create(users, batch_size=1000)

        profiles = Profile.objects.bulk_create(
            [Profile(user=u) for u in users], batch_size=1000
        )

        tags = Tag.objects.bulk_create(
            [Tag(name=fake.word()) for i in range(ratio)], batch_size=1000
        )

        questions = Question.objects.bulk_create(
            [
                Question(
                    name=fake.sentence(nb_words=6),
                    text=fake.paragraph(nb_sentences=3),
                    author=random.choice(profiles)
                )
                for i in range(ratio * 10)
            ],
            batch_size=1000
        )

        question_tags = []
        for question in questions:
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(tags, min(num_tags, len(tags)))
            for tag in selected_tags:
                question_tags.append(QuestionTag(question=question, tag=tag))
        QuestionTag.objects.bulk_create(question_tags, batch_size=1000)

        answers = Answer.objects.bulk_create(
            [
                Answer(
                    question=random.choice(questions),
                    text=fake.paragraph(nb_sentences=2),
                    author=random.choice(profiles),
                    isRight=random.random() < 0.1
                )
                for i in range(ratio * 100)
            ],
            batch_size=1000
        )

        seen_q, qlikes = set(), []
        for i in range(ratio * 100):
            q, p = random.choice(questions), random.choice(profiles)
            if (q.id, p.id) not in seen_q:
                seen_q.add((q.id, p.id))
                qlikes.append(QuestionLike(question=q, author=p))
        QuestionLike.objects.bulk_create(qlikes, batch_size=1000)

        seen_a, alikes = set(), []
        for i in range(ratio * 100):
            a, p = random.choice(answers), random.choice(profiles)
            if (a.id, p.id) not in seen_a:
                seen_a.add((a.id, p.id))
                alikes.append(AnswerLike(answer=a, author=p))
        AnswerLike.objects.bulk_create(alikes, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: юзеров={ratio}, тегов={ratio}, вопросов={ratio*10}, '
            f'ответов={ratio*100}, связей_тегов={len(question_tags)}, '
            f'лайков={len(qlikes)+len(alikes)}'
        ))