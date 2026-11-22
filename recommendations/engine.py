"""
CURLIQUE Rule-Based Diagnosis and Routine Engine
Strictly deterministic Python logic based on approved hair-care science:
- The Curly Girl Method (CGM) adaptations
- Porosity dynamics (Cuticle openness, moisture retention, protein requirements)
- Strand thickness & weight capacity
- Scalp biome & Nepal climate considerations (monsoon humidity & winter dryness)
"""

def generate_hair_diagnosis(profile):
    """
    Generates a full diagnosis, moisture-protein balance recommendation,
    and a step-by-step personalized routine for the given HairProfile.
    """
    curl = profile.curl_type
    porosity = profile.porosity
    density = profile.density
    scalp = profile.scalp_type
    concerns = profile.concerns_list
    budget = profile.budget

    # 1. Determine Title and Core Diagnosis
    curl_family = profile.curl_family
    porosity_label = profile.get_porosity_display().split(' (')[0]
    diagnosis_title = f"{curl} {porosity_label} Porosity {curl_family} Profile"

    # 2. Moisture vs Protein Balance Rule
    if porosity == 'high':
        if 'heat_damage' in concerns or 'breakage' in concerns:
            mp_balance = {
                'moisture': 60,
                'protein': 40,
                'headline': "High Moisture + Intensive Rebuilding Protein",
                'advice': "Your raised cuticles lose hydration quickly and need hydrolyzed proteins to patch structural fissures, followed by rich sealing emollients."
            }
        else:
            mp_balance = {
                'moisture': 70,
                'protein': 30,
                'headline': "Balanced Moisture with Regular Light Protein",
                'advice': "Your hair readily drinks water but struggles to hold it. Focus on layered hydration sealed with nourishing plant oils."
            }
    elif porosity == 'low':
        if 'breakage' in concerns:
            mp_balance = {
                'moisture': 85,
                'protein': 15,
                'headline': "Maximum Moisture with Rare Micro-Protein",
                'advice': "Low porosity cuticles are compact and stiff. Protein overload will cause brittleness. Use gentle warmth, steam, and lightweight humectants."
            }
        else:
            mp_balance = {
                'moisture': 90,
                'protein': 10,
                'headline': "Pure Hydration (Protein-Sensitive)",
                'advice': "Your cuticles are tightly sealed. Prioritize water-based hydration like Aloe Vera and Flaxseed. Avoid heavy proteins that sit on top."
            }
    else:  # medium
        mp_balance = {
            'moisture': 75,
            'protein': 25,
            'headline': "Ideal Equilibrium (Maintenance & Elasticity)",
            'advice': "Your cuticles are well-aligned. Alternate between hydrating deep conditioners and light monthly protein treatments to preserve bounce."
        }

    # 3. Step-by-Step Personalized Routine Steps
    # Step 1: Cleanse (Wash Day)
    if scalp == 'oily':
        step1_title = "Clarifying Cleanse & Scalp Detox"
        step1_freq = "2 to 3 times per week"
        step1_desc = "Use a gentle sulfate-free clarifying shampoo to cleanse excess sebum without stripping natural curl oils. Massage scalp thoroughly with fingertips for 2 minutes."
        step1_tags = ['sulfate-free', 'clarifying', 'tea-tree']
    elif scalp == 'dry' or scalp == 'sensitive':
        step1_title = "Hydrating Cream Cleanse / Low-Poo"
        step1_freq = "1 to 2 times per week"
        step1_desc = "Cleanse with an ultra-moisturizing, sulfate-free cream wash. Focus only on the scalp. Let the lather gently rinse down the strand lengths."
        step1_tags = ['sulfate-free', 'cg-friendly', 'moisture-rich']
    else:
        step1_title = "Balanced Gentle Cleanse"
        step1_freq = "2 times per week"
        step1_desc = "Wash with a botanical low-poo shampoo. Cleanses environmental dust and pollution common in Nepal cities without stripping moisture."
        step1_tags = ['sulfate-free', 'cg-friendly']

    # Step 2: Condition & Detangle
    if porosity == 'low':
        step2_title = "Lightweight Condition & Squish-to-Condish"
        step2_desc = "Apply a lightweight, silicone-free conditioner. Use warm water to open cuticles. Detangle gently using your fingers or a wide-tooth comb while hair is soaking wet with conditioner slip."
        step2_tags = ['lightweight', 'silicone-free', 'cg-friendly']
    elif porosity == 'high':
        step2_title = "Deep Nourishing Mask & Cuticle Smoothing"
        step2_desc = "Apply a rich, emollient conditioner or deep mask with Shea Butter and Hydrolyzed Keratin. Squeeze into lengths ('Squish to Condish') until hair feels like wet silk. Rinse with lukewarm or cool water to seal cuticles."
        step2_tags = ['moisture-rich', 'protein-rich', 'cg-friendly']
    else:
        step2_title = "Hydrating Detangle & Rinse"
        step2_desc = "Distribute conditioner generously through ends and mid-lengths. Gently detangle from ends upwards to prevent knot breakage. Rinse thoroughly."
        step2_tags = ['moisture-rich', 'cg-friendly']

    # Step 3: Leave-In & Moisture Foundation
    if density == 'fine':
        step3_title = "Weightless Leave-In Mist or Milk"
        step3_desc = "Spray or smooth a dime-sized amount of lightweight leave-in over dripping wet curls. Fine strands get easily weighed down; avoid thick butters near the root area."
        step3_tags = ['lightweight', 'aloe-based', 'leave-in']
    elif density == 'coarse' or curl.startswith('4'):
        step3_title = "Rich Leave-In Butter & LOC / LCO Method"
        step3_desc = "Apply a generous amount of curl cream (Liquid/Leave-in), follow with a nourishing oil (Oil), and seal with butter/cream (LOC method) to lock in moisture for days."
        step3_tags = ['heavy-butter', 'moisture-rich', 'leave-in']
    else:
        step3_title = "Hydrating Curl Cream"
        step3_desc = "Rake a nickel-sized amount of leave-in curl cream through damp sections using praying hands technique to clump curls together."
        step3_tags = ['moisture-rich', 'cg-friendly', 'leave-in']

    # Step 4: Styling & Definition (Cast Formation)
    if curl.startswith('2'):
        step4_title = "Curl Defining Mousse or Light Gel"
        step4_desc = "Scrunch an alcohol-free curl mousse or light-hold gel upwards towards the scalp while your head is tilted. This creates defined waves without crunch or flatness."
        step4_tags = ['lightweight', 'alcohol-free', 'styling-gel']
    elif curl.startswith('4'):
        step4_title = "Curl Custard / Twisting Pudding"
        step4_desc = "Work a firm-hold curling custard or styling gel through wet sections. Ideal for twist-outs, braid-outs, or wash-and-go definition with maximum shrinkage control."
        step4_tags = ['heavy-butter', 'styling-gel', 'cg-friendly']
    else:
        step4_title = "Strong Hold Flaxseed or Botanical Gel"
        step4_desc = "Smooth a botanical gel over wet curl clumps to form a protective 'gel cast'. This locks out Nepal's monsoon humidity and shields curls from winter frizz."
        step4_tags = ['cg-friendly', 'styling-gel', 'alcohol-free']

    # Step 5: Drying, Sealing & Night Protection
    nepal_climate_tip = (
        "In Nepal's monsoon or humid summer, scrunch out the gel crunch (SOTC) with 2 drops of Argan or Jojoba oil. "
        "In winter, sleep with a satin bonnet or silk pillowcase to prevent dry air from siphoning hair moisture."
    )
    step5_title = "Microfiber Plopping, Diffusing & Satin Sleep"
    step5_desc = (
        "Microfiber towel plop for 15 minutes. Air dry or diffuse on low heat with the cup pushed gently upwards. "
        "Once 100% dry, 'Scrunch Out The Crunch' (SOTC) for soft, bouncy ringlets. " + nepal_climate_tip
    )
    step5_tags = ['accessories', 'oil-based']

    routine_steps = [
        {'step_number': 1, 'category': 'Cleanse', 'title': step1_title, 'frequency': step1_freq, 'instructions': step1_desc, 'tags': step1_tags},
        {'step_number': 2, 'category': 'Condition', 'title': step2_title, 'frequency': "Every wash session", 'instructions': step2_desc, 'tags': step2_tags},
        {'step_number': 3, 'category': 'Leave-In Foundation', 'title': step3_title, 'frequency': "Post-wash on damp hair", 'instructions': step3_desc, 'tags': step3_tags},
        {'step_number': 4, 'category': 'Define & Hold', 'title': step4_title, 'frequency': "Styling day", 'instructions': step4_desc, 'tags': step4_tags},
        {'step_number': 5, 'category': 'Protect & Dry', 'title': step5_title, 'frequency': "Daily / Bedtime routine", 'instructions': step5_desc, 'tags': step5_tags},
    ]

    # 4. Golden Dos and Don'ts for Nepal Curls
    dos = [
        "Detangle ONLY when hair is wet and coated with slippery conditioner — never dry brush curls.",
        "Use a cotton t-shirt or microfiber towel to dry hair; standard terrycloth towels cause friction frizz.",
        "Sleep on a satin pillowcase or wear a satin bonnet to protect curl patterns overnight.",
        "When visiting a hair salon in Nepal, explicitly instruct the barber/stylist NOT to use thinning shears on your curls.",
    ]
    donts = [
        "Avoid sulfates (Sodium Lauryl Sulfate) in daily shampoos — they strip away natural sebum.",
        "Avoid non-water-soluble silicones (Dimethicone) without clarifying shampoos, as they create waterproof barrier buildup.",
        "Do not touch or scrunch curls while they are air drying or drying under a diffuser; wait until 100% dry.",
        "Avoid hot water rinses — lukewarm water maintains moisture, and cool water seals cuticles.",
    ]

    return {
        'diagnosis_title': diagnosis_title,
        'curl_family': curl_family,
        'mp_balance': mp_balance,
        'routine_steps': routine_steps,
        'dos': dos,
        'donts': donts,
    }


