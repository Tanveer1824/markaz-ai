#!/usr/bin/env python3
"""
Test script for focused, concise professional output
"""

def test_focused_output():
    """Test the focused output format"""
    
    # Sample real estate data
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
    
    print("🏠 Testing Focused Professional Output")
    print("=" * 50)
    
    # Test focused executive summary
    print("\n1. Focused Executive Summary:")
    print("-" * 30)
    
    total = sum(sample_data['values'])
    max_value = max(sample_data['values'])
    min_value = min(sample_data['values'])
    avg_value = total / len(sample_data['values'])
    
    top_categories = sorted(zip(sample_data['categories'], sample_data['values']), 
                           key=lambda x: x[1], reverse=True)[:3]
    
    summary = f"## 📋 Executive Summary\n\n"
    summary += "### 🔑 Key Findings\n"
    summary += f"• **Total Value**: KD {total:,.2f}\n"
    summary += f"• **Range**: KD {min_value:,.2f} - KD {max_value:,.2f}\n"
    summary += f"• **Average**: KD {avg_value:,.2f}\n\n"
    
    summary += "### 🏆 Top Performers\n"
    for i, (category, value) in enumerate(top_categories, 1):
        percentage = (value / total * 100) if total > 0 else 0
        summary += f"{i}. **{category}**: KD {value:,.2f} ({percentage:.1f}%)\n"
    
    print(summary)
    
    # Test focused data table
    print("\n2. Focused Data Table:")
    print("-" * 30)
    
    table_md = f"## 📊 Market Data Breakdown\n\n"
    table_md += "| Category | Value |\n"
    table_md += "|----------|-------|\n"
    
    for category, value in zip(sample_data['categories'], sample_data['values']):
        formatted_value = f"KD {value:,.2f}"
        table_md += f"| {category} | {formatted_value} |\n"
    
    table_md += f"\n**Total**: KD {total:,.2f}\n"
    print(table_md)
    
    # Test focused insights
    print("\n3. Focused Key Insights:")
    print("-" * 30)
    
    insights = "## 💡 Key Insights\n"
    for i, (category, value) in enumerate(top_categories, 1):
        insights += f"{i}. **{category}** leads with KD {value:,.2f}\n"
    
    if len(sample_data['values']) > 3:
        insights += f"4. **{len(sample_data['values'])-3} additional segments** show varied performance\n"
    
    print(insights)
    
    # Test strategic recommendations
    print("\n4. Strategic Recommendations:")
    print("-" * 30)
    
    recommendations = "## 🎯 Strategic Recommendations\n"
    recommendations += "• **Market Entry**: Focus on high-performing segments for immediate returns\n"
    recommendations += "• **Risk Management**: Diversify across multiple governorates and property types\n"
    recommendations += "• **Growth Strategy**: Monitor emerging trends for future investment opportunities\n"
    
    print(recommendations)
    
    print("\n" + "=" * 50)
    print("✅ Focused output test completed!")
    print("\nKey improvements:")
    print("• Removed unnecessary sections (Detailed Analysis, Source Information)")
    print("• Simplified data tables (Category | Value only)")
    print("• Focused executive summary (Key Findings + Top Performers)")
    print("• Concise insights and recommendations")
    print("• No repetitive explanations")

if __name__ == "__main__":
    test_focused_output()
