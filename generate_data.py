import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_transactions(num_records=1200):
    print(f"Generating {num_records} realistic transactional logs...")
    np.random.seed(42)
    

    products = [f"PROD_{i:03d}" for i in range(1, 51)]
    categories = {
        'Electronics': [f"PROD_{i:03d}" for i in range(1, 11)],
        'Home Utility': [f"PROD_{i:03d}" for i in range(11, 25)],
        'Mobile Accessories': [f"PROD_{i:03d}" for i in range(25, 40)],
        'Audio Equipment': [f"PROD_{i:03d}" for i in range(40, 51)]
    }
    
    prod_to_cat = {}
    for cat, prod_list in categories.items():
        for p in prod_list:
            prod_to_cat[p] = cat

    base_time = datetime.now()
    records = []

    for i in range(num_records):
        pid = np.random.choice(products)
        timestamp = base_time - timedelta(minutes=np.random.randint(0, 240)) # Spanning past 4 hours
        quantity = int(np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05]))
        price = float(np.random.randint(150, 6000))
        
        records.append({
            'transaction_id': f"TX_{20000 + i}",
            'product_id': pid,
            'category': prod_to_cat[pid],
            'price': price,
            'timestamp': timestamp,
            'quantity': quantity
        })

    print("Injecting simulated trending anomaly spike for PROD_042...")
    for j in range(85):
        timestamp = base_time - timedelta(minutes=np.random.randint(0, 30))
        records.append({
            'transaction_id': f"TX_SPIKE_{100 + j}",
            'product_id': 'PROD_042',
            'category': 'Audio Equipment',
            'price': 2499.0,
            'timestamp': timestamp,
            'quantity': int(np.random.randint(2, 6)) # Larger purchasing quantities
        })

    df = pd.DataFrame(records)
    
    mask = np.random.rand(*df.shape) < 0.01 # 1% missing value rate
    df.loc[mask['price'], 'price'] = np.nan
    
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/raw_transactions.csv'
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created and exported to: {output_path}")

if __name__ == "__main__":
    generate_synthetic_transactions(1200)
