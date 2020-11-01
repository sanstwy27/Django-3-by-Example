import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.management import BaseCommand
from django.db.models import Count

from sanstwy27_educa import settings


class Command(BaseCommand):
    help = 'Sends an e-mail reminder to users registered more than N days that are not enrolled into any courses yet'

    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a course'
        date_joined = datetime.date.today() - datetime.timedelta(days=options['days'])
        users = User.objects.annotate(course_count=Count('courses_joined')).filter(course_count=0,
                                                                                   date_joined__lte=date_joined)
        for user in users:
            message = "Dear {},\n\n We noticed that you didn't enroll in any courses yet. What are you waiting for?".format(
                user.first_name)
            emails.append((subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]))
        send_mass_mail(emails)
        self.stdout.write('Sent {} reminders'.format(len(emails)))