
# Ocula Finance

**Ocula Finance** is an AI-assisted financial analytics platform designed to provide intelligent, real-time trading signals and portfolio insights. It leverages AI, automation, and modern web technologies to empower traders with actionable information delivered directly via a responsive dashboard and Telegram alerts.

> 🔗 Visit the platform:  
> 🌐 https://oculafinance.com  
> 🧪 Backup: https://oculafinance.netlify.app/

---

## 🧠 Features

- **AI Trading Assistant** – Predictive models trained on market data (MetaTrader 5 required for AI usage).
- **Real-Time Alerts** – Browser & Telegram-based alerts for trading signals.
- **Integrated Web Dashboard** – Built using ReactJS for fast, responsive interaction.
- **Secure Backend API** – Python Flask-based backend connected to a MongoDB database.
- **Email Integration** – With Zoho and EmailJS for user communication.
- **Environment-based Configurations** – Easily switch between test and production environments.

---

## 🗂️ Project Structure

```bash
Ocula-Finance/
│
├── client/            # ReactJS Frontend
├── server/            # Python Flask Backend + AI
└── README.md
```

---

## ⚙️ Requirements

### Software

| Component        | Version          |
|------------------|------------------|
| Python           | 3.12             |
| Node.js          | 20.11.1          |
| MongoDB          | Atlas or Local   |
| MetaTrader 5     | Required for AI  |
| OS Compatibility | Backend – Any OS <br> AI – Windows only |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/micpana/Ocula-Finance.git
cd Ocula-Finance
```

---

### 2. Setup Environment Variables

#### Backend (Linux/macOS):

```bash
export LIVE_DB_URL="your_live_db_url"
export LIVE_DB_USERNAME="your_username"
export LIVE_DB_PASSWORD="your_password"
export TEST_DB_URL="your_test_db_url"
export TEST_DB_USERNAME="your_test_username"
export TEST_DB_PASSWORD="your_test_password"
export ZOHO_MAIL_API_KEY="your_zoho_key"
export ZOHO_MAIL_SECRET="your_zoho_secret"
export GMAIL_TEST_SMTP_EMAIL="your_gmail"
export GMAIL_TEST_SMTP_PASSWORD="your_password"
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

#### Backend (Windows - PowerShell):

```powershell
$env:LIVE_DB_URL="your_live_db_url"
$env:LIVE_DB_USERNAME="your_username"
$env:LIVE_DB_PASSWORD="your_password"
$env:TEST_DB_URL="your_test_db_url"
$env:TEST_DB_USERNAME="your_test_username"
$env:TEST_DB_PASSWORD="your_test_password"
$env:ZOHO_MAIL_API_KEY="your_zoho_key"
$env:ZOHO_MAIL_SECRET="your_zoho_secret"
$env:GMAIL_TEST_SMTP_EMAIL="your_gmail"
$env:GMAIL_TEST_SMTP_PASSWORD="your_password"
$env:TELEGRAM_BOT_TOKEN="your_bot_token"
```

#### Frontend (Create `.env` in `client/`):

```env
REACT_APP_EmailJsServiceID=your_service_id
REACT_APP_EmailJsTemplateID=your_template_id
REACT_APP_EmailJsAPIKey=your_emailjs_api_key
```

---

### 3. Install Dependencies

#### Frontend

```bash
cd client
npm install
```

#### Backend

```bash
cd ../server
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### Start the Frontend (ReactJS)

```bash
cd client
npm start
```

### Start the Backend (Flask API)

```bash
cd server
python app.py
```

---

## 🧠 AI: Training & Prediction

> 🛡️ **Note:** The AI files are encrypted. Use this decryption key to run them:  
> `Be1XeaQaeJcel4TayW5i7mOiwTPQcl-hf0TmwmEyMBE=`

### AI Requirements

- Run on **Windows only**
- Requires **MetaTrader5** software

### Train the AI Model

```bash
cd server
python x_y_train.py
```

### Run Predictions

```bash
python x_y_predict.py
```

### Configuration

All AI and backend configurations are located in:

```bash
server/settings.py
```

---

## 📬 Telegram Alerts

Ocula Finance includes a **Telegram bot** to send trading alerts alongside browser notifications.

Ensure you set the `TELEGRAM_BOT_TOKEN` environment variable before running the backend.

---

## 🛡️ Security Notes

- All AI files were encrypted during development to preserve intellectual property.
- The decryption key is now public as the project is open source.
- Use environment variables to protect sensitive data in deployment.

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

## 👤 Author

**Michael Panashe Mudimbu**  
🔗 [LinkedIn](https://www.linkedin.com/in/michael-panashe-mudimbu/)  
🐦 [Twitter / X](https://x.com/MudimbuMichael)  
📧 michaelmudimbu@gmail.com

---

## ⭐ Support

If you find this project useful, feel free to give it a ⭐ on [GitHub](https://github.com/micpana/Ocula-Finance)!
