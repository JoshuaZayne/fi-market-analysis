"""
Financial Institution Data Loader
=================================

Load and manage FI data from various sources.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Optional


class FILoader:
    """Load financial institution data from various sources."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the loader."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config"
        self.config_path = Path(config_path)

    def load_from_config(self) -> List[Dict]:
        """
        Load FI data from config/fi_database.json.

        Returns:
            List of institution dictionaries
        """
        db_path = self.config_path / "fi_database.json"

        with open(db_path, 'r') as f:
            data = json.load(f)

        return data.get('financial_institutions', [])

    def load_from_csv(self, file_path: str) -> List[Dict]:
        """
        Load FI data from CSV file.

        Expected columns: name, type, assets, region, current_vendor, tech_stack, state

        Args:
            file_path: Path to CSV file

        Returns:
            List of institution dictionaries
        """
        institutions = []

        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                institution = {
                    'name': row.get('name', ''),
                    'ticker': row.get('ticker'),
                    'type': row.get('type', 'bank'),
                    'assets': float(row.get('assets', 0)),
                    'region': row.get('region', 'Unknown'),
                    'current_vendor': row.get('current_vendor', 'Unknown'),
                    'tech_stack': row.get('tech_stack', 'unknown'),
                    'state': row.get('state', '')
                }
                institutions.append(institution)

        return institutions

    def load_from_json(self, file_path: str) -> List[Dict]:
        """
        Load FI data from JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            List of institution dictionaries
        """
        with open(file_path, 'r') as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        elif 'financial_institutions' in data:
            return data['financial_institutions']
        else:
            return []

    def save_to_json(self, institutions: List[Dict], file_path: str) -> None:
        """
        Save FI data to JSON file.

        Args:
            institutions: List of institution dictionaries
            file_path: Output file path
        """
        with open(file_path, 'w') as f:
            json.dump({'financial_institutions': institutions}, f, indent=2)

    def filter_institutions(
        self,
        institutions: List[Dict],
        region: Optional[str] = None,
        fi_type: Optional[str] = None,
        min_assets: Optional[float] = None,
        max_assets: Optional[float] = None,
        vendor: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter institutions by criteria.

        Args:
            institutions: List to filter
            region: Filter by region
            fi_type: Filter by type (bank, credit_union)
            min_assets: Minimum assets
            max_assets: Maximum assets
            vendor: Filter by current vendor

        Returns:
            Filtered list
        """
        result = institutions

        if region:
            result = [fi for fi in result if fi.get('region', '').lower() == region.lower()]

        if fi_type:
            result = [fi for fi in result if fi.get('type', '').lower() == fi_type.lower()]

        if min_assets is not None:
            result = [fi for fi in result if fi.get('assets', 0) >= min_assets]

        if max_assets is not None:
            result = [fi for fi in result if fi.get('assets', 0) <= max_assets]

        if vendor:
            result = [fi for fi in result if vendor.lower() in fi.get('current_vendor', '').lower()]

        return result

    def get_summary(self, institutions: List[Dict]) -> Dict:
        """
        Get summary statistics for a list of institutions.

        Args:
            institutions: List of institutions

        Returns:
            Summary dictionary
        """
        if not institutions:
            return {"count": 0}

        total_assets = sum(fi.get('assets', 0) for fi in institutions)
        banks = sum(1 for fi in institutions if fi.get('type') == 'bank')
        credit_unions = sum(1 for fi in institutions if fi.get('type') == 'credit_union')

        regions = {}
        for fi in institutions:
            region = fi.get('region', 'Unknown')
            regions[region] = regions.get(region, 0) + 1

        vendors = {}
        for fi in institutions:
            vendor = fi.get('current_vendor', 'Unknown')
            vendors[vendor] = vendors.get(vendor, 0) + 1

        return {
            "count": len(institutions),
            "banks": banks,
            "credit_unions": credit_unions,
            "total_assets": total_assets,
            "avg_assets": total_assets / len(institutions),
            "by_region": regions,
            "by_vendor": vendors
        }
