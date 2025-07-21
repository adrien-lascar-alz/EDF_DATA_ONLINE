
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import tempfile
import os

# Page config
st.set_page_config(
    page_title="Beacon Data Analyzer", 
    page_icon="📡", 
    layout="wide"
)

def get_beacons_from_db(db_path):
    """Get list of available beacons from database"""
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT DISTINCT beacon.Description FROM Beacon beacon ORDER BY beacon.Description"
        beacons = pd.read_sql_query(query, conn)
        conn.close()
        return beacons['Description'].tolist()
    except Exception as e:
        st.error(f"Error reading beacons from database: {e}")
        return []

def get_date_range_from_db(db_path):
    """Get min and max dates from database"""
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT MIN(DateTime) as min_date, MAX(DateTime) as max_date FROM BeaconEvent"
        result = pd.read_sql_query(query, conn)
        conn.close()
        
        min_date = pd.to_datetime(result['min_date'].iloc[0])
        max_date = pd.to_datetime(result['max_date'].iloc[0])
        return min_date, max_date
    except Exception as e:
        st.error(f"Error reading date range: {e}")
        return None, None

def get_dataframe_from_database(db_path, startup_datetime_str, cutoff_datetime_str, selected_beacons=None):
    """Get DataFrame from database with optional beacon filtering"""
    conn = sqlite3.connect(db_path)
    
    # Build query with optional beacon filtering
    beacon_filter = ""
    params = [startup_datetime_str, cutoff_datetime_str]
    
    if selected_beacons:
        beacon_placeholders = ','.join(['?' for _ in selected_beacons])
        beacon_filter = f"AND beacon.Description IN ({beacon_placeholders})"
        params.extend(selected_beacons)
    
    query = f"""
    SELECT 
        event.DateTime, 
        beacon.Description as BeaconDescription,
        event.ExternalSensorTemperature,
        event.ExternalSensorTemperatureExt1,
        event.RSSI
    FROM BeaconEvent event
    INNER JOIN Beacon beacon ON event.BeaconId = beacon.Id
    WHERE event.DateTime BETWEEN ? AND ? {beacon_filter}
    ORDER BY event.DateTime
    """
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df

