from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from quizzes.models import HairProfile
from shop.models import Category, SuitabilityTag, Product, HaircutGuide
from recommendations.models import CurlCareRule
from orders.models import Order, OrderItem, PaymentTransaction
from recommendations.engine import generate_hair_diagnosis

class Command(BaseCommand):
    help = "Seeds initial demonstration data for CURLIQUE Nepal"

    def handle(self, *args, **options):
        self.stdout.write("Starting CURLIQUE database seeding...")

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@curlique.com.np',
                'first_name': 'CURLIQUE',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin1234!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Superuser: admin / Admin1234!"))
        else:
            admin_user.set_password('Admin1234!')
            admin_user.save()

        # 2. Regular Demo User (Aarav Shrestha - 3B High Porosity)
        test_user, created = User.objects.get_or_create(
            username='aarav',
            defaults={
                'email': 'aarav@example.com',
                'first_name': 'Aarav',
                'last_name': 'Shrestha',
            }
        )
        if created:
            test_user.set_password('CurlyPass123!')
            test_user.save()
            self.stdout.write(self.style.SUCCESS("Created Demo User: aarav / CurlyPass123!"))

        profile, _ = UserProfile.objects.get_or_create(user=test_user)
        profile.phone_number = '9841234567'
        profile.city = 'Lalitpur'
        profile.district = 'Lalitpur'
        profile.address_line = 'Jhamsikhel Road, Ward 3'
        profile.bio = "Embracing my natural 3B springy ringlets after years of straight blowouts!"
        profile.save()

        # Demo Hair Profile for Aarav
        hair_prof, _ = HairProfile.objects.get_or_create(
            user=test_user,
            defaults={
                'curl_type': '3B',
                'porosity': 'high',
                'density': 'medium',
                'scalp_type': 'normal',
                'concerns': 'frizz,dryness',
                'budget': 'mid',
            }
        )
        diag = generate_hair_diagnosis(hair_prof)
        hair_prof.diagnosis_title = diag['diagnosis_title']
        hair_prof.diagnosis_summary = diag['mp_balance']['headline']
        hair_prof.save()

        # 3. Product Categories
        categories_data = [
            ('Cleansers & Shampoos', 'cleansers-shampoos', 'Sulfate-free low-poo, clarifying, and co-wash cleansers.', 'bi-droplet-half'),
            ('Conditioners & Deep Masks', 'conditioners-deep-masks', 'Nourishing rinse-out conditioners and intense protein-moisture hair masques.', 'bi-flower1'),
            ('Leave-In & Creams', 'leave-in-creams', 'Foundation moisture creams, curl milks, and leave-in conditioners.', 'bi-moisture'),
            ('Styling Gels & Custards', 'styling-gels-custards', 'Cast-forming styling gels, flaxseed gels, and definition custards.', 'bi-stars'),
            ('Scalp Oils & Serums', 'scalp-oils-serums', 'Lightweight plant oils to seal moisture and stimulate scalp circulation.', 'bi-capsule'),
            ('Accessories & Tools', 'accessories-tools', 'Satin bonnets, microfiber towels, wide-tooth combs, and diffusers.', 'bi-scissors'),
        ]
        cat_map = {}
        for name, slug, desc, icon in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc, 'icon_name': icon})
            cat_map[slug] = cat

        # 4. Suitability Tags
        tags_data = [
            ('CG-Friendly', 'cg-friendly', '100% Curly Girl Method compliant with zero sulfates, silicones, or drying alcohols.', 'success'),
            ('Sulfate-Free', 'sulfate-free', 'Free from harsh sodium lauryl sulfates (SLS/SLES) to protect natural scalp sebum.', 'success'),
            ('Silicone-Free', 'silicone-free', 'Zero non-soluble dimethicones, preventing waterproof barrier buildup.', 'info'),
            ('Protein-Rich', 'protein-rich', 'Contains hydrolyzed keratin, wheat, or silk proteins to reinforce cuticles.', 'warning'),
            ('Moisture-Rich', 'moisture-rich', 'Formulated with deep humectants and emollients to banish dry frizz.', 'primary'),
            ('Lightweight', 'lightweight', 'Weightless formulation ideal for fine strands and low-porosity hair.', 'info'),
            ('Heavy-Butter', 'heavy-butter', 'Rich in dense shea or cocoa butters for coarse curls and coily textures.', 'secondary'),
            ('Alcohol-Free', 'alcohol-free', 'Contains zero short-chain drying alcohols like isopropyl alcohol.', 'success'),
            ('Tea-Tree', 'tea-tree', 'Infused with purifying tea tree oil to calm dandruff and oily buildup.', 'success'),
            ('Aloe-Based', 'aloe-based', 'Pure aloe vera leaf juice foundation for soothing hydration.', 'success'),
        ]
        tag_map = {}
        for name, slug, desc, color in tags_data:
            t, _ = SuitabilityTag.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc, 'badge_color': color})
            tag_map[slug] = t

        # 5. Products Seed Data (Real CGM products available in Nepal with NPR prices)
        products_data = [
            {
                'name': 'Cleansing Cream Shampoo (Sulfate-Free)',
                'brand': 'Cantu Shea Butter',
                'category': 'cleansers-shampoos',
                'price': Decimal('1250.00'),
                'stock': 30,
                'is_featured': True,
                'size': '400ml',
                'short_description': 'Rich lathering sulfate-free shampoo formulated with pure Shea Butter to gently cleanse and moisturize.',
                'description': 'Award-winning sulfate-free formula cleanses and moisturizes helping to reduce breakage during shampooing. Made with pure shea butter and formulated without harsh ingredients, Cantu restores your real, authentic curl beauty.',
                'ingredients_list': 'Water (Aqua), Sodium C14-16 Olefin Sulfonate, Cocamidopropyl Betaine, Cocamide MEA, Glycol Distearate, Polysorbate 20, Steareth-4, Butyrospermum Parkii (Shea) Butter, Glycerin, Phenoxyethanol, Fragrance (Parfum).',
                'key_actives': 'Pure Shea Butter, Gentle Surfactants',
                'suitable_curl_types': '2B,2C,3A,3B,3C,4A,4B',
                'suitable_porosity': 'medium,high',
                'tags': ['cg-friendly', 'sulfate-free', 'silicone-free', 'moisture-rich'],
            },
            {
                'name': 'Jamaican Black Castor Oil Strengthen & Restore Shampoo',
                'brand': 'Shea Moisture',
                'category': 'cleansers-shampoos',
                'price': Decimal('2650.00'),
                'stock': 20,
                'is_featured': True,
                'size': '384ml',
                'short_description': 'Clarifying and strengthening shampoo with Apple Cider Vinegar and Peppermint to rebuild damaged cuticles.',
                'description': 'This sulfate-free clarifying shampoo removes product buildup while infusing hair with nourishing moisture. Ideal for those who regularly color, straighten, perm or heat style their hair, as well as kinky, curly or wavy natural styles.',
                'ingredients_list': 'Water, Decyl Glucoside, Sodium Lauroyl Lactylate, Fragrance, Glycerin, Hydrolyzed Wheat Protein, Ricinus Communis (Castor) Seed Oil, Apple Cider Vinegar, Mentha Piperita (Peppermint) Leaf Extract, Butyrospermum Parkii (Shea) Butter.',
                'key_actives': 'Jamaican Black Castor Oil, Apple Cider Vinegar, Peppermint, Hydrolyzed Wheat Protein',
                'suitable_curl_types': '3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'high,medium',
                'tags': ['cg-friendly', 'sulfate-free', 'silicone-free', 'protein-rich'],
            },
            {
                'name': 'Hydrating Gentle Low-Poo Shampoo',
                'brand': 'Ashba Botanicals',
                'category': 'cleansers-shampoos',
                'price': Decimal('1650.00'),
                'stock': 25,
                'is_featured': False,
                'size': '250ml',
                'short_description': 'Lightweight botanical cleanser designed specifically for South Asian wavy and fine curl textures.',
                'description': 'Mild, moisturizing shampoo that creates a gentle lather to cleanse the scalp without stripping. Packed with Chamomile Flower Extract and Rosemary, it promotes scalp micro-circulation and leaves curls light and bouncy.',
                'ingredients_list': 'Aqua, Cocamidopropyl Betaine, Sodium Cocoyl Isethionate, Glycerin, Chamomilla Recutita Flower Extract, Rosmarinus Officinalis Leaf Extract, Panthenol, Polyquaternium-10, Phenoxyethanol, Ethylhexylglycerin.',
                'key_actives': 'Chamomile Flower, Rosemary Extract, Panthenol (Pro-Vitamin B5)',
                'suitable_curl_types': '2A,2B,2C,3A,3B',
                'suitable_porosity': 'low,medium',
                'tags': ['cg-friendly', 'sulfate-free', 'silicone-free', 'lightweight', 'aloe-based'],
            },
            {
                'name': 'Botanique Nourish & Replenish Coconut Conditioner',
                'brand': 'Tresemme Botanique',
                'category': 'conditioners-deep-masks',
                'price': Decimal('850.00'),
                'stock': 40,
                'is_featured': False,
                'size': '650ml',
                'short_description': 'Budget-friendly holy-grail CGM conditioner infused with Coconut Milk and Aloe Vera.',
                'description': 'An affordable staple across Nepal for curly hair. Free of silicones and parabens, it provides immense slip for painless detangling in the shower and works wonderfully as a co-wash or rinse-out conditioner.',
                'ingredients_list': 'Water, Cetearyl Alcohol, Stearamidopropyl Dimethylamine, Behentrimonium Chloride, Cocos Nucifera (Coconut) Oil, Aloe Barbadensis Leaf Juice, Fragrance, Dipropylene Glycol, Lactic Acid, Potassium Chloride.',
                'key_actives': 'Coconut Oil, Aloe Vera Leaf Extract, Lactic Acid',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly', 'silicone-free', 'moisture-rich', 'aloe-based'],
            },
            {
                'name': 'Raw Shea Butter Deep Treatment Masque',
                'brand': 'Shea Moisture',
                'category': 'conditioners-deep-masks',
                'price': Decimal('2850.00'),
                'stock': 18,
                'is_featured': True,
                'size': '340g',
                'short_description': 'Intensive restoring mask with Sea Kelp and Argan Oil to deeply moisturize dry, over-processed curls.',
                'description': 'Our intensive treatment masque deeply moisturizes and conditions dry, damaged hair. Perfect for transitioning chemically treated hair to natural curls. Formulated with raw shea butter, sea kelp and argan oil to restore natural lipids.',
                'ingredients_list': 'Water, Butyrospermum Parkii (Shea) Butter, Ricinus Communis (Castor) Seed Oil, Glycerin, Cetearyl Alcohol, Glyceryl Stearate, Behentrimonium Chloride, Argania Spinosa Kernel Oil, Macrocystis Pyrifera (Kelp) Extract, Panthenol.',
                'key_actives': 'Raw Organic Shea Butter, Argan Oil, Sea Kelp',
                'suitable_curl_types': '3B,3C,4A,4B,4C',
                'suitable_porosity': 'high',
                'tags': ['cg-friendly', 'silicone-free', 'moisture-rich', 'heavy-butter'],
            },
            {
                'name': 'Hydrating Cream Conditioner',
                'brand': 'Cantu Shea Butter',
                'category': 'conditioners-deep-masks',
                'price': Decimal('1350.00'),
                'stock': 35,
                'is_featured': False,
                'size': '400ml',
                'short_description': 'Nourishes dry, brittle hair with pure shea butter and essential oils for maximum slip.',
                'description': 'Helps hair retain natural oils for fewer split ends. Made with pure shea butter to replace vital moisture, revealing stronger, healthier hair with a natural shine. Makes wide-tooth comb detangling effortless.',
                'ingredients_list': 'Water (Aqua), Cetyl Alcohol, Stearyl Alcohol, Stearamidopropyl Dimethylamine, Glycerin, Glyceryl Stearate, Butyrospermum Parkii (Shea) Butter, Dimethicone (Water Soluble), Fragrance, Citric Acid.',
                'key_actives': 'Shea Butter, Glycerin, Stearyl Alcohol',
                'suitable_curl_types': '2C,3A,3B,3C,4A,4B',
                'suitable_porosity': 'medium,high',
                'tags': ['cg-friendly', 'sulfate-free', 'moisture-rich'],
            },
            {
                'name': 'Moisturizing Curl Activator Cream',
                'brand': 'Cantu Shea Butter',
                'category': 'leave-in-creams',
                'price': Decimal('1450.00'),
                'stock': 30,
                'is_featured': True,
                'size': '355ml',
                'short_description': 'Cult-favorite leave-in cream that activates curl bounce and provides frizz-free definition.',
                'description': 'Activates curls, delivers volume, and adds shine. Delivers a soft, bouncy finish without crunch. Rake through soaking wet hair in sections for clumped, hydrated curls that resist Nepal monsoon humidity.',
                'ingredients_list': 'Water (Aqua), Glycerin, Propanediol, Butyrospermum Parkii (Shea) Butter, Cetearyl Alcohol, Stearyl Alcohol, Ceteareth-20, Canola Oil, Polyquaternium-10, Olea Europaea (Olive) Fruit Oil, Cocos Nucifera (Coconut) Oil.',
                'key_actives': 'Pure Shea Butter, Olive Fruit Oil, Coconut Oil',
                'suitable_curl_types': '3A,3B,3C,4A,4B',
                'suitable_porosity': 'high,medium',
                'tags': ['cg-friendly', 'sulfate-free', 'silicone-free', 'moisture-rich', 'heavy-butter'],
            },
            {
                'name': 'Right Ringlets Leave-In Conditioner',
                'brand': 'Ashba Botanicals',
                'category': 'leave-in-creams',
                'price': Decimal('1750.00'),
                'stock': 22,
                'is_featured': False,
                'size': '200ml',
                'short_description': 'Featherlight leave-in lotion infused with Baobab Oil and Quinoa Protein.',
                'description': 'Formulated specifically for fine to medium wavy and curly textures that cannot tolerate heavy butters. Baobab oil softens curls while Hydrolyzed Quinoa strengthens strands without weighing down your crown.',
                'ingredients_list': 'Aqua, Cetearyl Alcohol, Adansonia Digitata (Baobab) Seed Oil, Hydrolyzed Quinoa Protein, Linum Usitatissimum (Flaxseed) Extract, Panthenol, Behentrimonium Methosulfate, Phenoxyethanol, Fragrance.',
                'key_actives': 'Baobab Seed Oil, Hydrolyzed Quinoa, Flaxseed Extract',
                'suitable_curl_types': '2A,2B,2C,3A,3B',
                'suitable_porosity': 'low,medium',
                'tags': ['cg-friendly', 'lightweight', 'silicone-free', 'protein-rich', 'aloe-based'],
            },
            {
                'name': 'Ultra Defining Hair Gel (Strong Hold)',
                'brand': 'Curl Up',
                'category': 'styling-gels-custards',
                'price': Decimal('1550.00'),
                'stock': 28,
                'is_featured': True,
                'size': '200ml',
                'short_description': 'Forms a protective gel cast around curl clumps, blocking out humidity and holding ringlets for days.',
                'description': 'Alcohol-free defining gel enriched with Flaxseed and Chia Seed extracts. Forms an authentic CGM gel cast that locks in hydration. Once 100% dry, scrunch out the crunch (SOTC) for pillow-soft, touchable curls.',
                'ingredients_list': 'Aqua, Linum Usitatissimum (Flaxseed) Seed Extract, Salvia Hispanica (Chia) Seed Extract, Glycerin, Carbomer, Polysorbate 20, Panthenol, Triethanolamine, Phenoxyethanol, Ethylhexylglycerin.',
                'key_actives': 'Flaxseed Mucilage, Chia Seed Extract, Panthenol',
                'suitable_curl_types': '2B,2C,3A,3B,3C,4A',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly', 'alcohol-free', 'silicone-free', 'lightweight'],
            },
            {
                'name': 'Olive Oil Maximum Hold Styling Gel',
                'brand': 'Eco Styler',
                'category': 'styling-gels-custards',
                'price': Decimal('950.00'),
                'stock': 50,
                'is_featured': False,
                'size': '473ml',
                'short_description': 'High-value styling gel with 100% pure olive oil for weightless maximum hold and shine.',
                'description': 'Eco Style Olive Oil gel helps your scalp naturally regulate its own moisturizing system. Attracts moisture to the scalp and holds it in, while taming edges and controlling humidity frizz during Nepal wet months.',
                'ingredients_list': 'Water (Aqua), Carbomer, Hydrolyzed Wheat Protein, Glycerin, Amino-2-Methyl-1-Propanol, Sodium Hydroxymethylglycinate, Polysorbate 20, Tetrasodium EDTA, Olive Oil, Fragrance.',
                'key_actives': '100% Pure Olive Oil, Hydrolyzed Wheat Protein',
                'suitable_curl_types': '3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'medium,high',
                'tags': ['alcohol-free', 'protein-rich', 'moisture-rich'],
            },
            {
                'name': 'Virgin Olive Scalp & Strand Hair Oil',
                'brand': 'Dabur Vatika',
                'category': 'scalp-oils-serums',
                'price': Decimal('650.00'),
                'stock': 40,
                'is_featured': False,
                'size': '200ml',
                'short_description': 'Affordable cold-pressed olive oil infused with Lemon and Almond for scalp nourishment and SOTC.',
                'description': 'Readily available across grocery stores and pharmacies in Nepal. Exceptional for pre-poo oil treatments or using 2 drops to "Scrunch Out The Crunch" (SOTC) on dry gel casts.',
                'ingredients_list': 'Olea Europaea (Olive) Fruit Oil, Prunus Amygdalus Dulcis (Sweet Almond) Oil, Citrus Limon (Lemon) Peel Oil, Tocopheryl Acetate (Vitamin E), Mineral-Free Herbal Base.',
                'key_actives': 'Cold-Pressed Olive Oil, Sweet Almond Oil, Vitamin E',
                'suitable_curl_types': '2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'high,medium',
                'tags': ['silicone-free', 'moisture-rich'],
            },
            {
                'name': '100% Organic Cold-Pressed Moroccan Argan Oil',
                'brand': 'The Ordinary',
                'category': 'scalp-oils-serums',
                'price': Decimal('1950.00'),
                'stock': 15,
                'is_featured': True,
                'size': '30ml',
                'short_description': 'Ultra-pure lightweight finishing oil that seals porous cuticles and imparts brilliant shine.',
                'description': 'This formulation uses 100% pure Moroccan Argan Seed Oil extracted through a cold pressing process that preserves fatty acids, vitamins, phenols, and carotenes. Excellent for high-porosity curl sealing.',
                'ingredients_list': '100% Argania Spinosa Kernel Oil.',
                'key_actives': '100% Pure Organic Cold-Pressed Argan Oil',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly', 'lightweight', 'silicone-free', 'moisture-rich'],
            },
            {
                'name': 'Mulberry Silk Satin Sleep Bonnet (Dual Layer)',
                'brand': 'CURLIQUE Essentials',
                'category': 'accessories-tools',
                'price': Decimal('1100.00'),
                'stock': 50,
                'is_featured': True,
                'size': 'Adjustable Band',
                'short_description': 'Double-lined premium satin bonnet to prevent overnight friction frizz and moisture loss.',
                'description': 'Designed specifically for Nepal winters and dry bedrooms. Sleeping on cotton siphons away moisture and causes tangled friction breakage. This dual-layered satin bonnet preserves your curl clumps for 3-4 days between washes.',
                'ingredients_list': 'High-Grade Breathable Satin with Soft Elastic Comfort Band.',
                'key_actives': 'Friction-Free Satin Weave',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly'],
            },
            {
                'name': 'Collapsible Universal Curly Diffuser Attachment',
                'brand': 'CURLIQUE Essentials',
                'category': 'accessories-tools',
                'price': Decimal('1350.00'),
                'stock': 25,
                'is_featured': False,
                'size': 'Fits 1.6-2.0 Inch Dryers',
                'short_description': 'Even heat distribution diffuser that cups curls gently without disturbing clumping.',
                'description': 'Collapsible silicone design makes it travel-friendly. Deep bowl accommodates dense curls, while 3D prongs lift roots to enhance volume while minimizing heat exposure.',
                'ingredients_list': 'Heat-Resistant Food-Grade Silicone.',
                'key_actives': '3D Airflow Dispersion',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly'],
            },
            {
                'name': 'Tea Tree & Rosemary Scalp Clarifying Treatment',
                'brand': 'CURLIQUE Organics',
                'category': 'scalp-oils-serums',
                'price': Decimal('950.00'),
                'stock': 30,
                'is_featured': False,
                'size': '100ml',
                'short_description': 'Soothes itchy scalp, removes hard-water deposits common in Kathmandu, and stimulates roots.',
                'description': 'Formulated with organic Australian tea tree and Himalayan rosemary. Cleanses microbial scalp buildup and balances excessive sebum for oily or flake-prone curl wearers.',
                'ingredients_list': 'Simmondsia Chinensis (Jojoba) Oil, Melaleuca Alternifolia (Tea Tree) Leaf Oil, Rosmarinus Officinalis (Rosemary) Leaf Oil, Tocopherol (Vitamin E).',
                'key_actives': 'Tea Tree Oil, Rosemary Oil, Jojoba Oil',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'low,medium,high',
                'tags': ['tea-tree', 'cg-friendly', 'lightweight', 'silicone-free'],
            },
            {
                'name': 'Ultra-Absorbent Microfiber Hair Plop Towel',
                'brand': 'CURLIQUE Essentials',
                'category': 'accessories-tools',
                'price': Decimal('850.00'),
                'stock': 40,
                'is_featured': False,
                'size': '65cm x 25cm',
                'short_description': 'Replaces harsh terrycloth towels to cut drying time in half without roughing up cuticles.',
                'description': 'Standard bathroom towels have loop fibers that snag curls and cause instant frizz. Our gentle microfiber plop wrap absorbs excess water rapidly while keeping curl clumps intact.',
                'ingredients_list': '80% Polyester, 20% Polyamide Microfiber with Secure Button Fastener.',
                'key_actives': 'Zero-Friction Microfiber',
                'suitable_curl_types': '2A,2B,2C,3A,3B,3C,4A,4B,4C',
                'suitable_porosity': 'low,medium,high',
                'tags': ['cg-friendly'],
            },
        ]

        for p_data in products_data:
            cat = cat_map[p_data['category']]
            tags_to_add = [tag_map[tslug] for tslug in p_data.get('tags', []) if tslug in tag_map]
            
            prod, _ = Product.objects.get_or_create(
                name=p_data['name'],
                brand=p_data['brand'],
                defaults={
                    'category': cat,
                    'price': p_data['price'],
                    'stock': p_data['stock'],
                    'is_featured': p_data['is_featured'],
                    'size': p_data['size'],
                    'short_description': p_data['short_description'],
                    'description': p_data['description'],
                    'ingredients_list': p_data['ingredients_list'],
                    'key_actives': p_data['key_actives'],
                    'suitable_curl_types': p_data['suitable_curl_types'],
                    'suitable_porosity': p_data['suitable_porosity'],
                }
            )
            prod.suitability_tags.set(tags_to_add)

        # 6. Haircut Guides with Real Nepal Salon Scripts
        guides_data = [
            {
                'name': 'The DevaCut (Curl-by-Curl Dry Cut)',
                'slug': 'the-devacut-nepal',
                'suitable_curls': '3A, 3B, 3C, 4A, 4B',
                'face_shapes': 'Oval, Round, Heart, Square',
                'description': 'The golden standard of curly cutting. Hair is cut 100% completely dry in its natural curl state, curl clump by curl clump. This prevents the shock of extreme shrinkage that happens when curls are cut wet and stretched.',
                'nepal_salon_advice': (
                    "Exact instructions to tell your barber/stylist in Kathmandu:\n\n"
                    "1. 'Dai/Didi, please do NOT wash or wet my hair first. Cut my curls completely dry in their natural state.'\n"
                    "2. 'Please DO NOT use thinning scissors (kh खौरिने कैंची) under any circumstances! Thinning shears shred curl clumps and create permanent frizz.'\n"
                    "3. 'Cut each curl clump individually where the curl naturally bends.'\n"
                    "4. 'Keep in mind my curls shrink 3 to 4 inches when dry, so please cut less length than you normally would.'"
                ),
                'maintenance_guide': (
                    "Re-cut every 4 to 6 months. Maintain between salon visits by refreshing with water mist and leave-in cream. "
                    "Sleep in a satin bonnet to keep the shape intact."
                )
            },
            {
                'name': 'The Rezo Cut (Maximum Body & 360° Volume)',
                'slug': 'the-rezo-cut-nepal',
                'suitable_curls': '2C, 3A, 3B, 3C, 4A, 4C',
                'face_shapes': 'Oval, Diamond, Long/Oblong',
                'description': 'Created by master stylist Nubia Suarez, the Rezo cut creates circular balance and volume around the head while maintaining consistent length. It liberates curls from the root so they bounce freely.',
                'nepal_salon_advice': (
                    "Exact instructions for your Nepal stylist:\n\n"
                    "1. 'I want circular layering that adds volume at the crown without losing perimeter length.'\n"
                    "2. 'Create soft triangular interior sections to let my curls move in 360 degrees.'\n"
                    "3. 'Do NOT pull my hair flat with a comb while cutting — hold it loosely with minimal tension.'"
                ),
                'maintenance_guide': (
                    "Diffuse with your head tilted upside down for 5 minutes to lift roots. Apply a lightweight mousse at the crown."
                )
            },
            {
                'name': 'Layered Curly Bob (Triangle Hair Prevention)',
                'slug': 'layered-curly-bob-nepal',
                'suitable_curls': '2A, 2B, 2C, 3A, 3B',
                'face_shapes': 'Round, Heart, Oval',
                'description': 'The classic curly nightmare is the "Christmas Tree" or pyramid effect where hair is flat at the crown and puffy at the bottom. A properly layered curly bob distributes weight evenly and frames the jawline.',
                'nepal_salon_advice': (
                    "What to say at the salon:\n\n"
                    "1. 'Please cut graduated layers starting from cheekbone level down.'\n"
                    "2. 'The goal is to eliminate the bottom-heavy triangle shape.'\n"
                    "3. 'Keep the nape slightly shorter so the top curls drape smoothly over the shoulders.'"
                ),
                'maintenance_guide': (
                    "Scrunch an alcohol-free gel into wet lengths. Air dry or diffuse on low heat. Very easy low-maintenance daily wash-and-go."
                )
            },
            {
                'name': 'Curly Shag with Curtain Bangs',
                'slug': 'curly-shag-curtain-bangs-nepal',
                'suitable_curls': '2B, 2C, 3A, 3B',
                'face_shapes': 'Oval, Heart, Square',
                'description': 'A trendy, rock-and-roll 70s inspired silhouette that features lots of choppy crown layers and face-framing curly bangs. Adds incredible volume to fine or medium curls.',
                'nepal_salon_advice': (
                    "Instructions for your stylist:\n\n"
                    "1. 'Cut curtain bangs dry at bridge-of-nose level so when they bounce up, they hit right at eyebrow level.'\n"
                    "2. 'Incorporate lots of short layers on the crown for lived-in texture.'\n"
                    "3. 'Keep the perimeter wispy and textured, not blunt.'"
                ),
                'maintenance_guide': (
                    "Style the bangs first with a finger coil and a drop of leave-in milk. Let air dry completely before fluffing."
                )
            },
            {
                'name': 'Tapered Coily Cut',
                'slug': 'tapered-coily-cut-nepal',
                'suitable_curls': '3C, 4A, 4B, 4C',
                'face_shapes': 'Oval, Round, High Cheekbones',
                'description': 'Keeps length and definition at the top of the crown while neatly tapering the sides and nape. Highlight coils and facial symmetry with minimal morning styling.',
                'nepal_salon_advice': (
                    "What to tell your barber in Nepal:\n\n"
                    "1. 'Taper the sides and back with clippers or scissors, maintaining a soft gradient.'\n"
                    "2. 'Leave 3 to 4 inches of coily length on the top crown.'\n"
                    "3. 'Line up the edges crisply around the temples and neck.'"
                ),
                'maintenance_guide': (
                    "Perform LOC method (Leave-in, Oil, Cream) on the crown coils daily. Re-taper the sides every 3 to 4 weeks."
                )
            },
            {
                'name': 'Ouidad Carving & Slicing Cut',
                'slug': 'ouidad-carving-slicing-nepal',
                'suitable_curls': '3A, 3B, 3C, 4A',
                'face_shapes': 'Oval, Square, Round',
                'description': 'A wet cutting method designed specifically for dense curls. The stylist carefully "carves" small C-shaped interior sections to remove bulk so curls nestle into each other rather than fighting for space.',
                'nepal_salon_advice': (
                    "Instructions for the stylist:\n\n"
                    "1. 'Cut the structural outline wet with gentle tension.'\n"
                    "2. 'Carve out internal bulk from the interior of dense sections so curl clumps fit together like puzzle pieces.'\n"
                    "3. 'Again, no thinning razors or thinning shears — clean scissor snips only.'"
                ),
                'maintenance_guide': (
                    "Excellent for high-density hair that feels too heavy in hot Kathmandu summers. Wash with lightweight conditioner."
                )
            },
        ]

        for g_data in guides_data:
            HaircutGuide.objects.get_or_create(
                slug=g_data['slug'],
                defaults={
                    'name': g_data['name'],
                    'suitable_curls': g_data['suitable_curls'],
                    'face_shapes': g_data['face_shapes'],
                    'description': g_data['description'],
                    'nepal_salon_advice': g_data['nepal_salon_advice'],
                    'maintenance_guide': g_data['maintenance_guide'],
                }
            )

        # 7. Curl Care Rules (For Diagnosis Engine)
        rules_data = [
            ('porosity', 'low', 'Low Porosity Warmth & Hydration', 'Low porosity cuticles are sealed tightly. Use warm water to open cuticles and prioritize water-based humectants.', 'Avoid heavy butter buildup.', 'Lightweight leave-in only.', 'Aloe, Glycerin, Panthenol', 'Heavy Shea, Coconut Oil', 1),
            ('porosity', 'high', 'High Porosity Structural Patching', 'Raised cuticles absorb water quickly and lose it just as fast. Requires hydrolyzed protein to fill gaps.', 'Use moisturizing cream cleanse.', 'Layer LOC method with butter.', 'Hydrolyzed Keratin, Shea Butter', 'Harsh Sulfates, Alcohol', 1),
            ('curl_type', '3B', '3B Springy Ringlet Definition', 'Needs humidity barrier protection to stop atmospheric moisture from causing frizz.', 'Sulfate-free low-poo.', 'Botanical gel cast with SOTC.', 'Flaxseed, Argan Oil', 'Drying Alcohols', 2),
            ('scalp', 'oily', 'Scalp Detox & Sebum Regulation', 'Keep scalp clear of oil buildup so follicles breathe freely.', 'Gentle clarifying 2-3x weekly.', 'Keep heavy creams off roots.', 'Tea Tree, Rosemary, Peppermint', 'Heavy scalp waxes', 2),
            ('concern', 'frizz', 'Nepal Monsoon Frizz Control', 'Form a protective gel cast on wet hair to seal out humidity.', 'Condition with deep slip.', 'Scrunch out crunch with 2 drops oil.', 'Flaxseed Gel, Jojoba Oil', 'Dry brushing', 3),
        ]
        for r_type, r_key, title, summary, c_adv, s_adv, ing_rec, ing_av, pri in rules_data:
            CurlCareRule.objects.get_or_create(
                rule_type=r_type,
                rule_key=r_key,
                defaults={
                    'title': title,
                    'summary': summary,
                    'conditioning_advice': c_adv,
                    'styling_advice': s_adv,
                    'ingredients_recommended': ing_rec,
                    'ingredients_to_avoid': ing_av,
                    'priority': pri,
                }
            )

        # 8. Demo Orders for Demonstration & Admin Reports
        demo_order, ord_created = Order.objects.get_or_create(
            order_number='CURL-NP-DEMO01',
            defaults={
                'user': test_user,
                'full_name': 'Aarav Shrestha',
                'email': 'aarav@example.com',
                'phone': '9841234567',
                'delivery_address': 'Jhamsikhel Ward 3',
                'city': 'Lalitpur',
                'district': 'Lalitpur',
                'payment_method': 'ESEWA',
                'payment_status': 'PAID',
                'order_status': 'DELIVERED',
                'subtotal': Decimal('3800.00'),
                'delivery_fee': Decimal('100.00'),
                'total_amount': Decimal('3900.00'),
            }
        )
        if ord_created:
            p1 = Product.objects.filter(brand='Shea Moisture').first()
            p2 = Product.objects.filter(category__slug='accessories-tools').first()
            if p1:
                OrderItem.objects.create(order=demo_order, product=p1, product_name=p1.name, product_brand=p1.brand, price=p1.price, quantity=1)
            if p2:
                OrderItem.objects.create(order=demo_order, product=p2, product_name=p2.name, product_brand=p2.brand, price=p2.price, quantity=1)
            PaymentTransaction.objects.create(
                order=demo_order,
                transaction_uuid='CURL-NP-DEMO01-1712000000',
                transaction_code='ESEWA-TX-998822',
                provider='eSewa Sandbox v2',
                amount=Decimal('3900.00'),
                status='PAID',
                is_verified=True
            )

        demo_order2, ord2_created = Order.objects.get_or_create(
            order_number='CURL-NP-DEMO02',
            defaults={
                'user': test_user,
                'full_name': 'Aarav Shrestha',
                'email': 'aarav@example.com',
                'phone': '9841234567',
                'delivery_address': 'Jhamsikhel Ward 3',
                'city': 'Lalitpur',
                'district': 'Lalitpur',
                'payment_method': 'COD',
                'payment_status': 'PENDING',
                'order_status': 'PLACED',
                'subtotal': Decimal('2700.00'),
                'delivery_fee': Decimal('100.00'),
                'total_amount': Decimal('2800.00'),
            }
        )
        if ord2_created:
            p3 = Product.objects.filter(brand='Cantu Shea Butter').first()
            p4 = Product.objects.filter(brand='Curl Up').first()
            if p3:
                OrderItem.objects.create(order=demo_order2, product=p3, product_name=p3.name, product_brand=p3.brand, price=p3.price, quantity=1)
            if p4:
                OrderItem.objects.create(order=demo_order2, product=p4, product_name=p4.name, product_brand=p4.brand, price=p4.price, quantity=1)

        self.stdout.write(self.style.SUCCESS("✓ Successfully seeded all CURLIQUE demonstration data!"))
