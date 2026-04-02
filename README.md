# 🛒 Smart Basket Recommendation System

A production-ready **product recommendation system** that suggests relevant items based on a user's cart using **Association Rule Mining (Apriori / FP-Growth)**.

---

## 🚀 Live Demo

- 🌐 **Frontend (Streamlit):** https://o-mart.streamlit.app
- ⚡ **Backend API (FastAPI):** https://o-mart-smart-basket-recommendation-system.onrender.com
- 📘 **API Docs:** https://o-mart-smart-basket-recommendation-system.onrender.com/docs

---

## 🧠 Overview

This system analyzes historical transaction data to discover relationships between products and generate **intelligent recommendations**.

It simulates how real-world e-commerce platforms (Amazon, Daraz, etc.) suggest:

> “Customers who bought this also bought…”

---

## ✨ Features

- 🧺 **Multi-product cart recommendations**
- 📊 **Association rule mining (Apriori & FP-Growth)**
- 📈 **Ranking using lift + confidence**
- 🔄 **Cold-start fallback (popular products)**
- ⚡ **FastAPI backend (high performance)**
- 🎨 **Streamlit UI (interactive frontend)**
- ☁️ **Fully deployed (Render + Streamlit Cloud)**

---

## 🏗️ System Architecture

```
User Input (Cart Items)
        ↓
Streamlit UI (Frontend)
        ↓
HTTP Request (POST /recommend)
        ↓
FastAPI Backend (Render)
        ↓
Association Rule Engine
        ↓
Ranking (lift + confidence)
        ↓
JSON Response
        ↓
UI Display (Recommendations)
```

---

## 🛠️ Tech Stack

### 🔹 Backend

- FastAPI
- Uvicorn
- Pandas
- NumPy
- MLxtend (Apriori / FP-Growth)
- Scikit-learn

### 🔹 Frontend

- Streamlit
- Requests

### 🔹 Deployment

- Render (Backend API)
- Streamlit Community Cloud (Frontend)

---

## 📦 Project Structure

```
.
├── notebooks/
│   └── data_exploration.ipynb
│
├── src/
│   ├── api/
│   │   └── main.py          # FastAPI backend
│   │
│   └── ui/
│       └── app.py           # Streamlit frontend
│
├── rules.pkl                # Association rules
├── popular.pkl             # Popular product fallback
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

1. Transaction data is transformed into a **basket format**
2. Frequent itemsets are generated using:
   - Apriori
   - FP-Growth

3. Association rules are extracted with:
   - Support
   - Confidence
   - Lift

4. When a user inputs cart items:
   - Matching rules are selected
   - Recommendations are ranked
   - If no match → fallback to popular items

---

## 📡 API Usage

### Endpoint

```
POST /recommend
```

### Request Body

```json
{
  "products": ["Limes", "Organic Cilantro"],
  "top_n": 5
}
```

### Response

```json
{
  "input": ["Limes", "Organic Cilantro"],
  "recommendations": ["Organic Avocado", "Organic Baby Spinach", "Large Lemon"]
}
```

---

## 🖥️ Run Locally

### 1. Clone repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run backend

```bash
uvicorn src.api.main:app --reload
```

### 4. Run frontend

```bash
streamlit run src/ui/app.py
```

---

## 📊 Future Improvements

- 👤 User personalization (user-level recommendations)
- 📉 Evaluation metrics (Precision@K, Recall@K)
- ⚡ Caching & performance optimization
- 🛍️ Add-to-cart interaction in UI
- ⚛️ React-based frontend (production UI)

---

## 🎯 Key Learnings

- Designing end-to-end ML systems
- Building REST APIs using FastAPI
- Deploying full-stack applications
- Applying association rule mining in real scenarios
- Handling real-world constraints (cold start, ranking)

---

## 👨‍💻 Author

**Abdullah Al Maruf**
CSE, RUET

---

## ⭐ If you found this useful

Give this repo a ⭐ and share your feedback!
