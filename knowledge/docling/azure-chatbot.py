import streamlit as st
import lancedb
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="KFH Real Estate AI Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Database path configuration - Azure compatible
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "lancedb")

def azure_openai_embedding(texts):
    """Custom embedding function using Azure OpenAI"""
    if isinstance(texts, str):
        texts = [texts]
    
    try:
        response = client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
            input=texts
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        st.error(f"Azure OpenAI embedding error: {e}")
        return None

# Initialize LanceDB connection with Azure compatibility
@st.cache_resource
def init_db():
    """Initialize database connection with Azure compatibility.

    Returns:
        LanceDB table object or None if database unavailable
    """
    try:
        # Check if we're running in Azure
        is_azure = os.getenv("AZURE_WEBAPP_NAME") or os.getenv("WEBSITE_SITE_NAME")
        
        if is_azure:
            st.info("🌐 Running in Azure environment")
        
        # Try to connect to database
        if os.path.exists(DB_PATH):
            db = lancedb.connect(DB_PATH)
            table = db.open_table("docling")
            st.success("✅ Database connected successfully!")
            return table
        else:
            raise FileNotFoundError(f"Database path not found: {DB_PATH}")
            
    except Exception as e:
        st.warning("⚠️ Database not available - using fallback mode")
        st.info(f"Error: {str(e)}")
        return None

def get_context_fallback(query: str) -> str:
    """Fallback context when database is not available"""
    return f"""
    This is a fallback response for your query: "{query}"
    
    The knowledge base database is not currently available. This could be because:
    - The database hasn't been built yet
    - The application is running in a fresh deployment
    - Database files are not accessible
    
    To get full functionality, please ensure the database is properly set up.
    """

def get_context(query: str, table, num_results: int = 5) -> str:
    """Search the database for relevant context.

    Args:
        query: User's question
        table: LanceDB table object
        num_results: Number of results to return

    Returns:
        str: Concatenated context from relevant chunks with source information
    """
    if table is None:
        return get_context_fallback(query)
    
    try:
        # Convert query to vector using Azure OpenAI
        query_vector = azure_openai_embedding(query)
        if query_vector is None:
            return get_context_fallback(query)
        
        # Search using vector similarity
        results = table.search(query=query_vector[0], query_type="vector").limit(num_results).to_pandas()
        contexts = []

        for _, row in results.iterrows():
            # Extract metadata
            filename = row["metadata"]["filename"]
            page_numbers = row["metadata"]["page_numbers"]
            title = row["metadata"]["title"]

            # Build source citation
            source_parts = []
            if filename:
                source_parts.append(filename)
            if page_numbers:
                source_parts.append(f"p. {', '.join(str(p) for p in page_numbers)}")

            source = f"\nSource: {' - '.join(source_parts)}"
            if title:
                source += f"\nTitle: {title}"

            contexts.append(f"{row['text']}{source}")

        return "\n\n".join(contexts)
    except Exception as e:
        st.error(f"Error searching database: {e}")
        return get_context_fallback(query)

def get_chat_response(messages, context: str) -> str:
    """Get streaming response from Azure OpenAI API.

    Args:
        messages: Chat history
        context: Retrieved context from database

    Returns:
        str: Model's response
    """
    system_prompt = f"""You are a helpful real estate analyst assistant that answers questions based on the KFH Real Estate Report 2025 Q1.
    Use only the information from the provided context to answer questions. If you're unsure or the context
    doesn't contain the relevant information, say so.
    
    RESPONSE STYLE: CONCISE & FOCUSED
    - Keep answers brief and to the point
    - Use bullet points for key data
    - Highlight important numbers with **bold**
    - Avoid lengthy explanations unless specifically requested
    - Focus on the most relevant information first
    
    DEFINITION RESPONSES:
    - For "what is", "definition", "what does mean" questions:
      * Provide clear, concise definitions
      * Use bullet points for key characteristics
      * Highlight specific requirements or criteria with **bold**
      * Include relevant examples if available
      * Keep to 3-5 key points maximum
    
    VISUALIZATION REQUESTS:
    - When users ask for charts, graphs, or visualizations:
      * Provide a brief summary of the data that will be visualized
      * Mention that a chart has been generated and displayed
      * Keep the text response concise since the chart shows the data
    
    Context from KFH Real Estate Report 2025 Q1:
    {context}
    
    Always provide accurate, data-driven insights based on the report content.
    Be concise and direct in your responses.
    """

    messages_with_context = [{"role": "system", "content": system_prompt}, *messages]

    try:
        # Create the streaming response with controlled length
        stream = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=messages_with_context,
            stream=True,
            max_tokens=1000,
            temperature=0.7
        )
        
        response = ""
        message_placeholder = st.empty()
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                message_placeholder.markdown(response + "▌")
        
        message_placeholder.markdown(response)
        return response
        
    except Exception as e:
        error_msg = f"Error getting response from Azure OpenAI: {e}"
        st.error(error_msg)
        return error_msg

def detect_visualization_request(text: str) -> bool:
    """Detect if user wants a visualization"""
    viz_keywords = [
        "chart", "graph", "plot", "visualize", "show me", "display",
        "bar chart", "pie chart", "line graph", "scatter plot",
        "trends over time", "comparison", "distribution"
    ]
    return any(keyword in text.lower() for keyword in viz_keywords)

