#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, '.')

try:
    # Test environment variables
    os.environ['SUPABASE_PROJECT_REF'] = '127.0.0.1:54322'
    os.environ['SUPABASE_DB_PASSWORD'] = 'pRl7Lc3w5brT3lSW4pLmuS-dr0Nefru3@c3ib'
    os.environ['SUPABASE_REGION'] = 'us-east-1'
    os.environ['QUERY_API_KEY'] = 'test-key'
    
    from supabase_mcp.settings import Settings
    print("Settings module imported successfully")
    
    # Test settings creation
    settings = Settings()
    print(f"Project ref: {settings.supabase_project_ref}")
    print(f"Region: {settings.supabase_region}")
    print(f"Password: {settings.supabase_db_password}")
    print("Settings validation passed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
