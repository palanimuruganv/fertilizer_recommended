# TabNet Model - Data Type Support

## ✅ Accepted Data Types

### **Numerical Inputs**
The following numeric types are **automatically converted to float** for TabNet:

| Type | Example | Status |
|------|---------|--------|
| **Integer** | `50`, `100`, `-5` | ✅ Accepted |
| **Float** | `50.5`, `100.25`, `6.5` | ✅ Accepted |
| **String (numeric)** | `"50"`, `"6.5"` | ✅ Accepted |
| **Decimal** | `Decimal('50.50')` | ✅ Accepted |
| **NaN (Not a Number)** | `float('nan')` | ⚠️ Converted to 0.0 |
| **Infinity** | `float('inf')` | ⚠️ Converted to 0.0 |

### **Categorical Inputs**
Categorical values must be exact string matches from the dataset:

| Field | Valid Values (Examples) |
|-------|------------------------|
| **Soil_Type** | Clay, Sandy, Loamy, Silt, etc. |
| **Crop_Type** | Wheat, Rice, Maize, Cotton, Potato, etc. |
| **Crop_Growth_Stage** | Seedling, Vegetative, Flowering, Maturity, Harvest, etc. |
| **Season** | Kharif, Rabi, Summer, etc. |
| **Irrigation_Type** | Drip, Sprinkler, Canal, Flood, etc. |
| **Previous_Crop** | Rice, Wheat, Maize, Cotton, Potato, etc. |
| **Region** | North, South, East, West, Central, etc. |

## 🔧 Data Type Conversion Flow

```
User Input (any numeric type)
    ↓
float() conversion
    ↓
NaN/Inf validation
    ↓
Pandas DataFrame
    ↓
LabelEncoder (categorical)
    ↓
StandardScaler (numerical)
    ↓
NumPy Float32 Array
    ↓
TabNet Model
```

## 📋 Numerical Input Fields

These fields accept **any numeric value** (int, float, string numbers):

```python
[
    "Soil_pH",                      # 0-14 range typical
    "Soil_Moisture",                # 0-100 (%)
    "Organic_Carbon",               # 0-1+ (%)
    "Electrical_Conductivity",      # 0-5+ (dS/m)
    "Nitrogen_Level",               # 0-100+ (ppm)
    "Phosphorus_Level",             # 0-100+ (ppm)
    "Potassium_Level",              # 0-100+ (ppm)
    "Temperature",                  # Any range (°C)
    "Humidity",                     # 0-100 (%)
    "Rainfall",                     # 0-5000+ (mm)
    "Fertilizer_Used_Last_Season",  # 0-1000+ (kg/ha)
    "Yield_Last_Season"             # 0-20+ (tons/ha)
]
```

## ⚡ Error Handling

If conversion fails, the system:
1. **Logs a warning** with the specific error
2. **Defaults to 0.0** for that field
3. **Continues processing** with other inputs
4. **Still makes a prediction** (without that feature)

## 🎯 Example Valid Inputs

### ✅ Valid (Will Work)
```json
{
  "Soil_Type": "Clay",
  "Nitrogen_Level": 50,           // Integer
  "Soil_pH": 6.5,                 // Float
  "Temperature": "28.3",          // String number
  "Humidity": "60"                // String number
}
```

### ❌ Invalid (Will Fail/Default)
```json
{
  "Soil_Type": "Unknown",         // Not in training data
  "Nitrogen_Level": "abc",        // Non-numeric string → defaults to 0.0
  "Soil_pH": NaN,                 // Invalid → defaults to 0.0
  "Temperature": Infinity         // Invalid → defaults to 0.0
}
```

## 📊 Frontend Input Validation

HTML form fields use:
- `type="number"` for numeric inputs (prevents invalid entries)
- `type="select"` for categorical inputs (ensures valid values)
- `step="0.1"` for decimal precision
- `min`, `max` attributes for reasonable ranges

## 🔍 Type Conversion in Code

```python
# Automatic conversion in app.py
for col in numerical_input_cols:
    try:
        value = float(data.get(col, 0))
        # Validate
        if np.isnan(value) or np.isinf(value):
            value = 0.0
        user_input[col] = value
    except (TypeError, ValueError):
        user_input[col] = 0.0  # Default fallback
```

## 🎓 Summary

| Aspect | Detail |
|--------|--------|
| **Integer Input** | ✅ Accepted - auto-converted to float |
| **Float Input** | ✅ Accepted - used directly |
| **String Number** | ✅ Accepted - converted to float |
| **Invalid Numbers** | ⚠️ Converted to 0.0 with warning |
| **Categorical Input** | ✅ Only exact matches from training data |
| **Output Format** | NumPy float32 array for TabNet |

---

**The model is flexible with numeric types but ensures data integrity through validation and conversion!**