def detect_definition_request(text: str) -> bool:
    """Detect if user wants a definition"""
    def_keywords = [
        "what is", "definition", "what does mean", "explain",
        "define", "meaning of", "describe"
    ]
    return any(keyword in text.lower() for keyword in def_keywords)

def format_definition_response(response: str) -> str:
    """Format definition responses for better readability"""
    # Add bullet points and formatting for definitions
    lines = response.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip() and not line.startswith('*'):
            formatted_lines.append(f"• {line.strip()}")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def create_sample_visualization():
    """Create a sample visualization when database is not available"""
    # Sample data for demonstration
    categories = ['Residential', 'Commercial', 'Industrial', 'Land']
    values = [45, 30, 15, 10]
    
    fig = px.pie(
        names=categories, 
        values=values,
        title="Sample Market Distribution (Demo Data)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Main application
def main():
    st.title("🏢 KFH Real Estate AI Assistant")
    st.markdown("Your intelligent guide to the KFH Real Estate Report 2025 Q1")
    
    # Initialize database
    table = init_db()
    
    # Show database status
    if table is None:
        st.warning("""
        **⚠️ Database Status**: Knowledge base not available
        
        **🔧 To enable full functionality**:
        1. Ensure database files are included in deployment
        2. Run the data pipeline: `1-extraction.py` → `2-chunking.py` → `3-embedding.py`
        3. Check file permissions and paths
        
        **💡 Current Mode**: Fallback mode with limited responses
        """)
        
        # Show sample visualization option
        if st.button("Show Sample Visualization"):
            fig = create_sample_visualization()
            st.plotly_chart(fig, use_container_width=True)
            st.info("This is sample data. Connect the database for real insights.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about financial data or request a chart..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get relevant context
        with st.status("🔍 Searching real estate report...", expanded=False) as status:
            context = get_context(prompt, table)
            
            if table is not None:
                st.markdown(
                    """
                    <style>
                    .search-result {
                        margin: 10px 0;
                        padding: 10px;
                        border-radius: 4px;
                        background-color: #f0f2f6;
                    }
                    .search-result summary {
                        cursor: pointer;
                        color: #0f52ba;
                        font-weight: 500;
                    }
                    .search-result summary:hover {
                        color: #1e90ff;
                    }
                    .metadata {
                        font-size: 0.9em;
                        color: #666;
                        font-style: italic;
                    }
                    </style>
                """,
                    unsafe_allow_html=True,
                )

                st.write("📄 Found relevant sections from the report:")
                for chunk in context.split("\n\n"):
                    if chunk.strip():
                        # Split into text and metadata parts
                        parts = chunk.split("\n")
                        if len(parts) > 1:
                            text = parts[0]
                            metadata = {
                                line.split(": ")[0]: line.split(": ")[1]
                                for line in parts[1:]
                                if ": " in line
                            }

                            source = metadata.get("Source", "Unknown source")
                            title = metadata.get("Title", "KFH Real Estate Report 2025 Q1")

                            st.markdown(
                                f"""
                                <div class="search-result">
                                    <details>
                                        <summary>{source}</summary>
                                        <div class="metadata">Section: {title}</div>
                                        <div style="margin-top: 8px;">{text}</div>
                                    </details>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
            else:
                st.info("📝 Using fallback context - database not available")

        # Display assistant response
        with st.chat_message("assistant"):
            if table is None:
                # Fallback response when database is not available
                response = f"""
                I understand you're asking about: "{prompt}"
                
                Unfortunately, I don't have access to the full knowledge base at the moment. 
                This is likely because the database hasn't been properly set up in this deployment.
                
                **To get accurate answers about the KFH Real Estate Report 2025 Q1:**
                1. Ensure the database files are included in your deployment
                2. Run the data processing pipeline
                3. Check that the LanceDB table 'docling' exists
                
                **For now, I can help with general real estate questions** or you can try reconnecting the database.
                """
            else:
                # Check if user wants visualization
                is_visualization_request = detect_visualization_request(prompt)
                
                if is_visualization_request:
                    response = "I can see you want a visualization! However, the visualization features require the full database to be available. Please ensure the database is properly connected to enable chart generation."
                else:
                    # Get regular model response
                    response = get_chat_response(st.session_state.messages, context)
                    
                    # Check if this is a definition request and format accordingly
                    if detect_definition_request(prompt):
                        response = format_definition_response(response)

            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar with helpful information
    with st.sidebar:
        st.header("📊 Report Overview")
        st.info("This assistant can help you with questions about:")
        st.markdown("""
        - Market trends and analysis
        - Property valuations
        - Investment opportunities
        - Regional market insights
        - Economic indicators
        - Future projections
        """)
        
        st.header("💡 Sample Questions")
        st.markdown("""
        - "What are the key market trends for 2025?"
        - "How are property prices performing?"
        - "What investment opportunities are highlighted?"
        - "What's the outlook for residential vs commercial?"
        """)
        
        st.header("🎯 Response Style")
        st.info("**Concise & Focused Answers:**")
        st.markdown("""
        - Brief, to-the-point responses
        - Key data in bullet points
        - Important numbers highlighted
        - No lengthy explanations
        """)
        
        # Database status in sidebar
        st.header("🔧 System Status")
        if table is not None:
            st.success("✅ Database Connected")
            st.info("Full functionality available")
        else:
            st.error("❌ Database Disconnected")
            st.warning("Limited functionality")
            st.info("Check deployment configuration")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
