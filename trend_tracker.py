import pandas as pd
import numpy as np
import os
from datetime import datetime

class TrendTrackerEngine:
    def __init__(self, alert_threshold_z=2.0):
        self.alert_threshold_z = alert_threshold_z
        self.processed_data = pd.DataFrame()

    def load_and_clean_data(self, file_path):
        """Ingests raw tracking records and imputes missing system properties."""
        print(f"Reading pipeline input from: {file_path}")
        df = pd.read_csv(file_path)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        if df['price'].isnull().sum() > 0:
            print(f"Data Cleansing: Imputing missing price entries...")
            df['price'] = df.groupby('category')['price'].transform(lambda x: x.fillna(x.median()))
            
        self.processed_data = df
        return df

    def compute_trending_metrics(self):
        """Applies rolling Z-score mathematical models over volume states."""
        if self.processed_data.empty:
            print("Processing buffer empty. Aborting extraction metrics loop.")
            return pd.DataFrame()

        metrics_df = self.processed_data.groupby(['product_id', 'category']).agg(
            total_sales_volume=('quantity', 'sum'),
            unique_transactions=('transaction_id', 'count')
        ).reset_index()

        mean_vol = metrics_df['total_sales_volume'].mean()
        std_vol = metrics_df['total_sales_volume'].std()

        if std_vol == 0:
            std_vol = 1.0

        metrics_df['trend_index_z'] = (metrics_df['total_sales_volume'] - mean_vol) / std_vol
        
        metrics_df['status'] = np.where(
            metrics_df['trend_index_z'] >= self.alert_threshold_z, 'TRENDING_SPIKE', 'STABLE'
        )
        
        return metrics_df.sort_values(by='trend_index_z', ascending=False)

if __name__ == "__main__":
    pipeline = TrendTrackerEngine(alert_threshold_z=2.5)
    
    if not os.path.exists('data/raw_transactions.csv'):
        from generate_data import generate_synthetic_transactions
        generate_synthetic_transactions(1200)
        
    pipeline.load_and_clean_data('data/raw_transactions.csv')
    trending_analytics = pipeline.compute_trending_metrics()
    
    print("\n--- Analytics Production Output: Top 5 Detected Items ---")
    print(trending_analytics.head(5).to_string(index=False))
