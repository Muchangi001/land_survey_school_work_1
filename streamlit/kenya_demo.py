import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go

# Set page config FIRST
st.set_page_config(
    page_title="Kenya Coordinate Converter",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #006600 0%, #009900 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #006600;
    }
</style>
""", unsafe_allow_html=True)


class PolarCoordinate:
    """Represents a coordinate in polar system (distance, angle)"""
    def __init__(self, distance: float, angle: float):
        if distance < 0:
            raise ValueError("Distance must be non-negative")
        self.distance = distance
        self.angle = angle
   
    def __str__(self):
        return f"Distance: {self.distance:.4f}m, Angle: {self.angle:.4f}°"


class RectangularCoordinate:
    """Represents a coordinate in rectangular system (northing, easting)"""
    def __init__(self, northing: float, easting: float):
        self.northing = northing
        self.easting = easting
    
    def __str__(self):
        return f"Northing: {self.northing:.4f}m, Easting: {self.easting:.4f}m"


def polar_to_rect(coord: PolarCoordinate) -> RectangularCoordinate:
    """Convert polar coordinates to rectangular coordinates"""
    angle_rad = math.radians(coord.angle)
    northing = coord.distance * math.cos(angle_rad)
    easting = coord.distance * math.sin(angle_rad)
    return RectangularCoordinate(northing, easting)


def rect_to_polar(coord: RectangularCoordinate) -> PolarCoordinate:
    """Convert rectangular coordinates to polar coordinates"""
    distance = math.sqrt(coord.northing ** 2 + coord.easting ** 2)
    angle_rad = math.atan2(coord.easting, coord.northing)
    angle_deg = math.degrees(angle_rad)
    # Normalize angle to 0-360 range
    if angle_deg < 0:
        angle_deg += 360
    return PolarCoordinate(distance, angle_deg)


def create_coordinate_plot(northing, easting, distance, angle, mode):
    """Create an interactive plot showing the coordinate system"""
    
    # Create figure
    fig = go.Figure()
    
    # Add grid lines
    max_val = max(abs(northing), abs(easting), distance) * 1.2
    if max_val == 0:
        max_val = 100
    
    # Add axes
    fig.add_trace(go.Scatter(
        x=[-max_val, max_val], y=[0, 0],
        mode='lines',
        line=dict(color='gray', width=1, dash='dash'),
        name='Easting Axis',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[-max_val, max_val],
        mode='lines',
        line=dict(color='gray', width=1, dash='dash'),
        name='Northing Axis',
        showlegend=False
    ))
    
    # Add polar angle arc if converting from polar
    if mode == "polar":
        angle_rad = math.radians(angle)
        arc_angles = [math.radians(i) for i in range(0, int(angle) + 1)]
        arc_radius = distance * 0.3
        arc_x = [arc_radius * math.sin(a) for a in arc_angles]
        arc_y = [arc_radius * math.cos(a) for a in arc_angles]
        
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y,
            mode='lines',
            line=dict(color='orange', width=2),
            name=f'Angle: {angle:.2f}°'
        ))
    
    # Add line from origin to point
    fig.add_trace(go.Scatter(
        x=[0, easting], y=[0, northing],
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=[8, 12], color=['green', 'red']),
        name=f'Distance: {distance:.2f}m',
        text=['Origin', 'Point'],
        textposition='top center'
    ))
    
    # Add the point
    fig.add_trace(go.Scatter(
        x=[easting], y=[northing],
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='circle'),
        text=[f'({northing:.2f}, {easting:.2f})'],
        textposition='top right',
        name='Target Point',
        showlegend=False
    ))
    
    # Add origin marker
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        marker=dict(size=12, color='green', symbol='circle'),
        text=['Origin (0, 0)'],
        textposition='bottom center',
        name='Origin',
        showlegend=False
    ))
    
    # Add directional labels
    label_offset = max_val * 0.9
    fig.add_annotation(x=0, y=label_offset, text="N", showarrow=False, font=dict(size=16, color="blue"))
    fig.add_annotation(x=label_offset, y=0, text="E", showarrow=False, font=dict(size=16, color="blue"))
    fig.add_annotation(x=0, y=-label_offset, text="S", showarrow=False, font=dict(size=16, color="blue"))
    fig.add_annotation(x=-label_offset, y=0, text="W", showarrow=False, font=dict(size=16, color="blue"))
    
    # Update layout
    fig.update_layout(
        title="Coordinate Visualization",
        xaxis_title="Easting (m)",
        yaxis_title="Northing (m)",
        hovermode='closest',
        height=600,
        showlegend=True,
        xaxis=dict(scaleanchor="y", scaleratio=1, zeroline=True, gridcolor='lightgray'),
        yaxis=dict(scaleanchor="x", scaleratio=1, zeroline=True, gridcolor='lightgray'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig


# Header
st.markdown('<div class="main-header"><h1>🇰🇪 Kenya Coordinate Converter</h1><p>Professional Surveying Tool for Coordinate Transformation</p></div>', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["🔄 Converter", "📊 Batch Processing", "ℹ️ Help"])

with tab1:
    # System selection
    col_radio1, col_radio2 = st.columns(2)
    with col_radio1:
        system = st.radio(
            "Select Conversion Direction:",
            ["Polar → Rectangular", "Rectangular → Polar"],
            horizontal=False
        )
    
    st.divider()
    
    if system == "Polar → Rectangular":
        st.subheader("📐 Polar to Rectangular Conversion")
        
        col1, col2 = st.columns(2)
        with col1:
            distance = st.number_input(
                "Distance (meters)", 
                value=100.0, 
                step=0.1, 
                format="%.4f",
                help="Enter the radial distance from origin",
                key="polar_distance"
            )
        with col2:
            angle = st.number_input(
                "Angle (degrees)", 
                value=45.0, 
                step=0.1, 
                format="%.4f",
                help="Enter the angle measured clockwise from North (0-360°)",
                key="polar_angle"
            )
        
        # Normalize angle
        angle = angle % 360
        
        if st.button("🔄 Convert to Rectangular", type="primary", use_container_width=True, key="btn_polar_to_rect"):
            try:
                polar_coord = PolarCoordinate(distance, angle)
                rect_coord = polar_to_rect(polar_coord)
                
                st.success("✅ Conversion Complete!")
                
                # Results in columns
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("### 📥 Input (Polar)")
                    st.info(f"**Distance:** {distance:.4f} m\n\n**Angle:** {angle:.4f}°")
                
                with res_col2:
                    st.markdown("### 📤 Output (Rectangular)")
                    st.success(f"**Northing:** {rect_coord.northing:.4f} m\n\n**Easting:** {rect_coord.easting:.4f} m")
                
                # Visualization
                st.divider()
                st.markdown("### 📍 Coordinate Visualization")
                fig = create_coordinate_plot(rect_coord.northing, rect_coord.easting, distance, angle, "polar")
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional information
                with st.expander("📋 Detailed Information"):
                    quadrant = ""
                    if rect_coord.northing >= 0 and rect_coord.easting >= 0:
                        quadrant = "NE (First Quadrant)"
                    elif rect_coord.northing >= 0 and rect_coord.easting < 0:
                        quadrant = "NW (Second Quadrant)"
                    elif rect_coord.northing < 0 and rect_coord.easting < 0:
                        quadrant = "SW (Third Quadrant)"
                    else:
                        quadrant = "SE (Fourth Quadrant)"
                    
                    bearing = angle
                    if bearing > 90 and bearing <= 180:
                        bearing_text = f"S {180 - bearing:.2f}° E"
                    elif bearing > 180 and bearing <= 270:
                        bearing_text = f"S {bearing - 180:.2f}° W"
                    elif bearing > 270:
                        bearing_text = f"N {360 - bearing:.2f}° W"
                    else:
                        bearing_text = f"N {bearing:.2f}° E"
                    
                    st.write(f"**Quadrant:** {quadrant}")
                    st.write(f"**Bearing:** {bearing_text}")
                    st.write(f"**Angle from North:** {angle:.4f}°")
                    
            except ValueError as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif system == "Rectangular → Polar":
        st.subheader("📏 Rectangular to Polar Conversion")
        
        col1, col2 = st.columns(2)
        with col1:
            northing = st.number_input(
                "Northing (meters)", 
                value=70.71, 
                step=0.1, 
                format="%.4f",
                help="Enter the northing coordinate (Y-axis)",
                key="rect_northing"
            )
        with col2:
            easting = st.number_input(
                "Easting (meters)", 
                value=70.71, 
                step=0.1, 
                format="%.4f",
                help="Enter the easting coordinate (X-axis)",
                key="rect_easting"
            )
        
        if st.button("🔄 Convert to Polar", type="primary", use_container_width=True, key="btn_rect_to_polar"):
            try:
                rect_coord = RectangularCoordinate(northing, easting)
                polar_coord = rect_to_polar(rect_coord)
                
                st.success("✅ Conversion Complete!")
                
                # Results in columns
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("### 📥 Input (Rectangular)")
                    st.info(f"**Northing:** {northing:.4f} m\n\n**Easting:** {easting:.4f} m")
                
                with res_col2:
                    st.markdown("### 📤 Output (Polar)")
                    st.success(f"**Distance:** {polar_coord.distance:.4f} m\n\n**Angle:** {polar_coord.angle:.4f}°")
                
                # Visualization
                st.divider()
                st.markdown("### 📍 Coordinate Visualization")
                fig = create_coordinate_plot(northing, easting, polar_coord.distance, polar_coord.angle, "rect")
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional information
                with st.expander("📋 Detailed Information"):
                    quadrant = ""
                    if northing >= 0 and easting >= 0:
                        quadrant = "NE (First Quadrant)"
                    elif northing >= 0 and easting < 0:
                        quadrant = "NW (Second Quadrant)"
                    elif northing < 0 and easting < 0:
                        quadrant = "SW (Third Quadrant)"
                    else:
                        quadrant = "SE (Fourth Quadrant)"
                    
                    angle = polar_coord.angle
                    if angle > 90 and angle <= 180:
                        bearing_text = f"S {180 - angle:.2f}° E"
                    elif angle > 180 and angle <= 270:
                        bearing_text = f"S {angle - 180:.2f}° W"
                    elif angle > 270:
                        bearing_text = f"N {360 - angle:.2f}° W"
                    else:
                        bearing_text = f"N {angle:.2f}° E"
                    
                    st.write(f"**Quadrant:** {quadrant}")
                    st.write(f"**Bearing:** {bearing_text}")
                    st.write(f"**Horizontal Distance:** {polar_coord.distance:.4f} m")
                    
            except ValueError as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("📊 Batch Coordinate Processing")
    st.write("Process multiple coordinates at once")
    
    batch_system = st.radio(
        "Select batch conversion type:",
        ["Polar → Rectangular", "Rectangular → Polar"],
        key="batch_radio"
    )
    
    if batch_system == "Polar → Rectangular":
        st.write("Enter polar coordinates (Distance, Angle) - one per line:")
        batch_input = st.text_area(
            "Batch Input",
            placeholder="100.0, 45.0\n150.0, 90.0\n200.0, 135.0",
            height=150
        )
        
        if st.button("Process Batch", type="primary", key="batch_polar_btn"):
            if batch_input.strip():
                results = []
                lines = batch_input.strip().split('\n')
                
                for i, line in enumerate(lines, 1):
                    try:
                        parts = line.split(',')
                        if len(parts) == 2:
                            dist = float(parts[0].strip())
                            ang = float(parts[1].strip()) % 360
                            polar = PolarCoordinate(dist, ang)
                            rect = polar_to_rect(polar)
                            results.append({
                                'Row': i,
                                'Distance (m)': dist,
                                'Angle (°)': ang,
                                'Northing (m)': rect.northing,
                                'Easting (m)': rect.easting
                            })
                    except Exception as e:
                        st.warning(f"⚠️ Error in line {i}: {line}")
                
                if results:
                    df = pd.DataFrame(results)
                    st.success(f"✅ Processed {len(results)} coordinates")
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results as CSV",
                        csv,
                        "polar_to_rect_results.csv",
                        "text/csv",
                        key="download_polar"
                    )
            else:
                st.warning("⚠️ No valid coordinates to process")
    
    elif batch_system == "Rectangular → Polar":
        st.write("Enter rectangular coordinates (Northing, Easting) - one per line:")
        batch_input = st.text_area(
            "Batch Input",
            placeholder="70.71, 70.71\n0, 150\n-100, 100",
            height=150
        )
        
        if st.button("Process Batch", type="primary", key="batch_rect_btn"):
            if batch_input.strip():
                results = []
                lines = batch_input.strip().split('\n')
                
                for i, line in enumerate(lines, 1):
                    try:
                        parts = line.split(',')
                        if len(parts) == 2:
                            north = float(parts[0].strip())
                            east = float(parts[1].strip())
                            rect = RectangularCoordinate(north, east)
                            polar = rect_to_polar(rect)
                            results.append({
                                'Row': i,
                                'Northing (m)': north,
                                'Easting (m)': east,
                                'Distance (m)': polar.distance,
                                'Angle (°)': polar.angle
                            })
                    except Exception as e:
                        st.warning(f"⚠️ Error in line {i}: {line}")
                
                if results:
                    df = pd.DataFrame(results)
                    st.success(f"✅ Processed {len(results)} coordinates")
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results as CSV",
                        csv,
                        "rect_to_polar_results.csv",
                        "text/csv",
                        key="download_rect"
                    )
            else:
                st.warning("⚠️ No valid coordinates to process")

with tab3:
    st.subheader("ℹ️ Help & Information")
    
    st.markdown("""
    ### 📖 About This Tool
    This coordinate converter is designed for Kenyan surveyors and engineers to transform coordinates between:
    - **Polar Coordinates**: Distance and angle from origin
    - **Rectangular Coordinates**: Northing (Y) and Easting (X) values
    
    ### 🧭 Coordinate Systems
    
    #### Polar Coordinates (Distance, Angle)
    - **Distance**: Radial distance from the origin point (in meters)
    - **Angle**: Measured clockwise from North (0°) in degrees
        - 0° = North
        - 90° = East
        - 180° = South
        - 270° = West
    
    #### Rectangular Coordinates (Northing, Easting)
    - **Northing**: Y-coordinate, positive towards North
    - **Easting**: X-coordinate, positive towards East
    
    ### 📐 Conversion Formulas
    
    **Polar → Rectangular:**
    ```
    Northing = Distance × cos(Angle)
    Easting = Distance × sin(Angle)
    ```
    
    **Rectangular → Polar:**
    ```
    Distance = √(Northing² + Easting²)
    Angle = atan2(Easting, Northing)
    ```
    
    ### 💡 Usage Tips
    - Use the batch processing tab for multiple coordinates
    - All angles are normalized to 0-360° range
    - Negative coordinates are supported
    - Download results as CSV for further processing
    
    ### 🎯 Common Use Cases
    - Traverse calculations
    - Setting out coordinates
    - Boundary surveys
    - Construction layout
    - Topographic surveys
    
    ### ⚠️ Notes
    - Ensure input units are consistent (meters)
    - Angles are in decimal degrees
    - Distance values must be non-negative
    """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🇰🇪 Built for Kenyan Surveying")
with col2:
    st.caption("📍 Professional Coordinate Tools")
with col3:
    st.caption("v1.0")