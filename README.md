# Fashion & Nail AI 💅✨

A sophisticated AI-powered fashion and nail expert that provides personalized recommendations in two modes:
- **Outfit → Nails**: Get nail polish suggestions based on your outfit
- **Nails → Outfit**: Get outfit recommendations based on your nail polish

## Features

- 🎨 **Extensive Color Palette**: 15+ color families with 5 unique shades each
- 💅 **Polish Type Variety**: Polygel, Gel, Dip Powder, Acrylic, Regular, Matte, Glossy, Shellac
- 👗 **Smart Outfit Matching**: Considers outfit types, colors, and occasions
- 🔄 **Variation Algorithm**: Never repeats the same combinations
- 📱 **REST API**: Easy integration with web and mobile apps

## Quick Start

### Installation

1. **Clone or download the files**
```bash
# Make sure you have Python 3.7+ installed
python --version
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python fashion_nail_ai.py
```

The API will be available at `http://localhost:5000`

### API Usage

#### Health Check
```bash
curl http://localhost:5000/health
```

#### 1️⃣ Outfit → Nails Mode

**Request:**
```bash
curl -X POST http://localhost:5000/fashion-advice \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "outfit_to_nails",
    "outfit_description": "Black elegant dress with silver accessories",
    "outfit_type": "Dresses"
  }'
```

**Response:**
```json
{
  "classic": {
    "name": "Nude",
    "shade": "Champagne Nude",
    "hex": "#F7E7CE",
    "polish_type": "Gel"
  },
  "bold": {
    "name": "Cherry Red",
    "shade": "Classic Cherry",
    "hex": "#DE3163",
    "polish_type": "Glossy"
  }
}
```

#### 2️⃣ Nails → Outfit Mode

**Request:**
```bash
curl -X POST http://localhost:5000/fashion-advice \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "nails_to_outfit",
    "nail_color": "Hot Pink",
    "nail_shade": "Fuchsia Pink",
    "polish_type": "Gel"
  }'
```

**Response:**
```json
{
  "casual": {
    "top": "Cotton T-Shirt",
    "bottom": "Jeans",
    "shoes": "Sneakers",
    "accessories": "Rose gold jewelry, pink accent bag"
  },
  "dressy": {
    "top": "Silk Blouse",
    "bottom": "Pencil Skirt",
    "shoes": "Heels",
    "accessories": "Pearl jewelry, blush clutch"
  }
}
```

## Supported Options

### Outfit Types
- **Clothing**: Dresses, Skirts, Pants, Jeans, Shorts, Shirts, Blouses, Jackets, Coats, Sweaters, T-Shirts, Jumpsuits, Rompers, Suits
- **Footwear**: Sneakers, Heels, Sandals

### Color Palette
- **Neutrals**: Nude, Sheer Pink, Rose, Silver
- **Bold Colors**: Cherry Red, Hot Pink, Electric Blue, Burgundy
- **Pastels**: Lavender, Mint Green, Sky Blue, Coral
- **Metallics**: Gold, Silver
- **Rich Tones**: Plum, Tangerine

### Polish Types
- Polygel, Gel, Dip Powder, Acrylic
- Regular Nail Polish, Matte, Glossy, Shellac

## Example Use Cases

### Business Meeting
```json
{
  "mode": "outfit_to_nails",
  "outfit_description": "Navy blue suit with white shirt",
  "outfit_type": "Suits"
}
```

### Date Night
```json
{
  "mode": "nails_to_outfit",
  "nail_color": "Burgundy",
  "nail_shade": "Deep Burgundy",
  "polish_type": "Gel"
}
```

### Casual Weekend
```json
{
  "mode": "outfit_to_nails",
  "outfit_description": "Denim jeans with white t-shirt",
  "outfit_type": "Jeans"
}
```

## API Integration

### Python Example
```python
import requests
import json

def get_nail_suggestions(outfit_desc, outfit_type):
    url = "http://localhost:5000/fashion-advice"
    payload = {
        "mode": "outfit_to_nails",
        "outfit_description": outfit_desc,
        "outfit_type": outfit_type
    }
    response = requests.post(url, json=payload)
    return response.json()

# Usage
suggestions = get_nail_suggestions("Red cocktail dress", "Dresses")
print(f"Classic: {suggestions['classic']['name']} - {suggestions['classic']['shade']}")
print(f"Bold: {suggestions['bold']['name']} - {suggestions['bold']['shade']}")
```

### JavaScript Example
```javascript
async function getNailSuggestions(outfitDesc, outfitType) {
    const response = await fetch('http://localhost:5000/fashion-advice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mode: 'outfit_to_nails',
            outfit_description: outfitDesc,
            outfit_type: outfitType
        })
    });
    
    return await response.json();
}

// Usage
getNailSuggestions('Blue summer dress', 'Dresses')
    .then(data => console.log(data));
```

## Advanced Features

### Variation Algorithm
The AI ensures no repeated combinations by:
- Tracking the last 20 suggestions
- Randomizing color selections within appropriate palettes
- Varying shades and polish types for the same color

### Smart Color Matching
The AI considers:
- **Outfit colors**: Matches complementary or contrasting colors
- **Outfit types**: Formal vs. casual appropriateness
- **Occasions**: Business, casual, evening, etc.
- **Color theory**: Harmonious color combinations

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters)
- `500`: Server error

Example error response:
```json
{
  "error": "Missing outfit_description or outfit_type"
}
```

## Customization

You can easily extend the AI by modifying `fashion_nail_ai.py`:

1. **Add new colors**: Update the `color_palette` dictionary
2. **Add polish types**: Extend the `polish_types` list
3. **Modify outfit logic**: Update `_get_colors_for_outfit()` method
4. **Add new outfit types**: Extend the `outfit_types` list

## Technical Details

- **Framework**: Flask (Python web framework)
- **Algorithm**: Rule-based AI with randomization
- **Memory**: Tracks recent suggestions to ensure variation
- **Performance**: Fast response times with efficient color matching

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in fashion_nail_ai.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **JSON parsing errors**
   - Ensure Content-Type is set to `application/json`
   - Validate JSON format before sending

## Contributing

Feel free to enhance the AI by:
- Adding more color combinations
- Improving outfit matching logic
- Adding seasonal considerations
- Implementing user preferences

## License

This project is open source and available under the MIT License.

---

**Happy styling! 💅✨**