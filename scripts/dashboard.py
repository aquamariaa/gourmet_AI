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
st.markdown("Automated analysis of Wongnai restaurant reviews.")

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
    
    # --- TABS LAYOUT (Added "Overview" as first tab) ---
    tab_overview, tab_strategy, tab_analysis, tab_keywords = st.tabs([
        "🌍 Overview", 
        "📊 Strategic Plan", 
        "💬 Review Analysis", 
        "🔑 Keyword Trends"
    ])

    # ==========================================
    # TAB 1: OVERVIEW (The Big Picture)
    # ==========================================
    with tab_overview:
        st.header("Executive Summary")
        
        # --- Top Metrics Row ---
        col1, col2, col3, col4 = st.columns(4)
        total_reviews = len(df_analysis)
        sentiment_counts = df_analysis['sentiment'].value_counts()
        good_pct = (sentiment_counts.get('good', 0) / total_reviews * 100) if total_reviews else 0
        top_issue = df_suggestions.iloc[0]['category'] if not df_suggestions.empty else "None"
        
        col1.metric("Total Reviews", f"{total_reviews:,}")
        col2.metric("Satisfaction Score", f"{good_pct:.1f}%")
        col3.metric("Critical Pain Point", top_issue.title(), delta="Needs Fix", delta_color="inverse")
        col4.metric("Pipeline Status", "Active", "Updated Just Now")
        
        st.markdown("---")
        
        # --- Split View: Sentiment vs Issues ---
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("1. How do people feel?")
            fig_pie_mini = px.pie(df_analysis, names='sentiment', 
                             color='sentiment', 
                             color_discrete_map={'good':'#00cc96', 'bad':'#EF553B'},
                             hole=0.5, height=350)
            st.plotly_chart(fig_pie_mini, width='stretch')
            
        with c2:
            st.subheader("2. What are the problems?")
            # Quick aggregate for the bar chart
            chart_data = df_suggestions.groupby("category", as_index=False)["issue_count"].sum()
            fig_bar_mini = px.bar(chart_data, x="issue_count", y="category", orientation='h',
                                  text_auto=True, height=350)
            fig_bar_mini.update_traces(marker_color='#1F77B4')
            st.plotly_chart(fig_bar_mini, width='stretch')

        # --- Quick Keyword Glance ---
        st.subheader("3. Top Keywords")
        top_5_keywords = df_keywords.head(5)['keyword'].tolist()
        st.info(f"Most talked about: **{', '.join(top_5_keywords)}**")

    # ==========================================
    # TAB 2: STRATEGIC SUGGESTIONS
    # ==========================================
    with tab_strategy:
        st.header("🚀 Actionable Business Strategy")
        
        if df_suggestions.empty:
            st.success("No critical issues found! Keep up the good work.")
        else:
            if 'suggestion_idx' not in st.session_state:
                st.session_state.suggestion_idx = 0
            
            idx = st.session_state.suggestion_idx
            total_items = len(df_suggestions)
            row = df_suggestions.iloc[idx]

            progress = (idx + 1) / total_items
            st.progress(progress, text=f"Strategy Card {idx + 1} of {total_items}")

            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.subheader(f"📂 {row['category'].title()}")
                with c2:
                    p_rank = row['priority_rank']
                    p_color = "red" if p_rank == 1 else "orange" if p_rank == 2 else "green"
                    st.markdown(f":{p_color}[**Priority #{p_rank}**]")

                st.divider()
                st.markdown(f"### 💡 {row['suggestion']}")
                st.write("") 

                m1, m2, m3 = st.columns(3)
                m1.metric("Severity", row['severity_of_issue'])
                m2.metric("Est. Cost", row['resource_cost'])
                m3.metric("Customer Complaints", f"{row['issue_count']} reports")

            col_prev, col_info, col_next = st.columns([1, 5, 1])
            with col_prev:
                if st.button("⬅️ Prev", width='stretch'):
                    if st.session_state.suggestion_idx > 0:
                        st.session_state.suggestion_idx -= 1
                        st.rerun()
            with col_info:
                st.caption(f"Showing suggestion {idx + 1} / {total_items}")
            with col_next:
                if st.button("Next ➡️", width='stretch'):
                    if st.session_state.suggestion_idx < total_items - 1:
                        st.session_state.suggestion_idx += 1
                        st.rerun()

            st.divider()
            st.caption("Overview of all issues")
            
            # Group by category for single color bars
            chart_data = df_suggestions.groupby("category", as_index=False)["issue_count"].sum()
            fig_severity = px.bar(chart_data, x="category", y="issue_count",
                                  title="Complaints Breakdown", text_auto=True, height=300)
            fig_severity.update_traces(marker_color='#1F77B4')
            st.plotly_chart(fig_severity, width='stretch')

    # ==========================================
    # TAB 3: DEEP DIVE ANALYSIS
    # ==========================================
    with tab_analysis:
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.subheader("Sentiment Distribution")
            fig_pie = px.pie(df_analysis, names='sentiment', hole=0.4, 
                             color='sentiment', color_discrete_map={'good':'#00cc96', 'bad':'#EF553B'})
            st.plotly_chart(fig_pie, width='stretch')
            
            st.markdown("---")
            st.subheader("Filter Data")
            cat_filter = st.multiselect("Filter by Category", options=df_analysis['category'].unique())
            sent_filter = st.radio("Filter by Sentiment", ["All", "good", "bad"], horizontal=True)

        with col_right:
            st.subheader("Review Explorer")
            filtered_df = df_analysis.copy()
            if cat_filter:
                filtered_df = filtered_df[filtered_df['category'].isin(cat_filter)]
            if sent_filter != "All":
                filtered_df = filtered_df[filtered_df['sentiment'] == sent_filter]
            
            st.dataframe(
                filtered_df[['sentiment', 'category', 'keywords', 'review_text']], 
                height=600, 
                width='stretch'
            )

    # ==========================================
    # TAB 4: KEYWORDS
    # ==========================================
    with tab_keywords:
        st.header("What are people saying?")
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            st.subheader("Top Frequent Words")
            top_n = st.slider("Number of words", 5, 50, 20)
            st.bar_chart(df_keywords.set_index('keyword')['frequency'].head(top_n))
            
        with col_k2:
            st.subheader("Keyword Categories")
            fig_tree = px.treemap(df_keywords.head(50), path=['category_type', 'keyword'], values='frequency',
                                  title="Keyword Hierarchy (Top 50)")
            st.plotly_chart(fig_tree, width='stretch')