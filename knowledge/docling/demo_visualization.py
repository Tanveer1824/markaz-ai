#!/usr/bin/env python3
"""
Demo script showing the enhanced visualization features
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def create_sample_data():
    """Create sample real estate data for demonstration"""
    return {
        'categories': [
            'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025'
        ],
        'values': [372.7, 385.2, 398.1, 410.5, 415.2, 420.8, 418.5, 422.1, 425.8],
        'labels': [
            'Q1 2023: 372.7', 'Q2 2023: 385.2', 'Q3 2023: 398.1', 'Q4 2023: 410.5',
            'Q1 2024: 415.2', 'Q2 2024: 420.8', 'Q3 2024: 418.5', 'Q4 2024: 422.1', 'Q1 2025: 425.8'
        ],
        'chart_type': 'line',
        'title': 'Rental Value Trends Over Time'
    }

def create_visualization(data: dict, chart_type: str = 'line') -> go.Figure:
    """Create visualization based on data and chart type"""
    if chart_type == 'line':
        fig = go.Figure(data=[
            go.Scatter(
                x=data['categories'],
                y=data['values'],
                mode='lines+markers',
                line=dict(color='rgb(55, 83, 109)', width=3),
                marker=dict(size=8)
            )
        ])
    elif chart_type == 'bar':
        fig = go.Figure(data=[
            go.Bar(
                x=data['categories'],
                y=data['values'],
                text=data['values'],
                texttemplate='%{text:,.1f}',
                textposition='outside',
                marker_color='rgb(55, 83, 109)'
            )
        ])
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=data['categories'],
                y=data['values'],
                text=data['values'],
                texttemplate='%{text:,.1f}',
                textposition='outside',
                marker_color='rgb(55, 83, 109)'
            )
        ])
    
    fig.update_layout(
        title=f"{chart_type.title()} Chart - {data['title']}",
        template="plotly_white",
        height=400,
        xaxis_title="Time Period",
        yaxis_title="Rental Values (KD)",
        showlegend=False
    )
    
    return fig

def create_data_summary_table(data: dict) -> str:
    """Create a summary table for the visualized data"""
    if not data['values']:
        return "No data available for summary."
    
    total = sum(data['values'])
    avg = total / len(data['values'])
    max_val = max(data['values'])
    min_val = min(data['values'])
    
    summary = "## 📊 Data Summary\n\n"
    summary += f"**Total Value**: KD {total:,.2f}\n\n"
    summary += f"**Average**: KD {avg:,.2f}\n\n"
    summary += f"**Range**: KD {min_val:,.2f} - KD {max_val:,.2f}\n\n"
    
    summary += "| Time Period | Value (KD) | Percentage |\n"
    summary += "|-------------|------------|------------|\n"
    
    for category, value in zip(data['categories'], data['values']):
        percentage = (value / total * 100) if total > 0 else 0
        summary += f"| {category} | {value:,.1f} | {percentage:.1f}% |\n"
    
    return summary

def main():
    st.title("📊 Enhanced Visualization Features Demo")
    st.markdown("This demo shows how the chat interface now automatically generates charts and data summaries!")
    
    # Sample data
    sample_data = create_sample_data()
    
    st.header("🎯 Example: Rental Value Trends Over Time")
    st.info("When you ask: **'Line chart of rental value trends over time'** in the chat, you'll get:")
    
    # Create and display visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Interactive Line Chart")
        fig = create_visualization(sample_data, 'line')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Chart Features")
        st.markdown("""
        - **Hover Details**: See exact values
        - **Zoom & Pan**: Interactive exploration
        - **Responsive**: Adapts to screen size
        - **Professional**: Clean, business-ready styling
        """)
    
    # Data summary table
    st.subheader("📋 Data Summary Table")
    summary_table = create_data_summary_table(sample_data)
    st.markdown(summary_table)
    
    # Show different chart types
    st.header("🎨 Multiple Chart Types Available")
    
    chart_types = ['line', 'bar']
    chart_names = ['Line Chart (Trends)', 'Bar Chart (Comparisons)']
    
    for chart_type, chart_name in zip(chart_types, chart_names):
        with st.expander(f"📊 {chart_name}"):
            fig = create_visualization(sample_data, chart_type)
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"This {chart_type} chart would be automatically generated when you request it in the chat!")
    
    # Usage examples
    st.header("💡 How to Use in Chat")
    
    st.subheader("🎯 For Trends Over Time:")
    st.code("""
"Line chart of rental value trends over time"
"Show me rental trends over time"
"Display quarterly performance trends"
"Price trends chart"
    """)
    
    st.subheader("📊 For Comparisons:")
    st.code("""
"Create a bar chart of governorate prices"
"Show me a pie chart of market segments"
"Make a bar chart of property values by region"
    """)
    
    st.subheader("🔍 For Specific Analysis:")
    st.code("""
"Rental value trends from 2023 to 2025"
"Quarterly market performance chart"
"Market segment distribution chart"
    """)
    
    # Key improvements
    st.header("🚀 Key Improvements Made")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Smart Detection
        - Automatically recognizes visualization requests
        - Distinguishes between questions and chart requests
        - Context-aware for real estate data
        
        ### 📈 Better Charts
        - Line charts for trends over time
        - Bar charts for comparisons
        - Professional styling and formatting
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Data Summary
        - Comprehensive statistics tables
        - Percentage breakdowns
        - Professional formatting
        
        ### 🎯 User Experience
        - Interactive charts with hover details
        - Responsive design
        - Clean, business-ready output
        """)
    
    # Getting started
    st.header("🚀 Ready to Try?")
    
    st.info("""
    1. **Start the Chat Interface**: `streamlit run 5-chat.py`
    2. **Ask for Visualizations**: Use the examples above
    3. **Explore the Results**: Interactive charts + data summaries
    4. **Customize**: Different chart types for different data
    """)
    
    st.success("🎉 The chat interface now automatically generates professional charts and reports when you request them!")

if __name__ == "__main__":
    main()
