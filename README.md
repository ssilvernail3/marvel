# MarvelPedia 🦸‍♂️🦹‍♀️

MarvelPedia is a full-stack web application that lets users explore Marvel superheroes and villains using the official Marvel API. Users can register, log in, search for characters, and view detailed information including images, descriptions, comic appearances, and more. Built using Flask and enhanced with dynamic UI elements and animations, this app is a polished and interactive experience.

## 🔍 Features

- Marvel character search using Marvel's public API
- Secure login and user registration system
- Dynamically rendered character cards with full details
- Styled with a vivid animated background and responsive layout
- Ability to create your own custom superheroes and villains
- Clear and friendly UX design

## 🛠 Tech Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** HTML, CSS (custom with animation), JavaScript, jQuery, Bootstrap
- **APIs:** Marvel Developer API
- **Other Tools:** Axios, CryptoJS (for API hash auth), Jinja2

## 🚀 Getting Started

1. Clone the repo:
```bash
git clone https://github.com/ssilvernail3/marvelpedia.git
cd marvelpedia
```

2. Set up virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL and run database migrations:
```bash
createdb marvelpedia
flask db upgrade
```

5. Set Marvel API keys as environment variables:
```bash
export MARVEL_PUBLIC_KEY=your_public_key
export MARVEL_PRIVATE_KEY=your_private_key
```

6. Run the app:
```bash
flask run
```

## 🧪 Sample Marvel Characters
Search for characters like:
- Thor
- Iron Man
- Black Widow
- Captain Marvel
- Loki

## 📸 Screenshots
Coming soon.

## 👨‍💻 Author
**Shane Silvernail**  
[LinkedIn](https://www.linkedin.com/in/ssilvernail3) • [GitHub](https://github.com/ssilvernail3)

---

