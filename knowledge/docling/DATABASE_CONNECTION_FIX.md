# Database Connection Fix

## Problem
The Streamlit app was failing with the error:
```
ValueError: Table 'docling' was not found
```

This happens because Streamlit runs from a different working directory than expected, causing the relative path `"data/lancedb"` to resolve incorrectly.

## Root Cause
- **Local development**: When you run Python scripts from the `knowledge/docling` directory, the path `"data/lancedb"` works correctly
- **Streamlit deployment**: When Streamlit runs, it may use a different working directory, causing the relative path to fail
- **Path resolution**: The app needs to find the database at `knowledge/docling/data/lancedb` from the workspace root

## Solutions

### Option 1: Use the Helper Script (Recommended)
Run the helper script that automatically sets the correct working directory:

**Windows:**
```bash
cd knowledge/docling
run_streamlit.bat
```

**Linux/Mac:**
```bash
cd knowledge/docling
python run_streamlit.py
```

### Option 2: Set Environment Variable
Set the `DB_PATH` environment variable to the absolute path:

**Windows:**
```cmd
set DB_PATH=E:\MArkaz\markaz-ai\knowledge\docling\data\lancedb
streamlit run knowledge/docling/5-chat.py
```

**Linux/Mac:**
```bash
export DB_PATH=/path/to/markaz-ai/knowledge/docling/data/lancedb
streamlit run knowledge/docling/5-chat.py
```

### Option 3: Run from Correct Directory
Change to the docling directory before running Streamlit:

```bash
cd knowledge/docling
streamlit run 5-chat.py
```

## What Was Fixed

1. **Multiple path resolution**: The app now tries multiple possible paths to find the database
2. **Absolute path support**: Added support for absolute paths via environment variables
3. **Better error messages**: Clear error messages with suggested solutions
4. **Helper scripts**: Created scripts to run Streamlit with correct configuration

## Database Structure
The LanceDB database is located at:
```
knowledge/docling/data/lancedb/docling.lance/
```

The table name is `"docling"` (without the `.lance` extension).

## Verification
To verify the database connection works:

```bash
cd knowledge/docling
python -c "import lancedb; db = lancedb.connect('data/lancedb'); print('Tables:', db.table_names())"
```

Expected output:
```
Tables: ['docling']
```

## Environment Variables
You can set these environment variables for customization:

- `DB_PATH`: Custom database path (default: script directory + data/lancedb)
- `TABLE_NAME`: Custom table name (default: docling)
- `DEBUG`: Enable debug output (set to "true" for verbose logging)
