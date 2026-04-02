from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from typing import List, Tuple
from pathlib import Path


app = FastAPI(title="Food Recommendation API")
BASE_DIR = Path(__file__).resolve().parents[2]

# Load artifacts
rules_path = Path("rules.pkl")
popular_path = Path("popular.pkl")

with open(rules_path, "rb") as f:
    rules = pickle.load(f)

with open("popular.pkl", "rb") as f:
    popular_products = pickle.load(f)


# Build product lookup for normalization
all_products = set()

for _, row in rules.iterrows():
    all_products.update(row["antecedents"])
    all_products.update(row["consequents"])

product_lookup = {
    product.lower().strip(): product
    for product in all_products
}


class RecommendationRequest(BaseModel):
    products: List[str]
    top_n: int = 5


def normalize_products(products: List[str]) -> Tuple[List[str], List[str]]:
    normalized = []
    unknown = []

    for product in products:
        key = product.lower().strip()

        if key in product_lookup:
            canonical_name = product_lookup[key]
            if canonical_name not in normalized:
                normalized.append(canonical_name)
        else:
            unknown.append(product)

    return normalized, unknown


def recommend_from_cart(cart_items: List[str], rules, popular_products, top_n: int = 5) -> List[str]:
    cart_set = set(cart_items)

    matched_rules = rules[
        rules["antecedents"].apply(lambda x: set(x).issubset(cart_set))
    ].copy()

    if not matched_rules.empty:
        matched_rules["antecedent_size"] = matched_rules["antecedents"].apply(len)

        matched_rules = matched_rules.sort_values(
            by=["antecedent_size", "lift", "confidence"],
            ascending=[False, False, False]
        )

        recommendations = []

        for _, row in matched_rules.iterrows():
            consequents = list(row["consequents"])

            for item in consequents:
                if item not in cart_set and item not in recommendations:
                    recommendations.append(item)

        if recommendations:
            return recommendations[:top_n]

    # Fallback to popular products if no matching rule found
    fallback = [p for p in popular_products if p not in cart_set]
    return fallback[:top_n]


@app.get("/")
def home():
    return {"message": "Food Recommendation API running"}


@app.post("/recommend")
def recommend(request: RecommendationRequest):
    normalized_products, unknown_products = normalize_products(request.products)

    if request.top_n <= 0:
        return {
            "input": request.products,
            "normalized_input": normalized_products,
            "unknown_products": unknown_products,
            "recommendations": [],
            "message": "top_n must be greater than 0."
        }

    if not normalized_products:
        return {
            "input": request.products,
            "normalized_input": [],
            "unknown_products": unknown_products,
            "recommendations": popular_products[:request.top_n],
            "message": "No valid products found in input. Returning popular products."
        }

    recommendations = recommend_from_cart(
        normalized_products,
        rules,
        popular_products,
        request.top_n
    )

    return {
        "input": request.products,
        "normalized_input": normalized_products,
        "unknown_products": unknown_products,
        "recommendations": recommendations
    }