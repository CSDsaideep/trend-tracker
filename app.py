import streamlit as st
import pandas as pd
import plotly.express as px
import os
from trend_tracker import TrendTrackerEngine

st.set_page_config(page_title="Trend Tracker Live Dashboard", layout="wide")

st.title("📊 Trend Tracker: Real-Time Product Popularity Analytics")
st.markdown("Automated streaming pipeline utilizing rolling Z-Score transformations to isolate viral consumer demand spikes.")

@st.cache_data(ttl=10) # Refresh data states every 10 seconds
def run_analytics_pipeline():
    file_path = 'data/raw_transactions.csv'
    if not os.path.exists(file_path):
        from generate_data import generate_synthetic_transactions
        generate_synthetic_transactions(1200)
        
    engine = TrendTrackerEngine(alert_threshold_z=2.0)
    engine.load_and_clean_data(file_path)
    return engine.compute_trending_metrics()

try:
    df_metrics = run_analytics_pipeline()
    
    st.sidebar.header("Pipeline Configurations")
    z_slider = st.sidebar.slider("Z-Score Sensitivity Threshold", 1.0, 3.5, 2.0, step=0.1)
    
    df_metrics['status'] = ['TRENDING_SPIKE' if z >= z_slider else 'STABLE' for z in df_metrics['trend_index_z']]
    
    trending_count = len(df_metrics[df_metrics['status'] == 'TRENDING_SPIKE'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Unique Products Monitored", value=len(df_metrics))
    with col2:
        st.metric(label="System Detected Viral Spikes", value=trending_count, 
                  delta=f"{trending_count} active alerts", delta_color="inverse" if trending_count > 0 else "normal")
    with col3:
        st.metric(label="Max Z-Score Observed", value=f"{df_metrics['trend_index_z'].max():.2f}")

    st.subheader("📈 Real-Time Product Popularity Index Mapping")
    
    fig = px.bar(
        df_metrics.head(15),
        x='product_id',
        y='trend_index_z',
        color='status',
        color_discrete_map={'TRENDING_SPIKE': '#EF553B', 'STABLE': '#636EFA'},
        labels={'trend_index_z': 'Popularity Score (Z-Score)', 'product_id': 'Product ID'},
        title="Top 15 Products Evaluated Across Current Execution Window"
    )
    fig.add_hline(y=z_slider, line_dash="dash", line_color="red", annotation_text="Anomaly Alert Threshold")
    st.plotly_chart(fig, use_container_width=True)

    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("🔥 Active Trending Alerts")
        trending_items = df_metrics[df_metrics['status'] == 'TRENDING_SPIKE']
        if not trending_items.empty:
            st.dataframe(
                trending_items[['product_id', 'category', 'total_sales_volume', 'trend_index_z']], 
                use_container_width=True, hide_index=True
            )
        else:
            st.info("All tracked product streams are operating within stable baseline standard deviations.")
            
    with right_col:
        st.subheader("📦 Category Volume Share")
        cat_fig = px.pie(
            df_metrics, 
            values='total_sales_volume', 
            names='category', 
            hole=0.4,
            title="Total Items Processed per Retail Stream"
        )
        st.plotly_chart(cat_fig, use_container_width=True)

except Exception as e:
    st.error(f"Pipeline Connection Interrupted: {e}")
