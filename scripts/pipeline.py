import os
import pandas as pd
from datasets import load_dataset
import re
from tqdm import tqdm
from collections import Counter
import numpy as np
import random


# CONFIGURATION
SAMPLE_SIZE = 2000  # Total reviews to process (will aim for 50/50 split)

# PATHS
RAW_PATH = "data/raw/raw_reviews.csv"
STAGED_PATH = "data/staged/clean_reviews.csv"
ANALYSIS_PATH = "data/results/analysis.csv"
KEYWORDS_PATH = "data/results/keywords.csv"
SUGGESTION_PATH = "data/results/suggestion.csv"

# ==========================================
# MANUAL KNOWLEDGE BASE
# ==========================================
KEYWORD_MAP = {
    "positive": ["อร่อย", "ดี", "เยี่ยม", "ชอบ", "แนะนำ", "สด", "สะอาด", "คุ้ม", "เร็ว", "สวย", "เลิศ", "ถูกใจ", "หอม", "นุ่ม"],
    "negative": ["แย่", "ไม่อร่อย", "ช้า", "แพง", "สกปรก", "เหม็น", "ห่วย", "น้อย", "เค็ม", "จืด", "ดิบ", "รอนาน", "ผิดหวัง", "แมลงสาบ", "แข็ง", "ไม่ได้เรื่อง", "เสียดาย"],
    "service": ["พนักงาน", "บริการ", "เสิร์ฟ", "ต้อนรับ", "พูดจา", "คนขาย", "รอ", "คิว", "ช้า", "หน้างอ"],
    "price": ["ราคา", "บาท", "แพง", "ถูก", "เช็คบิล", "คุ้ม", "กระเป๋า"],
    "atmosphere": ["บรรยากาศ", "ร้าน", "แอร์", "เสียง", "ที่นั่ง", "โต๊ะ", "ห้องน้ำ", "จอดรถ", "ร้อน", "ยุง"],
    "location": ["ทางเข้า", "ซอย", "ถนน", "ที่จอด", "mrt", "bts", "หาอยาก", "แผนที่"],
}

SUGGESTION_RULES = {
    "food": [
        {"suggestion": "Review recipes and check ingredient freshness daily", "severity": "High", "resources": "Medium (Cost of Goods)", "priority": 1},
        {"suggestion": "Conduct blind taste testing with staff before serving", "severity": "Medium", "resources": "Low (Time)", "priority": 2},
        {"suggestion": "Revise menu to remove unpopular/complained items", "severity": "Low", "resources": "Low", "priority": 3}
    ],
    "service": [
        {"suggestion": "Conduct urgent staff training on hospitality standards", "severity": "High", "resources": "Low (Training Time)", "priority": 1},
        {"suggestion": "Implement a queue management system", "severity": "Medium", "resources": "Medium", "priority": 2},
        {"suggestion": "Hire additional part-time staff for peak hours", "severity": "High", "resources": "High (Salary)", "priority": 3}
    ],
    "price": [
        {"suggestion": "Analyze portion sizes vs competitors", "severity": "High", "resources": "Low", "priority": 1},
        {"suggestion": "Introduce value-set menus or lunch promotions", "severity": "Medium", "resources": "Medium", "priority": 2}
    ],
    "atmosphere": [
        {"suggestion": "Deep clean the facility (especially restrooms)", "severity": "High", "resources": "Low", "priority": 1},
        {"suggestion": "Adjust lighting or music volume", "severity": "Low", "resources": "Low", "priority": 2},
        {"suggestion": "Renovate or repair broken furniture", "severity": "Medium", "resources": "High", "priority": 3}
    ],
    "location": [
        {"suggestion": "Improve signage visibility on the main road", "severity": "Medium", "resources": "Medium", "priority": 1},
        {"suggestion": "Update Google Maps pin and add clear directions online", "severity": "Low", "resources": "Low", "priority": 2}
    ]
}

def ensure_directories():
    dirs = ["data/raw", "data/staged", "data/results"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# ==========================================
# 1. EXTRACT
# ==========================================
def extract_data():
    print("--- Starting Extraction ---")
    if os.path.exists(RAW_PATH):
        print(f"Raw data found at {RAW_PATH}. (Assuming it contains full dataset).")
        return

    try:
        print("Downloading FULL dataset from Hugging Face...")
        dataset = load_dataset("iamwarint/wongnai-restaurant-review")
        df = pd.DataFrame(dataset['train'])
        
        ensure_directories()
        df.to_csv(RAW_PATH, index=False, escapechar='\\') 
        print(f"Extraction complete. Saved {len(df)} rows to {RAW_PATH}.")
        
    except Exception as e:
        print(f"CRITICAL ERROR during extraction: {e}")
        exit(1)

# ==========================================
# 2. TRANSFORM (BALANCED SAMPLING)
# ==========================================
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.replace("\n", " ").strip()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^\u0E00-\u0E7Fa-zA-Z0-9\s\.\,\!\?]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def pre_classify_sentiment(text):
    """
    Quickly guesses sentiment based on keywords to help with sampling.
    """
    if not isinstance(text, str): return "neutral"
    pos_score = sum(1 for word in KEYWORD_MAP['positive'] if word in text)
    neg_score = sum(1 for word in KEYWORD_MAP['negative'] if word in text)
    if neg_score > pos_score: return "bad"
    if pos_score > neg_score: return "good"
    return "neutral"

