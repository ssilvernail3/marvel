# MarvelPedia

MarvelPedia is a dynamic web app that lets users explore Marvel superheroes and villains via the official Marvel API. Users can search for any Marvel character and view real-time character data in an interactive comic-inspired interface.

Registered users can also create their own custom "Supers" with abilities and origin stories.

## Features

- 🔎 **Public Marvel Search** (no login required)
- 🦸 **Character Cards** with dynamic data and images
- 📝 **User Registration and Login**
- ✨ **Create, Edit, and Delete custom Supers**
- 🎨 **Comic + Retro design with animated cards**
- 🔐 **Per-route authentication for protected features**
- 🚀 **Responsive design, mobile-friendly**

## Tech Stack

- **Flask** (Python web framework)
- **PostgreSQL** (database)
- **SQLAlchemy** (ORM)
- **WTForms** (forms & validation)
- **Flask-Bcrypt** (secure password hashing)
- **Marvel API** (external character data)
- **Bootstrap** (styling)
- **Custom CSS** (comic-inspired theming)
- **JavaScript + Axios** (API requests)

## Setup

1️⃣ Clone the repo:

bash
git clone https://github.com/ssilvernail3/marvel.git
cd Marvel

2️⃣ Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Create .env file with Marvel API keys
# In your project root, create a file named .env and add:
MARVEL_PUBLIC_KEY=your_public_key
MARVEL_PRIVATE_KEY=your_private_key

4️⃣ Run the app locally
flask run

5️⃣ Visit in your browser:
http://localhost:5000/

Future Improvements
	•	Add multi-hero search
	•	Add favorites system
	•	Deploy live on Render
	•	Add user profile pages

⸻

Credits

Developed by Shane Silvernail
© 2025 Marvel — API data provided by Marvel.



