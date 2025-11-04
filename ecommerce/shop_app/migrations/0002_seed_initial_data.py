from django.db import migrations


def seed_forward(apps, schema_editor):
    Category = apps.get_model('shop_app', 'Category')
    Product = apps.get_model('shop_app', 'Product')

    # Create categories
    categories_data = [
        {"category_name": "Гар утас", "slug": "gar-utas", "description": "Ухаалаг гар утас болон дагалдах хэрэгсэл"},
        {"category_name": "Зөөврийн компьютер", "slug": "zoovorh-kompyuter", "description": "Ноутбук болон компьютерийн хэрэгсэл"},
        {"category_name": "Гоо сайхан", "slug": "goo-saikhan", "description": "Арьс арчилгаа, гоо сайхны бүтээгдэхүүн"},
        {"category_name": "Гэр ахуй", "slug": "ger-akhui", "description": "Гэрийн хэрэглээний цахилгаан болон хэрэгсэл"},
        {"category_name": "Хувцас", "slug": "khuvtsas", "description": "Эрэгтэй, эмэгтэй, спорт хувцас"},
    ]

    slug_to_category = {}
    for c in categories_data:
        obj, _ = Category.objects.get_or_create(slug=c["slug"], defaults=c)
        slug_to_category[c["slug"]] = obj

    # Helper to pick an existing image path from media
    # Use product images that exist in the repository
    image_paths = [
        'photos/products/Latte.png',
        'photos/products/Espresso.png',
        'photos/products/Caramel_Macchiato.png',
        'photos/products/Cappuccino.jpg',
        'photos/products/Latte_odRk5QG.png',
        'photos/products/Espresso_BEiSU2h.png',
        'photos/products/Cappuccino_Qv3Ye06.jpg',
        'photos/products/Caramel_Macchiato_ACyPHK0.png',
    ]

    def img(i):
        return image_paths[i % len(image_paths)]

    products_data = [
        {"product_name": "iPhone 15 Pro", "slug": "iphone-15-pro", "price": 5200000, "stock": 12, "category_slug": "gar-utas", "description": "Apple-ийн хамгийн сүүлийн үеийн ухаалаг утас"},
        {"product_name": "Samsung Galaxy S24", "slug": "samsung-galaxy-s24", "price": 4850000, "stock": 8, "category_slug": "gar-utas", "description": "Өндөр хүчин чадал, AI камертай Android утас"},
        {"product_name": "MacBook Air M2", "slug": "macbook-air-m2", "price": 6800000, "stock": 5, "category_slug": "zoovorh-kompyuter", "description": "M2 чиптэй, хөнгөн загварын Apple ноутбук"},
        {"product_name": "Lenovo IdeaPad 3", "slug": "lenovo-ideapad-3", "price": 2300000, "stock": 10, "category_slug": "zoovorh-kompyuter", "description": "Суралцагчдад зориулсан дунд түвшний ноутбук"},
        {"product_name": "L'Oréal Face Cream", "slug": "loreal-face-cream", "price": 78000, "stock": 25, "category_slug": "goo-saikhan", "description": "Арьс чийгшүүлэх тос, бүх төрлийн арьсанд"},
        {"product_name": "Maybelline Mascara", "slug": "maybelline-mascara", "price": 42000, "stock": 30, "category_slug": "goo-saikhan", "description": "Сормуусыг өтгөрүүлж уртасгагч mascara"},
        {"product_name": "Dyson V12 Vacuum", "slug": "dyson-v12-vacuum", "price": 2950000, "stock": 4, "category_slug": "ger-akhui", "description": "Ухаалаг тоос сорогч, утасгүй хэрэглээтэй"},
        {"product_name": "Philips Airfryer XXL", "slug": "philips-airfryer-xxl", "price": 680000, "stock": 9, "category_slug": "ger-akhui", "description": "Тосгүй хоол шарагч, эрүүл хооллолтод"},
        {"product_name": "Adidas Running Shoes", "slug": "adidas-running-shoes", "price": 320000, "stock": 18, "category_slug": "khuvtsas", "description": "Эрэгтэй хөнгөн гүйлтийн пүүз"},
        {"product_name": "Nike Hoodie", "slug": "nike-hoodie", "price": 210000, "stock": 15, "category_slug": "khuvtsas", "description": "Эмэгтэй спорт загварын дулаан цамц"},
        {"product_name": "Smart Watch Huawei GT4", "slug": "smart-watch-huawei-gt4", "price": 980000, "stock": 11, "category_slug": "gar-utas", "description": "Зүрхний цохилт, дасгалын хяналт бүхий ухаалаг цаг"},
    ]

    for i, p in enumerate(products_data):
        category = slug_to_category[p["category_slug"]]
        Product.objects.get_or_create(
            slug=p["slug"],
            defaults={
                "product_name": p["product_name"],
                "description": p["description"],
                "price": p["price"],
                "images": img(i),
                "stock": p["stock"],
                "is_available": True,
                "category": category,
            },
        )


def seed_reverse(apps, schema_editor):
    Category = apps.get_model('shop_app', 'Category')
    Product = apps.get_model('shop_app', 'Product')

    product_slugs = [
        "iphone-15-pro",
        "samsung-galaxy-s24",
        "macbook-air-m2",
        "lenovo-ideapad-3",
        "loreal-face-cream",
        "maybelline-mascara",
        "dyson-v12-vacuum",
        "philips-airfryer-xxl",
        "adidas-running-shoes",
        "nike-hoodie",
        "smart-watch-huawei-gt4",
    ]
    Product.objects.filter(slug__in=product_slugs).delete()

    category_slugs = [
        "gar-utas",
        "zoovorh-kompyuter",
        "goo-saikhan",
        "ger-akhui",
        "khuvtsas",
    ]
    Category.objects.filter(slug__in=category_slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('shop_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]







