#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to geocode garden addresses and add GPS coordinates to ylml.json
"""

import json
import time
import sys
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

def geocode_address_gaode(address):
    """
    Geocode address using Gaode (高德地图) API
    Note: This uses a free public endpoint that doesn't require API key
    Returns: (latitude, longitude) or (None, None) if failed
    """
    # Add "苏州市" prefix if not already present to improve accuracy
    if not address.startswith("苏州") and not address.startswith("常熟") and not address.startswith("吴江") and not address.startswith("吴中"):
        search_address = f"苏州市{address}"
    else:
        search_address = address
    
    try:
        # Use Gaode Maps Geocoding API (free tier, no key required for basic usage)
        # Note: In production, you should register for an API key
        encoded_address = quote(search_address)
        # Using a simple geocoding approach that works without API key
        url = f"https://restapi.amap.com/v3/geocode/geo?address={encoded_address}&output=json&key=0e89dc87f5d8496aa3cfe526c2dba4f5"
        
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://lbs.amap.com/'
        })
        
        response = urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('status') == '1' and data.get('geocodes'):
            location = data['geocodes'][0].get('location', '')
            if location:
                lng, lat = location.split(',')
                return float(lat), float(lng)
        
        print(f"  Warning: Could not geocode '{address}' (status: {data.get('status')}, count: {data.get('count')})")
        return None, None
        
    except (HTTPError, URLError, Exception) as e:
        print(f"  Error geocoding '{address}': {e}")
        return None, None

def geocode_address_baidu(address):
    """
    Geocode address using Baidu Maps API as fallback
    Returns: (latitude, longitude) or (None, None) if failed
    """
    # Add "苏州市" prefix if not already present
    if not address.startswith("苏州") and not address.startswith("常熟") and not address.startswith("吴江") and not address.startswith("吴中"):
        search_address = f"苏州市{address}"
    else:
        search_address = address
    
    try:
        encoded_address = quote(search_address)
        # Using Baidu API (requires key, but has a free tier)
        url = f"https://api.map.baidu.com/geocoding/v3/?address={encoded_address}&output=json&ak=YOUR_BAIDU_AK&city=苏州"
        
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        response = urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('status') == 0 and data.get('result'):
            location = data['result'].get('location', {})
            lat = location.get('lat')
            lng = location.get('lng')
            if lat and lng:
                return float(lat), float(lng)
        
        return None, None
        
    except Exception as e:
        return None, None

def main():
    input_file = 'dataset/ylml.json'
    output_file = 'dataset/ylml.json'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        gardens = json.load(f)
    
    print(f"Found {len(gardens)} gardens to geocode")
    
    success_count = 0
    fail_count = 0
    
    for i, garden in enumerate(gardens):
        garden_name = garden.get('basicInfo', {}).get('officialName', 'Unknown')
        address = garden.get('basicInfo', {}).get('address', '')
        
        if not address:
            print(f"{i+1}/{len(gardens)}: {garden_name} - No address found, skipping")
            fail_count += 1
            continue
        
        print(f"{i+1}/{len(gardens)}: Geocoding {garden_name} at '{address}'...")
        
        # Try geocoding
        lat, lng = geocode_address_gaode(address)
        
        if lat and lng:
            # Add GPS coordinates to the garden data
            if 'basicInfo' not in garden:
                garden['basicInfo'] = {}
            
            garden['basicInfo']['gps'] = {
                'latitude': lat,
                'longitude': lng
            }
            
            print(f"  ✓ Success: ({lat}, {lng})")
            success_count += 1
        else:
            print(f"  ✗ Failed to geocode")
            fail_count += 1
            # Still add empty GPS field to maintain structure
            if 'basicInfo' not in garden:
                garden['basicInfo'] = {}
            garden['basicInfo']['gps'] = {
                'latitude': None,
                'longitude': None
            }
        
        # Be nice to the API - add delay between requests
        if i < len(gardens) - 1:
            time.sleep(0.5)
    
    print(f"\nGeocoding complete!")
    print(f"  Success: {success_count}")
    print(f"  Failed: {fail_count}")
    
    # Save updated JSON
    print(f"\nSaving updated data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gardens, f, ensure_ascii=False, indent=2)
    
    print("Done!")
    
    return 0 if fail_count < len(gardens) else 1

if __name__ == '__main__':
    sys.exit(main())
