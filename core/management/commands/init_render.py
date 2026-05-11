import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, call_command

from core.models import Booking, GCashAccount, Room, User


class Command(BaseCommand):
    help = "Initialize production database and seed media for Render deployments."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Reload the initial fixture even if data already exists.",
        )

    def handle(self, *args, **options):
        self.copy_seed_media()

        has_data = any(
            model.objects.exists()
            for model in (User, Room, GCashAccount, Booking)
        )
        if has_data and not options["force"]:
            self.stdout.write(self.style.SUCCESS("Database already initialized."))
            return

        call_command("loaddata", "initial_data", verbosity=options["verbosity"])
        self.stdout.write(self.style.SUCCESS("Database initialized from fixture."))

    def copy_seed_media(self):
        seed_root = Path(settings.BASE_DIR) / "core" / "seed_media"
        media_root = Path(settings.MEDIA_ROOT)
        if not seed_root.exists():
            return

        for source in seed_root.rglob("*"):
            if source.is_dir():
                continue

            target = media_root / source.relative_to(seed_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or source.stat().st_size != target.stat().st_size:
                shutil.copy2(source, target)