def create_interactive_plot(df, beacon, time_window):
    """Create interactive Plotly plot for a beacon"""
    beacon_data = df[df['BeaconDescription'] == beacon].copy()
    
    if beacon_data.empty:
        return None
    
    beacon_data.set_index('DateTime', inplace=True)
    
    # Resample data
    temp_resampled = beacon_data['ExternalSensorTemperature'].resample(time_window).mean()
    temp_ext1_resampled = beacon_data['ExternalSensorTemperatureExt1'].resample(time_window).mean()
    rssi_median = beacon_data['RSSI'].resample(time_window).median()
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add temperature traces
    fig.add_trace(
        go.Scatter(
            x=temp_resampled.index, 
            y=temp_resampled.values,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='blue'),
            marker=dict(size=4)
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=temp_ext1_resampled.index, 
            y=temp_ext1_resampled.values,
            mode='lines+markers',
            name='Temperature Ext1 (°C)',
            line=dict(color='green'),
            marker=dict(size=4, symbol='square')
        ),
        secondary_y=False,
    )
    
    # Add RSSI trace
    fig.add_trace(
        go.Scatter(
            x=rssi_median.index, 
            y=rssi_median.values,
            mode='markers',
            name='RSSI Median',
            line=dict(color='red'),
            marker=dict(size=4)
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Temperature (°C)", range=[20, 125], secondary_y=False)
    fig.update_yaxes(title_text="RSSI (dBm)", range=[-100, -50], secondary_y=True)
    
    fig.update_layout(
        title=f'Temperature and RSSI vs Time - {beacon}',
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_beacon_temperature_schematic(df, startup_datetime_str, cutoff_datetime_str, target_temp=115):
    """Create a 3x11 grid schematic showing beacon temperatures with color coding"""
    startup_datetime = datetime.strptime(startup_datetime_str, '%Y-%m-%d %H:%M:%S')
    cutoff_datetime = datetime.strptime(cutoff_datetime_str, '%Y-%m-%d %H:%M:%S')
    filtered_df = df[(df['DateTime'] >= startup_datetime) & (df['DateTime'] <= cutoff_datetime)]
    
    if filtered_df.empty:
        return None, "No data found for the specified time range."
    
    # Get maximum temperature for each beacon instead of last
    max_temps = filtered_df.groupby('BeaconDescription')['ExternalSensorTemperature'].max().round(1)
    beacons = sorted(max_temps.index.tolist())
    
    # Create 3x11 grid
    fig, axes = plt.subplots(3, 11, figsize=(16, 8))
    fig.suptitle(f'Beacon Temperature Schematic (Max vs Target {target_temp}°C)', fontsize=16)
    
    for i in range(3):
        for j in range(11):
            ax = axes[i, j]
            beacon_idx = i * 11 + j
            
            if beacon_idx < len(beacons):
                beacon = beacons[beacon_idx]
                max_temp = max_temps[beacon]
                
                # Color coding: green if close to target, red if far
                temp_diff = abs(max_temp - target_temp)
                if temp_diff <= 5:
                    color = 'lightgreen'
                elif temp_diff <= 15:
                    color = 'yellow'
                else:
                    color = 'lightcoral'
                
                # Create colored rectangle
                rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                
                # Add text
                ax.text(0.5, 0.7, beacon, ha='center', va='center', fontweight='bold', fontsize=8)
                ax.text(0.5, 0.4, f'{max_temp}°C', ha='center', va='center', fontsize=10)
                
            else:
                # Empty cell
                ax.add_patch(patches.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='gray', facecolor='white'))
                ax.text(0.5, 0.5, 'Empty', ha='center', va='center', fontsize=8, color='gray')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
    
    # Add legend
    legend_elements = [
        patches.Patch(color='lightgreen', label=f'Within ±5°C of {target_temp}°C'),
        patches.Patch(color='yellow', label=f'Within ±15°C of {target_temp}°C'),
        patches.Patch(color='lightcoral', label=f'More than ±15°C from {target_temp}°C')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05))
    
    plt.tight_layout()
    return fig, None

# Main Streamlit app
def main():
    st.title("📡 Beacon Data Analyzer")
    st.markdown("Upload your SQLite database and analyze beacon data interactively!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Drop your SQLite database file here", 
        type=['db', 'sqlite', 'sqlite3'],
        help="Upload your EDFBeaconCaptures.db file"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
            tmp_file.write(uploaded_file.read())
            db_path = tmp_file.name
        
        try:
            # Get available beacons
            beacons = get_beacons_from_db(db_path)
            
            if not beacons:
                st.error("No beacons found in the database or error reading data.")
                return
            
            # Get date range
            min_date, max_date = get_date_range_from_db(db_path)
            
            if min_date is None or max_date is None:
                st.error("Could not determine date range from database.")
                return
            
            # Sidebar controls
            st.sidebar.header("🎛️ Controls")
            
            # Beacon selection
            selected_beacons = st.sidebar.multiselect(
                "Select Beacon(s)",
                options=beacons,
                default=beacons[:3] if len(beacons) >= 3 else beacons,
                help="Choose one or more beacons to analyze"
            )
            
            # Date range selection
            col1, col2 = st.sidebar.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start Date", 
                    value=min_date.date(),
                    min_value=min_date.date(),
                    max_value=max_date.date()
                )
            with col2:
                end_date = st.date_input(
                    "End Date", 
                    value=max_date.date(),
                    min_value=min_date.date(),
                    max_value=max_date.date()
                )
            
            # Time range selection
            col3, col4 = st.sidebar.columns(2)
            with col3:
                start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
            with col4:
                end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
            
            # Time window selection
            time_window = st.sidebar.selectbox(
                "Time Window for Resampling",
                options=['1min', '5min', '10min', '30min', '1H'],
                index=1
            )
            
            # Beacon schematic options
            st.sidebar.subheader("🌡️ Beacon Temperature Schematic")
            show_schematic = st.sidebar.checkbox("Show Temperature Schematic", value=False)
            
            if show_schematic:
                target_temp = st.sidebar.number_input(
                    "Target Temperature (°C)",
                    min_value=50,
                    max_value=150,
                    value=115,
                    help="Reference temperature for color coding"
                )
            
            # Combine date and time
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)
            
            # Analysis button
            if st.sidebar.button("🔍 Analyze Data", type="primary"):
                if not selected_beacons:
                    st.warning("Please select at least one beacon.")
                    return
                
                # Get data
                with st.spinner("Loading data from database..."):
                    df = get_dataframe_from_database(
                        db_path, 
                        start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        end_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        selected_beacons
                    )
                
                if df.empty:
                    st.warning("No data found for the selected criteria.")
                    return
                
                # Display summary
                st.success(f"✅ Found {len(df)} data points for {len(selected_beacons)} beacon(s)")
                
                # Show beacon temperature schematic if enabled
                if show_schematic:
                    st.header("🌡️ Beacon Temperature Schematic")
                    
                    with st.spinner("Creating temperature schematic..."):
                        schematic_fig, error_msg = create_beacon_temperature_schematic(
                            df, 
                            start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            end_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            target_temp
                        )
                    
                    if error_msg:
                        st.error(error_msg)
                    elif schematic_fig:
                        st.pyplot(schematic_fig)
                        
                        # Show beacon statistics summary
                        st.subheader("📊 Schematic Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        temp_data = df.groupby('BeaconDescription')['ExternalSensorTemperature'].max()
                        temp_diffs = abs(temp_data - target_temp)
                        
                        with col1:
                            green_count = len(temp_diffs[temp_diffs <= 5])
                            st.metric("🟢 Within ±5°C", green_count)
                        with col2:
                            yellow_count = len(temp_diffs[(temp_diffs > 5) & (temp_diffs <= 15)])
                            st.metric("🟡 Within ±15°C", yellow_count)
                        with col3:
                            red_count = len(temp_diffs[temp_diffs > 15])
                            st.metric("🔴 Beyond ±15°C", red_count)
                        with col4:
                            total_beacons = len(temp_data)
                            st.metric("📡 Total Beacons", total_beacons)
                        
                        # Add explanation
                        st.info(f"""
                        **Temperature Schematic Explanation:**
                        - 🟢 **Green**: Beacons within ±5°C of target ({target_temp}°C)
                        - 🟡 **Yellow**: Beacons within ±15°C of target ({target_temp}°C)  
                        - 🔴 **Red**: Beacons more than ±15°C from target ({target_temp}°C)
                        - Shows **maximum** temperature reached by each beacon in the selected time range
                        """)
                        
                        plt.close(schematic_fig)  # Free up memory
                
                # Show data summary
                with st.expander("📊 Data Summary"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", len(df))
                    with col2:
                        st.metric("Date Range", f"{len(df['DateTime'].dt.date.unique())} days")
                    with col3:
                        st.metric("Beacons", len(df['BeaconDescription'].unique()))
                    
                    st.dataframe(df.head())
                
                # Create plots for each beacon
                st.header("📈 Beacon Analysis")
                
                for beacon in selected_beacons:
                    beacon_df = df[df['BeaconDescription'] == beacon]
                    if not beacon_df.empty:
                        st.subheader(f"🎯 {beacon}")
                        
                        # Create interactive plot
                        fig = create_interactive_plot(df, beacon, time_window)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Show beacon statistics
                        with st.expander(f"Statistics for {beacon}"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "Avg Temperature", 
                                    f"{beacon_df['ExternalSensorTemperature'].mean():.1f}°C"
                                )
                            with col2:
                                st.metric(
                                    "Avg RSSI", 
                                    f"{beacon_df['RSSI'].mean():.1f} dBm"
                                )
                            with col3:
                                st.metric(
                                    "Data Points", 
                                    len(beacon_df)
                                )
        
        finally:
            # Clean up temporary file
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    else:
        st.info("👆 Please upload your SQLite database file to get started!")
        
        # Show example
        st.markdown("### 🔍 What this app does:")
        st.markdown("""
        1. **📁 Upload Database**: Drop your SQLite database file
        2. **🎯 Select Beacons**: Choose which beacons to analyze
        3. **📅 Set Time Range**: Pick date and time filters
        4. **📊 View Results**: Interactive plots and statistics
        5. **🎛️ Adjust Settings**: Change time windows and filters
        """)

if __name__ == "__main__":
    main()
