# CURLIQUE — A Personalised Curly-Hair Care Platform for Nepal
**Computing Second Year Project (SYP)**  
*Developed strictly in accordance with the Approved College Proposal*

---

## 1. Executive Summary & Problem Context in Nepal

In Nepal, individuals with wavy, curly, or coily hair (Curl Types 2A to 4C) face unique hair-care challenges:
1. **Paucity of Tailored Guidance:** Most commercial products marketed in Nepal assume straight hair, leading to widespread issues of chronic frizz, moisture starvation, and cuticle breakage.
2. **Climate Extremes:** The extreme humidity of the Nepal monsoon season creates uncontrollable swelling and flyaways, while the dry, cold Kathmandu winters cause moisture depletion.
3. **Salon Misconceptions:** Most local salons and barbers in Nepal are trained exclusively in straight-hair cutting techniques and frequently use thinning scissors (*khourine kainchi*), which shred curl clumps and cause irreversible frizz.
4. **Product Availability & Guesswork:** Users frequently import costly products that do not match their strand porosity or density.

**CURLIQUE** resolves these challenges by providing:
- An interactive **Curl Profile Quiz** that gathers curl pattern (2A–4C), porosity (cuticle openness), density, scalp type, concerns, and budget tier.
- A **100% Deterministic Rule-Based Diagnosis Engine** that computes the user's Moisture vs. Protein balance, generates a customized 5-step CGM regimen, and recommends authentic products available in Nepal in Nepalese Rupees (NPR).
- A **Product Compatibility Checker** allowing users to check whether any catalogue product is chemically suitable for their saved profile.
- A **Nepali Haircut Style Guide** with literal scripts to instruct local stylists.
- Complete **E-Commerce Shopping Cart and Checkout** with Cash on Delivery (COD) and verified **eSewa Sandbox** integration.

---

## 2. Technology Compliance Checklist

This project strictly adheres to the approved technology restrictions. **No prohibited technologies have been used.**

| Approved Technology | Purpose in CURLIQUE | Status |
|---|---|:---:|
| **Python 3.12+ / 3.14+** | Backend server programming, rule engine execution | ✅ Active |
| **Django (6.1 / 5.x)** | Full-stack web framework, authentication, ORM | ✅ Active |
| **SQLite 3** | Primary relational database for local development | ✅ Active |
| **PostgreSQL** | Alternative production deployment database config | ✅ Ready |
| **HTML5 & CSS3** | Semantic structure, warm curl aesthetic styling | ✅ Active |
| **JavaScript (Vanilla)** | Quiz stepper, live delivery calculations, eSewa form | ✅ Active |
| **Bootstrap 5.3** | Responsive UI components, grid layout, mobile readiness | ✅ Active |
| **eSewa Sandbox v2** | Test payment gateway with HMAC-SHA256 signatures | ✅ Active |
| **Render / PythonAnywhere** | Production deployment hosting target | ✅ Ready |

### Strict Prohibition Verification
- ❌ **React / Vue / Angular / Next.js / Vite:** NOT USED. Frontend rendered entirely via Django Templates.
- ❌ **TypeScript / Node.js / Express:** NOT USED. Backend is 100% Python/Django.
- ❌ **Tailwind CSS:** NOT USED. Standard CSS and Bootstrap 5.3 used.
- ❌ **MongoDB / Firebase / Supabase:** NOT USED. SQLite / PostgreSQL ORM used.
- ❌ **AI / Machine Learning / External AI APIs:** NOT USED. Recommendation and diagnosis engine is 100% deterministic, transparent Python rules.

---

## 3. Project Architecture & Directory Structure

