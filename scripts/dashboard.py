import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Config
st.set_page_config(
    page_title="Gourmet AI - Insights",
    page_icon="🍽️",
    layout="wide"
)

# Constants
ANALYSIS_PATH = "data/results/analysis.csv"
KEYWORDS_PATH = "data/results/keywords.csv"
SUGGESTION_PATH = "data/results/suggestion.csv"

# Title
st.title("🍽️ Gourmet AI: Restaurant Insights Dashboard")
st.markdown("Automated analysis of Wongnai restaurant reviews using **ELT Pipeline** & **Rule-Based Logic**.")

def load_data():
    """Loads data safely."""
    if not os.path.exists(ANALYSIS_PATH):
        st.error("❌ Data not found! Please run the pipeline first.")
        return None, None, None
    
    df_analysis = pd.read_csv(ANALYSIS_PATH)
    df_keywords = pd.read_csv(KEYWORDS_PATH)
    df_suggestions = pd.read_csv(SUGGESTION_PATH)
    return df_analysis, df_keywords, df_suggestions

# Load Data
df_analysis, df_keywords, df_suggestions = load_data()

if df_analysis is not None:
    # --- TOP METRICS ROW ---
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    total_reviews = len(df_analysis)
    sentiment_counts = df_analysis['sentiment'].value_counts()
    good_pct = (sentiment_counts.get('good', 0) / total_reviews * 100)
    top_issue = df_suggestions.iloc[0]['category'] if not df_suggestions.empty else "None"
    
    col1.metric("Total Reviews Analyzed", f"{total_reviews:,}")
    col2.metric("Customer Satisfaction", f"{good_pct:.1f}%", help="% of Good Reviews")
    col3.metric("Critical Issue", top_issue.title(), delta="Needs Attention", delta_color="inverse")
    col4.metric("Pipeline Status", "Active", "Updated Just Now")
    
    st.divider()

    # --- TABS LAYOUT ---
    tab1, tab2, tab3 = st.tabs(["📊 Strategic Plan", "💬 Review Analysis", "🔑 Keyword Trends"])

    # TAB 1: STRATEGIC SUGGESTIONS (The "Consultant" Slider View)
    with tab1:
        st.header("🚀 Actionable Business Strategy")
        
        if df_suggestions.empty:
            st.success("No critical issues found! Keep up the good work.")
        else:
            # 1. Initialize Session State for the Slider Index
            if 'suggestion_idx' not in st.session_state:
                st.session_state.suggestion_idx = 0
            
            # Helper: Get current data
            idx = st.session_state.suggestion_idx
            total_items = len(df_suggestions)
            row = df_suggestions.iloc[idx]

            # 2. Progress Bar
            progress = (idx + 1) / total_items
            st.progress(progress, text=f"Strategy Card {idx + 1} of {total_items}")

            # 3. The "Card" Container
            with st.container(border=True):
                # Header: Category & Priority Badge
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.subheader(f"📂 {row['category'].title()}")
                with c2:
                    # Dynamic color for priority
                    p_rank = row['priority_rank']
                    p_color = "red" if p_rank == 1 else "orange" if p_rank == 2 else "green"
                    st.markdown(f":{p_color}[**Priority #{p_rank}**]")

                st.divider()

                # Main Suggestion Text
                st.markdown(f"### 💡 {row['suggestion']}")
                
                st.write("") # Spacer

                # Context Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Severity", row['severity_of_issue'], help="How critical is this problem?")
                m2.metric("Est. Cost", row['resource_cost'], help="Resources needed to fix it")
                m3.metric("Customer Complaints", f"{row['issue_count']} reports")

            # 4. Navigation Buttons (Previous / Next)
            col_prev, col_info, col_next = st.columns([1, 5, 1])
            
            with col_prev:
                if st.button("⬅️ Prev", use_container_width=True):
                    if st.session_state.suggestion_idx > 0:
                        st.session_state.suggestion_idx -= 1
                        st.rerun()

            with col_info:
                st.caption(f"Showing suggestion {idx + 1} / {total_items}")

            with col_next:
                if st.button("Next ➡️", use_container_width=True):
                    if st.session_state.suggestion_idx < total_items - 1:
                        st.session_state.suggestion_idx += 1
                        st.rerun()

            # Optional: Keep the chart below the slider for big picture context
            st.divider()
            st.caption("Overview of all issues")
            fig_severity = px.bar(df_suggestions, x="category", y="issue_count", color="severity_of_issue", 
                                  title="Complaints Breakdown", text_auto=True, height=300)
            st.plotly_chart(fig_severity, use_container_width=True)

    # TAB 2: DEEP DIVE ANALYSIS
    with tab2:
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.subheader("Sentiment Distribution")
            fig_pie = px.pie(df_analysis, names='sentiment', title='Good vs Bad Reviews', hole=0.4, 
                             color='sentiment', color_discrete_map={'good':'#00cc96', 'bad':'#EF553B'})
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("Filter Data")
            cat_filter = st.multiselect("Filter by Category", options=df_analysis['category'].unique())
            sent_filter = st.radio("Filter by Sentiment", ["All", "good", "bad"], horizontal=True)

        with col_right:
            st.subheader("Review Explorer")
            # Filtering logic
            filtered_df = df_analysis.copy()
            if cat_filter:
                filtered_df = filtered_df[filtered_df['category'].isin(cat_filter)]
            if sent_filter != "All":
                filtered_df = filtered_df[filtered_df['sentiment'] == sent_filter]
            
            st.dataframe(filtered_df[['sentiment', 'category', 'keywords', 'review_text']], height=500, use_container_width=True)

    # TAB 3: KEYWORDS
    with tab3:
        st.header("What are people saying?")
        
        # Split into Positive vs Negative keywords based on our manual map categories if possible, 
        # or just visualize the raw frequency
        
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            st.subheader("Top Frequent Words")
            top_n = st.slider("Number of words", 5, 50, 20)
            
            # Simple bar chart
            st.bar_chart(df_keywords.set_index('keyword')['frequency'].head(top_n))
            
        with col_k2:
            st.subheader("Keyword Categories")
            fig_tree = px.treemap(df_keywords.head(50), path=['category_type', 'keyword'], values='frequency',
                                  title="Keyword Hierarchy (Top 50)")
            st.plotly_chart(fig_tree, use_container_width=True)