def transform_data():
    print("\n--- Starting Transformation (Randomized Balance) ---")
    try:
        # Read the FULL raw file
        df = pd.read_csv(RAW_PATH, engine='python', on_bad_lines='skip', escapechar='\\')
        
        # Identify Review Column
        target_col = 'review_body' if 'review_body' in df.columns else 'review'
        
        # 1. Quick classification to separate pools
        print("Pre-classifying reviews to separate pools...")
        df['temp_sentiment'] = df[target_col].astype(str).apply(pre_classify_sentiment)
        
        pool_good = df[df['temp_sentiment'] == 'good']
        pool_bad = df[df['temp_sentiment'] == 'bad']
        
        print(f"Pool Available: {len(pool_good)} GOOD | {len(pool_bad)} BAD")
        
        # ==========================================
        # NEW LOGIC: Random Split (50% - 90% Good)
        # ==========================================
        good_ratio = random.uniform(0.5, 0.9)
        target_good_count = int(SAMPLE_SIZE * good_ratio)
        target_bad_count = SAMPLE_SIZE - target_good_count
        
        print(f"Target Ratio: {good_ratio:.1%} Good Reviews")
        print(f"Target Counts: {target_good_count} Good | {target_bad_count} Bad")

        # Sample Good
        n_good = min(len(pool_good), target_good_count)
        sample_good = pool_good.sample(n=n_good, random_state=42)
        
        # Sample Bad
        n_bad = min(len(pool_bad), target_bad_count)
        sample_bad = pool_bad.sample(n=n_bad, random_state=42)
        
        print(f"Selected Actual: {len(sample_good)} GOOD and {len(sample_bad)} BAD reviews.")
        
        # Combine
        balanced_df = pd.concat([sample_good, sample_bad])
        
        # Shuffle result so they aren't ordered by sentiment
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

        # 3. Clean Text
        balanced_df['review_text'] = balanced_df[target_col].apply(clean_text)
        balanced_df = balanced_df[balanced_df['review_text'].str.len() > 5]

        output_df = balanced_df[['review_text']].copy()
        output_df.to_csv(STAGED_PATH, index=False)
        print(f"Transformation complete. Saved {len(output_df)} reviews to {STAGED_PATH}")
        
    except Exception as e:
        print(f"CRITICAL ERROR during transformation: {e}")
        exit(1)

# ==========================================
# 3. ANALYZE AND LOAD
# ==========================================
def analyze_review_manual(text):
    pos_score = sum(1 for word in KEYWORD_MAP['positive'] if word in text)
    neg_score = sum(1 for word in KEYWORD_MAP['negative'] if word in text)
    
    sentiment = "bad" if neg_score > pos_score else "good"

    detected_categories = {}
    for cat in ["service", "price", "atmosphere", "location"]:
        count = sum(1 for word in KEYWORD_MAP[cat] if word in text)
        if count > 0:
            detected_categories[cat] = count
    
    category = max(detected_categories, key=detected_categories.get) if detected_categories else "food"
    
    found_keywords = []
    for key, word_list in KEYWORD_MAP.items():
        for word in word_list:
            if word in text:
                found_keywords.append(word)

    return {
        "sentiment": sentiment,
        "category": category,
        "keywords_str": ",".join(found_keywords[:5]),
        "keywords_list": found_keywords
    }

def analyze_and_load():
    print("\n--- Starting Analysis & Loading ---")
    
    if not os.path.exists(STAGED_PATH):
        return

    df = pd.read_csv(STAGED_PATH)
    print(f"Analyzing {len(df)} reviews...")
    
    analysis_results = []
    all_keywords_counter = Counter()

    for text in tqdm(df['review_text']):
        res = analyze_review_manual(text)
        analysis_results.append({
            "sentiment": res['sentiment'],
            "category": res['category'],
            "keywords": res['keywords_str']
        })
        all_keywords_counter.update(res['keywords_list'])
        
    # Save Analysis
    analysis_df = pd.DataFrame(analysis_results)
    analysis_df['review_text'] = df['review_text'].values
    analysis_df.to_csv(ANALYSIS_PATH, index=False)
    print(f"Analysis saved to {ANALYSIS_PATH}")
    
    # Save Keywords
    print("Generating Keywords Statistics...")
    keyword_data = []
    for word, freq in all_keywords_counter.most_common():
        cat_belong = "general"
        for cat, w_list in KEYWORD_MAP.items():
            if word in w_list:
                cat_belong = cat
                break
        keyword_data.append({"keyword": word, "category_type": cat_belong, "frequency": freq})
    pd.DataFrame(keyword_data).to_csv(KEYWORDS_PATH, index=False)
    print(f"Keywords stats saved to {KEYWORDS_PATH}")

    # Save Suggestions
    print("Generating Strategic Suggestions...")
    bad_reviews = analysis_df[analysis_df['sentiment'] == 'bad']
    
    if bad_reviews.empty:
        print("No bad reviews found.")
        return

    suggestion_results = []
    category_counts = bad_reviews['category'].value_counts()
    
    for category in category_counts.index:
        rules = SUGGESTION_RULES.get(category, SUGGESTION_RULES['food'])
        for rule in rules:
            suggestion_results.append({
                "category": category,
                "suggestion": rule['suggestion'],
                "severity_of_issue": rule['severity'],
                "resource_cost": rule['resources'],
                "priority_rank": rule['priority'],
                "issue_count": category_counts[category]
            })
            
    if suggestion_results:
        sug_df = pd.DataFrame(suggestion_results)
        sug_df = sug_df.sort_values(by=['issue_count', 'priority_rank'], ascending=[False, True])
        sug_df.to_csv(SUGGESTION_PATH, index=False)
        print(f"Strategic Suggestions saved to {SUGGESTION_PATH}")
