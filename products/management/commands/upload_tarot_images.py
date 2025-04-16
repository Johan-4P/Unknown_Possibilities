import os
import requests
from difflib import get_close_matches
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from cloudinary.uploader import upload
from products.models import TarotCard, Product

class Command(BaseCommand):
    help = 'Upload tarot card and product images from local folder to Cloudinary and update matching model objects.'

    def add_arguments(self, parser):
        parser.add_argument('--tarot-only', action='store_true', help='Only update tarot cards')
        parser.add_argument('--products-only', action='store_true', help='Only update products')

    def handle(self, *args, **options):
        folder_path = os.path.join(settings.BASE_DIR, 'local_tarot_cards')

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder not found: {folder_path}"))
            return

        tarot_names = {card.name.lower(): card for card in TarotCard.objects.all()}
        product_names = {product.name.lower(): product for product in Product.objects.all()}

        updated = []
        skipped = []

        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.png'):
                continue

            name_only = filename.replace('.png', '').replace('-', ' ').replace('_', ' ').lower()
            file_path = os.path.join(folder_path, filename)

            if options['products_only']:
                tarot_match = []
            else:
                tarot_match = get_close_matches(name_only, tarot_names.keys(), n=1, cutoff=0.6)

            if tarot_match:
                card = tarot_names[tarot_match[0]]
                with open(file_path, 'rb') as f:
                    result = upload(f, folder='tarot_cards/')
                    image_url = result['secure_url']
                    card.image = result['secure_url']
                    card.save()

                    self.stdout.write(self.style.SUCCESS(f"🔮 Updated TarotCard {card.name} with image: {filename}"))
                    updated.append(f"TarotCard: {card.name} <- {filename}")
                continue

            if options['tarot_only']:
                product_match = []
            else:
                product_match = get_close_matches(name_only, product_names.keys(), n=1, cutoff=0.6)

            if product_match:
                product = product_names[product_match[0]]
                with open(file_path, 'rb') as f:
                    result = upload(f, folder='products/')
                    image_url = result['secure_url']
                    image_content = ContentFile(requests.get(image_url).content)
                    product.image.save(filename, image_content, save=True)
                    self.stdout.write(self.style.SUCCESS(f"🛍️ Updated Product {product.name} with image: {filename}"))
                    updated.append(f"Product: {product.name} <- {filename}")
                continue

            self.stdout.write(self.style.WARNING(f"❌ No match found for: {filename}"))
            skipped.append(filename)

        # Log to file
        log_path = os.path.join(settings.BASE_DIR, 'upload_log.txt')
        with open(log_path, 'w') as log_file:
            log_file.write("=== Updated Items ===\n")
            for item in updated:
                log_file.write(f"{item}\n")
            log_file.write("\n=== Skipped (No Match) ===\n")
            for item in skipped:
                log_file.write(f"{item}\n")

        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n✅ Upload complete. {len(updated)} updated, {len(skipped)} skipped."))
        self.stdout.write(self.style.SUCCESS(f"📄 Log saved to: upload_log.txt"))