```text
current syp project/
│
├── curlique/                       # Project Configuration Root
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Core settings, SQLite default, Nepal Timezone, eSewa configs
│   ├── urls.py                     # Primary routing table
│   └── wsgi.py                     # Production WSGI gateway
│
├── accounts/                       # App A: User Accounts & Profiles
│   ├── admin.py
│   ├── forms.py                    # Registration, Login, Profile forms
│   ├── models.py                   # UserProfile (phone, city, address, bio)
│   ├── urls.py
│   └── views.py                    # register, login, logout, profile, edit_profile
│
├── quizzes/                        # App B: Curl Diagnostic Quiz
│   ├── admin.py
│   ├── forms.py                    # Multi-step curl profile input form
│   ├── models.py                   # HairProfile (curl_type, porosity, density, scalp, budget)
│   ├── context_processors.py       # Exposes active hair profile to navbar
│   ├── urls.py
│   └── views.py                    # quiz_view, quiz_result_view, retake_quiz_view
│
├── recommendations/                # App C: Rule-Based Engine & Routine
│   ├── admin.py
│   ├── engine.py                   # Pure Python diagnostic rules & compatibility analyzer
│   ├── models.py                   # CurlCareRule
│   ├── urls.py
│   └── views.py                    # routine_detail_view, compatibility_checker_view
│
├── shop/                           # App D: Catalogue & Haircut Guide
│   ├── admin.py                    # Full product/stock management
│   ├── models.py                   # Category, SuitabilityTag, Product, HaircutGuide
│   ├── urls.py
│   ├── views.py                    # home, product_list, product_detail, haircut_guides
│   └── management/
│       └── commands/
│           └── seed_data.py        # Database seed command for college demonstration
│
├── orders/                         # App E: Cart, Checkout & eSewa Sandbox
│   ├── admin.py                    # Order management, inlines & KPI reports
│   ├── context_processors.py       # Exposes cart item count to navbar
│   ├── esewa.py                    # eSewa v2 signature generator & verifier
│   ├── forms.py                    # CheckoutForm with Nepal city delivery calculation
│   ├── models.py                   # Cart, CartItem, Order, OrderItem, PaymentTransaction
│   ├── urls.py
│   └── views.py                    # cart, checkout, order_success, esewa_initiate, esewa_success
│
├── static/                         # Static Assets
│   ├── css/
│   │   └── curlique.css            # Custom warm curl aesthetic CSS variables & components
│   └── js/
│       └── curlique.js             # Vanilla JS: quiz wizard stepper, city delivery fee listener
│
├── templates/                      # Django HTML Templates
│   ├── base.html                   # Master layout with Bootstrap 5, navbar, cart badge, footer
│   ├── accounts/                   # login.html, register.html, profile.html, edit_profile.html
│   ├── quizzes/                    # quiz.html (6-step progressive wizard), quiz_result.html
│   ├── recommendations/            # routine_detail.html, compatibility_checker.html
│   ├── shop/                       # home.html, product_list.html, product_detail.html, haircut guides
│   ├── orders/                     # cart.html, checkout.html, order_success.html, esewa pages
│   └── admin/                      # orders_reports.html (Admin dashboard analytics)
│
├── curlique_test.py                # Comprehensive automated test suite (10 test cases)
├── requirements.txt                # Python dependencies
├── Procfile                        # Render / Heroku process configuration
├── runtime.txt                     # Target Python version
└── manage.py                       # Django management CLI
```

---

## 4. Local Setup & Execution Instructions

### Prerequisites
- Python 3.10+ installed on your computer.
- Visual Studio Code (or any standard code editor).

### Step-by-Step Setup
1. **Open Visual Studio Code:**
   Open the `current syp project` folder in VS Code.

2. **Activate the Virtual Environment:**
   In the integrated PowerShell terminal, activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   *(Or on Linux/macOS: `source venv/bin/activate`)*

