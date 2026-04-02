import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Food Recommendation System",
    page_icon="🛒",
    layout="centered"
)

# Title
st.title("🛒 Smart Basket Recommender")
st.caption("Add items from your cart and discover what to buy next.")

# Input
products_input = st.text_input(
    "What's in your cart?",
    placeholder="e.g. limes, organic cilantro"
)

# Button
if st.button("Get Recommendations", use_container_width=True):
    products = [p.strip() for p in products_input.split(",") if p.strip()]

    if not products:
        st.warning("Please enter at least one product.")
    else:
        payload = {
            "products": products,
            "top_n": 5   # fixed like real systems
        }

        try:
            response = requests.post(
                f"{API_URL}/recommend",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                recommendations = data.get("recommendations", [])
                unknown_products = data.get("unknown_products", [])

                st.markdown("## 🛒 You may also like")

                if recommendations:
                    for item in recommendations:
                        st.markdown(
                            f"""
                            <div style="
                                padding: 14px 18px;
                                margin-bottom: 12px;
                                border-radius: 12px;
                                background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
                                border: 1px solid #333;
                                font-size: 18px;
                                font-weight: 600;
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                            ">
                                <span>{item}</span>
                                <span style="font-size:14px; color:#9ca3af;">+ Add</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No recommendations found.")

                if unknown_products:
                    st.caption(
                        "⚠️ Some items were not recognized: "
                        + ", ".join(unknown_products)
                    )

            else:
                st.error(f"API error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to backend. Make sure FastAPI is running."
            )
        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again.")