python manage.py populate_demofrom django.core.management.base import BaseCommand
from django.utils.text import slugify
from accessories.models import Category, Product, ProductImage
from PIL import Image
import random
import os

class Command(BaseCommand):
    help = 'Populate demo products for accessories'

    def handle(self, *args, **options):
        # Create categories if not exist
        categories_data = [
            'Mouse',
            'Keyboard',
            'Headphones',
            'Speakers',
            'Webcam',
            'Microphone',
            'Cables',
            'Chargers',
            'Cases',
            'Stands'
        ]
        
        categories = []
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'Created category: {cat_name}')
        
        # Sample product names per category
        products_data = {
            'Mouse': [
                'Wireless Optical Mouse',
                'Gaming Mouse RGB',
                'Ergonomic Mouse',
                'Bluetooth Mouse',
                'Vertical Mouse',
                'Travel Mouse',
                'Laser Mouse',
                'Silent Mouse'
            ],
            'Keyboard': [
                'Mechanical Keyboard',
                'Wireless Keyboard',
                'Gaming Keyboard RGB',
                'Compact Keyboard',
                'Ergonomic Keyboard',
                'Bluetooth Keyboard',
                'Backlit Keyboard',
                'Numeric Keypad'
            ],
            'Headphones': [
                'Wireless Headphones',
                'Over-Ear Headphones',
                'Gaming Headset',
                'Noise Cancelling Headphones',
                'Bluetooth Earbuds',
                'Studio Headphones',
                'Sports Headphones',
                'Kids Headphones'
            ],
            'Speakers': [
                'Bluetooth Speakers',
                'Computer Speakers',
                'Soundbar',
                'Portable Speakers',
                'Wireless Speakers',
                'Home Theater Speakers',
                'Gaming Speakers',
                'Smart Speakers'
            ],
            'Webcam': [
                'HD Webcam',
                '4K Webcam',
                'Wireless Webcam',
                'Streaming Webcam',
                'Conference Webcam',
                'Security Webcam',
                'Auto-Focus Webcam',
                'Wide Angle Webcam'
            ],
            'Microphone': [
                'USB Microphone',
                'Wireless Microphone',
                'Condenser Microphone',
                'Gaming Microphone',
                'Podcast Microphone',
                'Lavalier Microphone',
                'Studio Microphone',
                'Conference Microphone'
            ],
            'Cables': [
                'USB Cable',
                'HDMI Cable',
                'Ethernet Cable',
                'Audio Cable',
                'DisplayPort Cable',
                'VGA Cable',
                'Power Cable',
                'Charging Cable'
            ],
            'Chargers': [
                'Wall Charger',
                'Car Charger',
                'Wireless Charger',
                'Power Bank',
                'USB Hub',
                'Multi-Port Charger',
                'Fast Charger',
                'Solar Charger'
            ],
            'Cases': [
                'Laptop Case',
                'Phone Case',
                'Tablet Case',
                'Hard Drive Case',
                'Cable Organizer',
                'Screen Protector',
                'Keyboard Case',
                'Mouse Pad'
            ],
            'Stands': [
                'Laptop Stand',
                'Monitor Stand',
                'Phone Stand',
                'Tablet Stand',
                'Speaker Stand',
                'Cooling Stand',
                'Ergonomic Stand',
                'Wall Mount'
            ]
        }
        
        # Create a dummy image if not exists
        demo_image_path = 'products/accessories/demo.jpg'
        full_path = os.path.join('media', demo_image_path)
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create a simple 400x300 image
            img = Image.new('RGB', (400, 300), color=(200, 200, 200))
            img.save(full_path)
            self.stdout.write('Created demo image')
        
        # Create products
        created_count = 0
        for cat_name, product_names in products_data.items():
            category = Category.objects.get(name=cat_name)
            for name in product_names:
                # Create product
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'slug': slugify(name),
                        'description': f'High-quality {name.lower()} for all your computing needs.',
                        'price': round(random.uniform(10, 200), 2),
                        'stock': random.randint(5, 50),
                        'available': True
                    }
                )
                if created:
                    # Create image
                    ProductImage.objects.create(
                        product=product,
                        image=demo_image_path,
                        alt_text=f'Image of {name}'
                    )
                    created_count += 1
                    self.stdout.write(f'Created product: {name}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} demo products'))