from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Todo


class Command(BaseCommand):
    help = "Checks if Todo deadlines are met"

    def add_arguments(self, parser):
        parser.add_argument(
            "--notify", action="store_true", help="Notify user if deadline is met"
        )

    def handle(self, *args, **options):
        todos = Todo.objects.filter(
            deadline__lte=timezone.now(), completed=False
        ).prefetch_related("user")

        if not todos:
            print("No todos have deadlines that are not met")
            return

        for todo in todos:
            if options.get("notify"):
                print(
                    f"Notifying user: {todo.user} at {todo.user.email}. Deadline is met for todo: '{todo}'"
                )
                send_mail(
                    subject=f"Deadline met for '{todo}'. Please take action.",
                    message=f"Deadline met for '{todo}' on {todo.deadline.strftime('%Y-%m-%d')}. Please take action.",
                    from_email="noreply@django-todos.com",
                    recipient_list=[todo.user.email],
                    fail_silently=False,
                )
            else:
                print(
                    f"Debug: Deadline for '{todo}' is met. Will not notify {todo.user}"
                )
