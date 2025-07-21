#!/usr/bin/env python3
"""
Test script for the beacon temperature schematic function
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Import the function from our main app
import sys
sys.path.append('.')

def test_beacon_schematic():
    """Test the beacon temperature schematic with sample data"""
    
    # Create sample data
    np.random.seed(42)
    beacons = [f"Beacon_{i:02d}" for i in range(1, 25)]  # 24 beacons
    
    # Generate sample data over 2 days
    start_time = datetime(2024, 1, 1, 10, 0, 0)
    end_time = datetime(2024, 1, 1, 18, 0, 0)
    
    data = []
    for beacon in beacons:
        for hour in range(8):  # 8 hours of data
            timestamp = start_time + timedelta(hours=hour)
            # Simulate different temperature patterns
            base_temp = 115 + np.random.normal(0, 20)  # Around target with variation
            temp = base_temp + np.random.normal(0, 5)  # Some noise
            
            data.append({
                'DateTime': timestamp,
                'BeaconDescription': beacon,
                'ExternalSensorTemperature': temp,
                'ExternalSensorTemperatureExt1': temp + np.random.normal(0, 2),
                'RSSI': np.random.randint(-90, -60)
            })
    
    df = pd.DataFrame(data)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    
    print(f"Created sample data with {len(df)} records for {len(beacons)} beacons")
    print(f"Temperature range: {df['ExternalSensorTemperature'].min():.1f}°C to {df['ExternalSensorTemperature'].max():.1f}°C")
    
    # Test the schematic function
    try:
        from beacon_analyzer_app import create_beacon_temperature_schematic
        
        fig, error = create_beacon_temperature_schematic(
            df, 
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time.strftime('%Y-%m-%d %H:%M:%S'),
            target_temp=115
        )
        
        if error:
            print(f"Error: {error}")
            return False
        elif fig:
            print("✅ Schematic created successfully!")
            plt.show()
            return True
        else:
            print("❌ No figure returned")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating schematic: {e}")
        return False

if __name__ == "__main__":
    test_beacon_schematic()
