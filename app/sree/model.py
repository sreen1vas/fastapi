import openai
import pandas as pd
import json
import time
from tqdm import tqdm
from datetime import datetime
import re
# Set your OpenAI API key
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load your CSV file
df = pd.read_csv("yelp_reviews.csv")

# Sentiment analysis function
def analyze_review(review_text):
    prompt = f"""
    Analyze the following restaurant review and assign a sentiment score (1-10) for the given aspects.
    If an aspect is not mentioned, return 'NA'.

    Review: "{review_text}"

**Definition of aspects:**
- **Food**: Taste, quality, and variety of dishes.
- **Service**: Friendliness, attentiveness, and speed of staff.
- **Ambiance**: Atmosphere, decor, and cleanliness.
- **Delivery**: Speed, accuracy, and overall experience of receiving food, whether dine-in, takeaway, or online delivery.
- **Pricing**: Value for money, affordability.

⚠️ IMPORTANT: Ensure the output always contains all aspects, including "Food", "Service", "Ambiance", "Delivery", and "Pricing".

Return the response in JSON format:
{{
"Food": <score or "NA">,
"Service": <score or "NA">,
"Ambiance": <score or "NA">,
"Delivery": <score or "NA">,
"Pricing": <score or "NA">
}}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        cleaned_str = result.replace("```json", "").replace("```", "").strip()
       
        cleaned_str = re.sub(r'(:\s*)NA', r'\1"NA"', cleaned_str)


        try:
            data_dict = json.loads(cleaned_str)
        except json.JSONDecodeError:
            print("JSON decode error. Skipping review.")
            return {"Review": review_text}

        cleaned_dict = {key: value for key, value in data_dict.items() if value != "NA"}

        weights = {"Food": 0.3, "Service": 0.25, "Ambiance": 0.2, "Delivery": 0.15, "Pricing": 0.1}
        valid_weights = {key: weights[key] for key in cleaned_dict if key in weights}
        total_weight = sum(valid_weights.values())
        normalized_weights = {key: weight / total_weight for key, weight in valid_weights.items()} if total_weight > 0 else {}

        overall_score = sum(cleaned_dict[key] * normalized_weights[key] for key in normalized_weights) if total_weight > 0 else "NA"
        cleaned_dict["Overall_Score"] = overall_score

        # Bias detection
        bias_flag = "No Bias"
        bias_reasons = []

        if overall_score != "NA" and overall_score >= 7 and any(score <= 3 for score in cleaned_dict.values() if isinstance(score, (int, float))):
            bias_reasons.append("Extreme negative rating in an otherwise positive review.")
        if max(cleaned_dict.values(), default=0) - min(cleaned_dict.values(), default=10) >= 6:
            bias_reasons.append("Large sentiment gap across aspects.")
        if any(word in review_text.lower() for word in ["worst", "terrible", "disgusting", "horrible"]):
            bias_reasons.append("Highly emotional language detected.")

        if bias_reasons:
            bias_flag = "Potential Bias: " + " | ".join(bias_reasons)

        cleaned_dict["Bias_Flag"] = bias_flag

        return {"Review": review_text, **cleaned_dict}
    
    except Exception as e:
        print("Error:", e)
        return {"Review": review_text}

# Batch analyzer with progress + auto-save
def analyze_multiple_reviews(review_texts):
    reviews_data = []
    for i, review in enumerate(tqdm(review_texts, desc="Analyzing reviews"), 1):
        result = analyze_review(review)
        reviews_data.append(result)

        # Optional delay to avoid rate limits
        time.sleep(0.5)

        # Save progress every 100 reviews
        if i % 100 == 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pd.DataFrame(reviews_data).to_csv(f"partial_output_{i}_{timestamp}.csv", index=False)
            print(f"✅ Saved partial output after {i} reviews.")

    return pd.DataFrame(reviews_data)

# Run the model
df_final = analyze_multiple_reviews(list(df['text'].values))

# Save final output
final_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
df_final.to_csv(f"final_output_{final_timestamp}.csv", index=False)
print("✅ Analysis complete. Results saved.")