def evaluate_product_compatibility(product, profile):
    """
    Evaluates how suitable a catalogue Product is for a given HairProfile.
    Returns a score (0 to 100), verdict label, positives, cautions, and application tip.
    """
    score = 70  # Baseline
    positives = []
    cautions = []

    # 1. Curl Type Match
    suitable_curls = [c.strip() for c in product.suitable_curl_types.split(',') if c.strip()]
    if profile.curl_type in suitable_curls:
        score += 10
        positives.append(f"Specifically formulated for curl pattern {profile.curl_type} ({profile.curl_family}).")
    elif profile.curl_family in [c.strip() for c in product.suitable_curl_types.split(',')]:
        score += 8
        positives.append(f"Formulated for {profile.curl_family} hair types.")
    else:
        score -= 15
        cautions.append(f"May not cater optimally to the unique curl elasticity of {profile.curl_type}.")

    # 2. Porosity Match
    suitable_porosity = [p.strip().lower() for p in product.suitable_porosity.split(',') if p.strip()]
    prod_tags = [t.slug for t in product.suitability_tags.all()]

    if profile.porosity in suitable_porosity:
        score += 10
        positives.append(f"Optimized for {profile.get_porosity_display().split(' ')[0]} porosity cuticles.")
    else:
        score -= 10
        cautions.append(f"Not tailored specifically for {profile.porosity} porosity cuticles.")

    # High Porosity checks
    if profile.porosity == 'high':
        if 'protein-rich' in prod_tags:
            score += 10
            positives.append("Contains hydrolyzed proteins to reinforce raised cuticles and reduce structural breakage.")
        if 'moisture-rich' in prod_tags or 'heavy-butter' in prod_tags:
            score += 5
            positives.append("Rich emollient base helps seal moisture inside highly porous strands.")

    # Low Porosity checks
    if profile.porosity == 'low':
        if 'heavy-butter' in prod_tags:
            score -= 15
            cautions.append("Contains heavy butters that may sit on top of compact low-porosity cuticles and cause buildup.")
        if 'lightweight' in prod_tags or 'aloe-based' in prod_tags:
            score += 10
            positives.append("Lightweight formulation easily penetrates closed low-porosity cuticles without heaviness.")
        if 'protein-rich' in prod_tags:
            score -= 8
            cautions.append("High protein content — use sparingly to prevent protein stiffness in low-porosity hair.")

    # 3. Density / Strand Thickness checks
    if profile.density == 'fine':
        if 'heavy-butter' in prod_tags:
            score -= 12
            cautions.append("Too rich for fine strands; may flatten crown volume.")
        if 'lightweight' in prod_tags:
            score += 8
            positives.append("Featherlight formula maintains natural volume and bounce in fine hair.")
    elif profile.density == 'coarse':
        if 'moisture-rich' in prod_tags or 'heavy-butter' in prod_tags:
            score += 8
            positives.append("Provides the deep hydration and softening coarse strands crave.")

    # 4. Scalp Type checks
    if profile.scalp_type == 'oily':
        if 'tea-tree' in prod_tags or 'clarifying' in prod_tags:
            score += 10
            positives.append("Purifying ingredients help regulate excess scalp oil and build-up.")
        if product.category.slug == 'scalp-oils' and 'heavy-butter' in prod_tags:
            score -= 10
            cautions.append("Avoid applying heavy oils directly to an oily scalp.")
    elif profile.scalp_type == 'sensitive':
        if 'sulfate-free' in prod_tags and 'silicone-free' in prod_tags:
            score += 8
            positives.append("Clean, gentle ingredients that avoid irritating sensitive scalp tissue.")

    # 5. Curly Girl Friendly check
    if 'cg-friendly' in prod_tags:
        score += 5
        positives.append("100% Curly Girl Method (CGM) approved — zero harsh sulfates or drying alcohols.")

    # Cap score
    score = max(20, min(99, score))

    if score >= 85:
        verdict = "Highly Compatible"
        badge_class = "success"
    elif score >= 65:
        verdict = "Good Compatibility"
        badge_class = "primary"
    elif score >= 50:
        verdict = "Compatible with Caution"
        badge_class = "warning"
    else:
        verdict = "Not Recommended for Profile"
        badge_class = "danger"

    return {
        'score': score,
        'verdict': verdict,
        'badge_class': badge_class,
        'positives': positives,
        'cautions': cautions,
    }
