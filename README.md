# NutriSync

A Django-based web application for tracking daily food consumption and nutrition intake. NutriSync helps users monitor their dietary habits by logging meals, viewing detailed nutrition information, and analyzing their nutritional patterns over time.

## 🚀 Features

- **User Authentication**: Secure login and registration with Django Allauth
- **Food Logging**: Log meals with automatic nutrition data retrieval
- **Nutrition Tracking**: Track calories, proteins, carbs, fats, fiber, sodium, sugar, and more
- **Dashboard**: Visual analytics with charts showing nutrition trends
- **Meal Categories**: Organize logs by breakfast, lunch, dinner, and snacks
- **User Profile Management**: Customize profile and settings
- **Responsive Design**: Works on desktop and mobile devices
- **PWA Support**: Progressive Web App with service worker for offline functionality


## 🛠️ Tech Stack

- **Backend**: Django 5.2.7, Python
- **Database**: SQLite (local) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Calorie Ninjas API
- **Authentication**: Django Allauth

- **Charting**: Chart.js

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtual environment

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nutrisync
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   CALORIE_NINJAS_API_KEY=your-api-key
   GOOGLE_GENERATIVE_AI_API_KEY=your-api-key
   ```

5. **Run migrations**
   ```bash
   cd projectsite
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://localhost:8000` in your browser.

## 🗄️ Database Models

### FoodLog Model
Tracks individual food consumption entries.

**Fields:**
- `user` - Foreign key to User model
- `food_name` - Name of the food item
- `description` - Optional description
- `calories` - Calorie count
- `meal_type` - Type of meal (breakfast, lunch, dinner, snack)
- `date` - Date of consumption
- `nutrition_data` - JSON field storing detailed nutrition info (proteins, carbs, fats, etc.)
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update

**Nutrition Data Includes:**
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)
- Sodium (mg)
- Sugar (g)
- Potassium (mg)
- Cholesterol (mg)
- Saturated Fat (g)


## 🔧 Core Features Explanation

### Food Logging
Users can log meals by entering food names. The app uses the **Calorie Ninjas API** to automatically retrieve nutrition information for the entered food.

### Dashboard
The dashboard displays:
- Daily calorie intake vs. targets
- Weekly nutrition trends
- Meal category breakdown
- Nutrition statistics (proteins, carbs, fats)

### Services
**CalorieNinjasService** handles:
- Parsing food queries from user input
- Fetching nutrition data from external API
- Extracting and aggregating nutrition information
- Formatting data for storage


## 👥 Authors

- Kert-Ace T. Ombion
- Nicholo Dela Rosa
- John Brence Condesa
- Datu Lachica
- Jon Richmond Vitug
- Ruzz Romil Serra

