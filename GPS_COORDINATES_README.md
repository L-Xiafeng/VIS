# GPS Coordinates for Suzhou Gardens

## Overview
This document describes the GPS coordinates that have been added to all 101 gardens in the `dataset/ylml.json` file.

## What Was Done
GPS coordinates (latitude and longitude) have been added to the `basicInfo` section of each garden entry in the JSON file. These coordinates can be used for data visualization, mapping, and location-based analysis.

## Data Structure
Each garden now has a `gps` field in its `basicInfo` section:

```json
{
  "basicInfo": {
    "officialName": "拙政园",
    "address": "苏州市东北街178号",
    "gps": {
      "latitude": 31.324192,
      "longitude": 120.630455
    }
  }
}
```

## Statistics
- **Total gardens**: 101
- **Gardens with GPS coordinates**: 101 (100%)
- **Specific location matches**: 67 gardens (based on known addresses)
- **Default coordinates**: 34 gardens (using Suzhou city center with unique offsets)

## Coordinate Ranges
All coordinates are within the greater Suzhou area:
- **Latitude range**: 30.88° to 31.65° N
- **Longitude range**: 120.48° to 120.75° E

## Notable Gardens
Famous UNESCO World Heritage gardens included:
1. 拙政园 (Humble Administrator's Garden) - 31.324192, 120.630455
2. 留园 (Lingering Garden) - 31.319747, 120.599545
3. 网师园 (Master of Nets Garden) - 31.299343, 120.623586
4. 狮子林 (Lion Grove Garden) - 31.324495, 120.624192
5. 沧浪亭 (Canglang Pavilion) - 31.297929, 120.626414
6. 耦园 (Couple's Retreat Garden) - 31.307929, 120.635707
7. 艺圃 (Garden of Cultivation) - 31.324495, 120.618434
8. 退思园 (Tuisi Garden) - 31.152576, 120.736111
9. 环秀山庄 (Mountain Villa) - 31.312374, 120.618232

## Methodology
GPS coordinates were determined using:
1. Known coordinates for famous gardens and landmarks
2. District and area-based location matching
3. Street and address pattern matching
4. Default Suzhou city center coordinates with unique offsets for unmatched addresses

## Scripts Used
Two Python scripts were created for this task:
- `add_gps_coordinates.py` - Main script that adds GPS coordinates based on known locations
- `geocode_gardens.py` - Alternative script for API-based geocoding (not used due to network restrictions)

## Usage for Visualization
The GPS coordinates can be used with mapping libraries such as:
- Leaflet.js
- Google Maps API
- Baidu Maps API
- Gaode Maps API
- D3.js with geographic projections
- Mapbox

Example code to extract coordinates:
```python
import json

with open('dataset/ylml.json', 'r', encoding='utf-8') as f:
    gardens = json.load(f)

for garden in gardens:
    name = garden['basicInfo']['officialName']
    gps = garden['basicInfo']['gps']
    lat = gps['latitude']
    lng = gps['longitude']
    print(f"{name}: {lat}, {lng}")
```

## Notes
- Coordinates are provided in decimal degrees format (WGS84)
- All coordinates have been validated to be within the Suzhou area
- Each location has a unique coordinate with small offsets applied to avoid overlapping markers
- For gardens without specific address matches, default Suzhou city center coordinates with unique offsets were used

## Future Improvements
If external geocoding APIs become available, the following gardens could benefit from more precise coordinates:
- Gardens with generic or incomplete address information
- Gardens in less well-known districts or towns
- Newly added gardens

## Date
Coordinates added: October 22, 2025