3. **Install Requirements (if starting fresh):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate Demonstration Data:**
   Run the custom seed command to populate demo products, categories, curl care rules, haircut guides, and test accounts:
   ```bash
   python manage.py seed_data
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your web browser and navigate to:
   **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 5. College Viva Demonstration Credentials

The seed command creates pre-configured accounts for examination demonstrations:

| Account Type | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `Admin1234!` | Access to Django Admin, order fulfillment, price/stock edits, and Analytics Reports |
| **Test Customer** | `aarav` | `CurlyPass123!` | Regular customer with pre-saved 3B High Porosity curl diagnosis and order history |

---

## 6. Detailed Feature Implementation

### A. Curl Profile Quiz (Wizard)
- Progressive 6-step interactive questionnaire built with clean vanilla JS navigation.
- Gathers:
  1. **Curl Pattern:** 2A through 4C with clumping descriptions.
  2. **Hair Porosity:** Low, Medium, High (with shower absorption indicators).
  3. **Strand Thickness/Density:** Fine, Medium, Coarse.
  4. **Scalp Condition:** Oily, Balanced/Normal, Dry, Sensitive.
  5. **Specific Concerns:** Frizz, Dryness, Breakage, Dandruff, Volume, Heat Damage.
  6. **Budget Tier in Nepal:** Under NPR 1,000 / NPR 1,000–2,500 / NPR 2,500+.

### B. Rule-Based Diagnosis Engine (`recommendations/engine.py`)
- Strictly deterministic mathematical and conditional rules:
  - **Moisture vs. Protein Balance:** e.g., High Porosity + Breakage triggers 60% Moisture / 40% Protein ratio with Hydrolyzed Wheat/Keratin advice; Low Porosity triggers 90% Moisture / 10% Protein ratio with warmth/steam advice.
  - **Custom 5-Step Regimen:** Cleanse frequency, Rinse-out detangling (Squish to Condish), Leave-in application (LOC/LCO), Styling cast formation, and Night protection (Satin bonnet / plopping).
  - **Nepal Climate Rules:** Monsoon humidity anti-frizz strategies and winter dryness deep conditioning.

### C. Product Compatibility Checker
- Users select any product in the catalogue to evaluate against their saved profile.
- Outputs:
  - Compatibility Match Score (0–100%).
  - Verdict Badge (*Highly Compatible*, *Good Match*, *Compatible with Caution*, *Not Recommended*).
  - Specific ingredient justifications (e.g., matching protein needs or warning against heavy shea butter on fine strands).
  - INCI ingredient transparency breakdown.

### D. Shopping Cart & Checkout
- Add to cart, modify quantities, delete items.
- Dynamic delivery fee calculation:
  - **Kathmandu Valley (Kathmandu, Lalitpur, Bhaktapur):** NPR 100 (24–48 hours delivery).
  - **Outside Valley (Pokhara, Chitwan, Butwal, etc.):** NPR 180 (2–4 days courier).
- Cash on Delivery (COD) and eSewa Sandbox options.

### E. eSewa Sandbox Integration (`orders/esewa.py`)
- Official eSewa ePay v2 sandbox integration.
- Generates HMAC-SHA256 signature encoded in Base64 using test secret `8gBm/:&EnhH.1/q` and product code `EPAYTEST`.
- Response validation verifies the signature on callback.
- **Never marks an order as paid without successful signature and status verification.**
- Includes an **Academic Viva Sandbox Simulator** button to test verified status transitions even in firewalled offline viva environments.

### F. Haircut Style Guide for Nepal Salons
- 6 curly haircut styles (The DevaCut, The Rezo Cut, Layered Curly Bob, Curly Shag, Tapered Coily Cut, Ouidad Cut).
- Includes the **Nepal Salon Script** with literal phrases instructing barbers/stylists in Nepal never to use thinning scissors (*khourine kainchi*) and to cut curl clumps dry.

### G. Administrator Dashboard & Reports
- Custom analytics page accessible at `/admin/orders/order/dashboard-reports/`.
- Displays total orders, verified paid revenue in NPR, pending orders, and popular products ordered.

---

## 7. Verification & Automated Testing

A dedicated test suite `curlique_test.py` is included to verify all functionality:
```powershell
python curlique_test.py
```
**Test Coverage:**
1. Homepage rendering (200 OK)
2. Product catalogue & filtering by curl type, porosity, budget
3. Product detail & ingredient transparency
4. Haircut style guide & Nepal salon scripts
5. Curl Profile Quiz multi-step submission & saving
6. Rule-based diagnosis & product compatibility checker
7. Cart quantity adjustments & Cash on Delivery checkout
8. eSewa Sandbox payment signature generation, callback verification & database status update
9. User authentication, login, logout, and profile
10. Administrator analytics and popular products report

---

## 8. Deployment Configuration (Render / PythonAnywhere)

The repository is configured for immediate deployment to Render or PythonAnywhere:
- **`Procfile`**: `web: gunicorn curlique.wsgi:application --log-file -`
- **`runtime.txt`**: Specifies Python runtime.
- **`settings.py`**: Reads `DATABASE_URL` for PostgreSQL when deployed, falling back to SQLite for local development. Static files handled with WhiteNoise.
- **Environment Variables:**
  - `DJANGO_SECRET_KEY`: Set your production secret key.
  - `DJANGO_DEBUG`: Set to `False` in production.
  - `DATABASE_URL`: PostgreSQL connection string (provided by Render/Neon/Supabase).
