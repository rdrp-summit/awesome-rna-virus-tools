#!/usr/bin/env python3
"""
Validate JSON entries against the schema

This script validates all JSON files in the entries/ directory
against the defined schema and reports any errors.
"""

import json
import jsonschema
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
ENTRIES_DIR = "entries"
SCHEMA_FILE = "scripts/schema.json"

def load_schema() -> Dict[str, Any]:
    """Load the JSON schema."""
    try:
        with open(SCHEMA_FILE, 'r') as f:
            schema = json.load(f)
        logger.info(f"Loaded schema from {SCHEMA_FILE}")
        return schema
    except FileNotFoundError:
        logger.error(f"Schema file not found: {SCHEMA_FILE}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in schema file: {e}")
        raise

def validate_entry(entry_path: Path, schema: Dict[str, Any]) -> List[str]:
    """Validate a single entry against the schema."""
    errors = []
    
    try:
        with open(entry_path, 'r') as f:
            entry_data = json.load(f)
        
        # Validate against schema
        try:
            jsonschema.validate(entry_data, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
        
        # Additional custom validations
        errors.extend(validate_custom_rules(entry_data))
        
    except FileNotFoundError:
        errors.append("File not found")
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
    
    return errors

def validate_custom_rules(entry: Dict[str, Any]) -> List[str]:
    """Apply custom validation rules beyond the schema."""
    errors = []
    
    # Check for deprecated package_manager field
    if 'package_manager' in entry and 'package_managers' not in entry:
        errors.append("Warning: 'package_manager' field is deprecated, use 'package_managers' array instead")
    
    # Check URL accessibility (basic format check)
    url = entry.get('url', '')
    if url and not (url.startswith('http://') or url.startswith('https://')):
        errors.append("URL should start with http:// or https://")
    
    # Check DOI format
    doi = entry.get('doi', '')
    if doi and not doi.startswith('10.'):
        errors.append("DOI should start with '10.'")
    
    # Check date format
    date = entry.get('date', '')
    if date:
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            errors.append("Date should be in YYYY-MM-DD format")
    
    # Check topics are not empty
    topics = entry.get('topics', [])
    if not topics:
        errors.append("At least one topic is required")
    
    # Check for reasonable description length
    description = entry.get('description', '')
    if len(description) > 500:
        errors.append("Description is very long (>500 chars), consider shortening")
    if len(description) < 10:
        errors.append("Description is very short (<10 chars), consider expanding")
    
    return errors

def validate_all_entries() -> bool:
    """Validate all entries and return True if all are valid."""
    entries_path = Path(ENTRIES_DIR)
    
    if not entries_path.exists():
        logger.error(f"Entries directory not found: {ENTRIES_DIR}")
        return False
    
    # Load schema
    try:
        schema = load_schema()
    except Exception:
        return False
    
    # Find all JSON files
    json_files = list(entries_path.glob("*.json"))
    if not json_files:
        logger.warning(f"No JSON files found in {ENTRIES_DIR}")
        return True
    
    logger.info(f"Validating {len(json_files)} entries...")
    
    all_valid = True
    total_errors = 0
    total_warnings = 0
    
    for json_file in sorted(json_files):
        errors = validate_entry(json_file, schema)
        
        if errors:
            all_valid = False
            logger.error(f"\n❌ {json_file.name}:")
            for error in errors:
                if error.startswith("Warning:"):
                    logger.warning(f"  {error}")
                    total_warnings += 1
                else:
                    logger.error(f"  {error}")
                    total_errors += 1
        else:
            logger.info(f"✅ {json_file.name}")
    
    # Summary
    logger.info(f"\n📊 Validation Summary:")
    logger.info(f"  Total files: {len(json_files)}")
    logger.info(f"  Valid files: {len(json_files) - len([f for f in json_files if validate_entry(f, schema)])}")
    logger.info(f"  Total errors: {total_errors}")
    logger.info(f"  Total warnings: {total_warnings}")
    
    if all_valid:
        logger.info("🎉 All entries are valid!")
    else:
        logger.error("❌ Some entries have validation errors")
    
    return all_valid

def main():
    """Main entry point."""
    logger.info("Starting entry validation")
    
    success = validate_all_entries()
    
    if success:
        logger.info("Validation completed successfully")
        exit(0)
    else:
        logger.error("Validation failed")
        exit(1)

if __name__ == "__main__":
    main()