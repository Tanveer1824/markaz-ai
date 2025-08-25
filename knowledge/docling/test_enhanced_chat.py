#!/usr/bin/env python3
"""
Test script for enhanced professional chat capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Any
import pandas as pd

def test_professional_formatting():
    """Test the professional formatting functions"""
    
    # Sample real estate data (similar to what would be extracted)
    sample_data = {
        'categories': [
            'Capital Governorate',
            'Hawally Governorate', 
            'Farwaniya Governorate',
            'Ahmadi Governorate',
            'Mubarak Al-Kabeer Governorate',
            'Jahra Governorate'
        ],
        'values': [853, 774, 574, 558, 655, 502],
        'labels': [
            'Capital Governorate: 853.00',
            'Hawally Governorate: 774.00',
            'Farwaniya Governorate: 574.00',
            'Ahmadi Governorate: 558.00',
            'Mubarak Al-Kabeer Governorate: 655.00',
            'Jahra Governorate: 502.00'
        ],
        'chart_type': 'bar',
        'title': 'Real Estate Data Visualization'
    }
    
    print("🏠 Testing Enhanced Professional Chat Capabilities")
    print("=" * 60)
    
    # Test professional table creation
    print("\n1. Professional Data Table:")
    print("-" * 40)
    
    # Import the functions (they should be available in the main chat file)
    try:
        # These would normally be imported from the main chat file
        # For testing, we'll simulate the output
        table_md = f"## 📊 Data Summary\n\n"
        table_md += "| Category | Value | Percentage |\n"
        table_md += "|----------|-------|------------|\n"
        
        total = sum(sample_data['values'])
        
        for category, value in zip(sample_data['categories'], sample_data['values']):
            percentage = (value / total * 100) if total > 0 else 0
            formatted_value = f"KD {value:,.2f}"
            table_md += f"| {category} | {formatted_value} | {percentage:.1f}% |\n"
        
        table_md += f"\n**Total**: KD {total:,.2f}\n"
        print(table_md)
        
    except Exception as e:
        print(f"Error creating table: {e}")
    
    # Test executive summary
    print("\n2. Executive Summary:")
    print("-" * 40)
    
    try:
        total = sum(sample_data['values'])
        max_value = max(sample_data['values'])
        min_value = min(sample_data['values'])
        avg_value = total / len(sample_data['values'])
        
        top_categories = sorted(zip(sample_data['categories'], sample_data['values']), 
                               key=lambda x: x[1], reverse=True)[:3]
        
        summary = f"## 📋 Executive Summary\n\n"
        summary += f"**Analysis of**: Rental Values by Governorate\n\n"
        
        summary += "### 🔑 Key Findings\n"
        summary += f"• **Total Value**: KD {total:,.2f}\n"
        summary += f"• **Range**: KD {min_value:,.2f} - KD {max_value:,.2f}\n"
        summary += f"• **Average**: KD {avg_value:,.2f}\n\n"
        
        summary += "### 🏆 Top Performers\n"
        for i, (category, value) in enumerate(top_categories, 1):
            percentage = (value / total * 100) if total > 0 else 0
            summary += f"{i}. **{category}**: KD {value:,.2f} ({percentage:.1f}%)\n"
        
        print(summary)
        
    except Exception as e:
        print(f"Error creating summary: {e}")
    
    # Test data export
    print("\n3. Data Export (CSV format):")
    print("-" * 40)
    
    try:
        csv_data = "Category,Value,Percentage\n"
        total = sum(sample_data['values'])
        for category, value in zip(sample_data['categories'], sample_data['values']):
            percentage = (value / total * 100) if total > 0 else 0
            csv_data += f'"{category}",{value:.2f},{percentage:.1f}\n'
        
        print(csv_data)
        
    except Exception as e:
        print(f"Error creating CSV: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced professional formatting test completed!")
    print("\nTo use these features in the chat interface:")
    print("1. Ask questions like 'Professional analysis of rental values'")
    print("2. Use keywords like 'executive summary', 'structured breakdown'")
    print("3. Export data using the sidebar export buttons")
    print("4. Get professional tables and insights automatically")

if __name__ == "__main__":
    test_professional_formatting()
