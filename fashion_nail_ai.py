import json
import random
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenAI Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

@dataclass
class ColorOption:
    name: str
    shade: str
    hex: str
    polish_type: str

@dataclass
class OutfitOption:
    top: str
    bottom: str
    shoes: str
    accessories: str

class FashionNailAI:
    def __init__(self):
        self.use_openai = bool(os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here')
        
        # Color palette with specific shades and hex codes
        self.color_palette = {
            "Nude": {
                "shades": ["Beige Nude", "Champagne Nude", "Taupe Nude", "Cream Nude", "Sand Nude"],
                "hex_codes": ["#F5DEB3", "#F7E7CE", "#D2B48C", "#FFF8DC", "#C2B280"]
            },
            "Sheer Pink": {
                "shades": ["Ballet Pink", "Rose Quartz", "Blush Pink", "Powder Pink", "Soft Pink"],
                "hex_codes": ["#F8BBD9", "#F7CAC9", "#FFB6C1", "#FFD1DC", "#FFCCCB"]
            },
            "Coral": {
                "shades": ["Living Coral", "Peach Coral", "Salmon Coral", "Bright Coral", "Sunset Coral"],
                "hex_codes": ["#FF6F61", "#FFAB91", "#FA8072", "#FF7F50", "#FF5722"]
            },
            "Cherry Red": {
                "shades": ["Classic Cherry", "Deep Cherry", "Bright Cherry", "Wine Cherry", "Ruby Cherry"],
                "hex_codes": ["#DE3163", "#B22222", "#DC143C", "#722F37", "#E0115F"]
            },
            "Burgundy": {
                "shades": ["Deep Burgundy", "Wine Burgundy", "Maroon Burgundy", "Oxblood", "Claret"],
                "hex_codes": ["#800020", "#722F37", "#800000", "#4A0E0E", "#7F1734"]
            },
            "Lavender": {
                "shades": ["Soft Lavender", "French Lavender", "Dusty Lavender", "Pale Lavender", "Mauve Lavender"],
                "hex_codes": ["#E6E6FA", "#9966CC", "#C4A4DE", "#DDA0DD", "#E0B4D6"]
            },
            "Mint Green": {
                "shades": ["Fresh Mint", "Pale Mint", "Seafoam Mint", "Spearmint", "Pastel Mint"],
                "hex_codes": ["#98FB98", "#AFEEEE", "#20B2AA", "#00FF7F", "#90EE90"]
            },
            "Sky Blue": {
                "shades": ["Powder Blue", "Baby Blue", "Cornflower Blue", "Light Sky Blue", "Periwinkle"],
                "hex_codes": ["#87CEEB", "#89CFF0", "#6495ED", "#87CEFA", "#CCCCFF"]
            },
            "Electric Blue": {
                "shades": ["Neon Blue", "Cobalt Blue", "Royal Blue", "Sapphire Blue", "Azure Blue"],
                "hex_codes": ["#7DF9FF", "#0047AB", "#4169E1", "#0F52BA", "#007FFF"]
            },
            "Gold": {
                "shades": ["Rose Gold", "Champagne Gold", "Antique Gold", "Metallic Gold", "Warm Gold"],
                "hex_codes": ["#E8B4A0", "#F7E7CE", "#CD7F32", "#FFD700", "#B8860B"]
            },
            "Silver": {
                "shades": ["Chrome Silver", "Platinum Silver", "Metallic Silver", "Pearl Silver", "Gunmetal Silver"],
                "hex_codes": ["#C0C0C0", "#E5E4E2", "#BCC6CC", "#F8F6F0", "#2C3539"]
            },
            "Rose": {
                "shades": ["Dusty Rose", "Mauve Rose", "Antique Rose", "Tea Rose", "Old Rose"],
                "hex_codes": ["#DCAE96", "#E0B4D6", "#FAEBD7", "#F88379", "#C08081"]
            },
            "Plum": {
                "shades": ["Deep Plum", "Purple Plum", "Wine Plum", "Eggplant", "Aubergine"],
                "hex_codes": ["#673147", "#8E4585", "#722F37", "#614051", "#3C1414"]
            },
            "Tangerine": {
                "shades": ["Bright Tangerine", "Peach Tangerine", "Orange Tangerine", "Sunset Tangerine", "Coral Tangerine"],
                "hex_codes": ["#FF8C00", "#FFAB91", "#FFA500", "#FF6347", "#FF7F50"]
            },
            "Hot Pink": {
                "shades": ["Fuchsia Pink", "Magenta Pink", "Neon Pink", "Electric Pink", "Vibrant Pink"],
                "hex_codes": ["#FF1493", "#FF00FF", "#FF69B4", "#FF6EC7", "#FF10F0"]
            }
        }
        
        self.polish_types = ["Polygel", "Gel", "Dip Powder", "Acrylic", "Regular Nail Polish", "Matte", "Glossy", "Shellac"]
        
        self.outfit_types = ["Dresses", "Skirts", "Pants", "Jeans", "Shorts", "Shirts", "Blouses", 
                           "Jackets", "Coats", "Sweaters", "T-Shirts", "Jumpsuits", "Rompers", 
                           "Suits", "Sneakers", "Heels", "Sandals"]
        
        # Store previous suggestions to ensure variation
        self.previous_nail_suggestions = []
        self.previous_outfit_suggestions = []
        
    def get_random_color_option(self, color_name: str) -> ColorOption:
        """Get a random shade and hex code for a given color name."""
        if color_name in self.color_palette:
            shades = self.color_palette[color_name]["shades"]
            hex_codes = self.color_palette[color_name]["hex_codes"]
            
            # Select random shade and corresponding hex
            index = random.randint(0, len(shades) - 1)
            shade = shades[index]
            hex_code = hex_codes[index]
            polish_type = random.choice(self.polish_types)
            
            return ColorOption(color_name, shade, hex_code, polish_type)
        else:
            # Fallback for unknown colors
            return ColorOption(color_name, f"{color_name} Shade", "#000000", random.choice(self.polish_types))
    
    def outfit_to_nails(self, outfit_description: str, outfit_type: str) -> Dict[str, Any]:
        """Generate nail polish suggestions based on outfit."""
        if self.use_openai:
            return self._outfit_to_nails_openai(outfit_description, outfit_type)
        else:
            return self._outfit_to_nails_classic(outfit_description, outfit_type)
    
    def _outfit_to_nails_classic(self, outfit_description: str, outfit_type: str) -> Dict[str, Any]:
        """Generate nail polish suggestions using classic algorithm."""
        # Determine appropriate colors based on outfit type and description
        classic_colors, bold_colors = self._get_colors_for_outfit(outfit_description, outfit_type)
        
        # Select random colors ensuring variation
        classic_color = random.choice(classic_colors)
        bold_color = random.choice(bold_colors)
        
        # Ensure we don't repeat the exact same combination
        attempts = 0
        while attempts < 10:  # Prevent infinite loop
            classic_option = self.get_random_color_option(classic_color)
            bold_option = self.get_random_color_option(bold_color)
            
            suggestion_key = f"{classic_option.name}_{classic_option.shade}_{bold_option.name}_{bold_option.shade}"
            if suggestion_key not in self.previous_nail_suggestions:
                self.previous_nail_suggestions.append(suggestion_key)
                # Keep only last 20 suggestions to prevent memory issues
                if len(self.previous_nail_suggestions) > 20:
                    self.previous_nail_suggestions.pop(0)
                break
            attempts += 1
        
        return {
            "classic": {
                "name": classic_option.name,
                "shade": classic_option.shade,
                "hex": classic_option.hex,
                "polish_type": classic_option.polish_type
            },
            "bold": {
                "name": bold_option.name,
                "shade": bold_option.shade,
                "hex": bold_option.hex,
                "polish_type": bold_option.polish_type
            }
        }
    
    def _outfit_to_nails_openai(self, outfit_description: str, outfit_type: str) -> Dict[str, Any]:
        """Generate nail polish suggestions using OpenAI."""
        try:
            available_colors = list(self.color_palette.keys())
            available_polish_types = self.polish_types
            
            prompt = f"""
            You are a fashion and nail expert AI. Based on the outfit description and type provided, suggest nail polish options.
            
            Outfit: {outfit_description}
            Outfit Type: {outfit_type}
            
            Available Colors: {', '.join(available_colors)}
            Available Polish Types: {', '.join(available_polish_types)}
            
            Please suggest:
            1. A CLASSIC option (neutral/safe color)
            2. A BOLD option (vibrant/contrasting color)
            
            For each option, choose from the available colors and polish types.
            Consider color theory, fashion matching, and the occasion.
            
            Respond ONLY with a JSON object in this exact format:
            {{
                "classic_color": "Color Name",
                "bold_color": "Color Name"
            }}
            """
            
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=OPENAI_TEMPERATURE
            )
            
            ai_response = response.choices[0].message.content
            ai_data = json.loads(ai_response)
            
            # Get specific shades and polish types for the AI-suggested colors
            classic_color = ai_data.get('classic_color', 'Nude')
            bold_color = ai_data.get('bold_color', 'Cherry Red')
            
            # Ensure colors are valid, fallback to default if not
            if classic_color not in self.color_palette:
                classic_color = 'Nude'
            if bold_color not in self.color_palette:
                bold_color = 'Cherry Red'
            
            classic_option = self.get_random_color_option(classic_color)
            bold_option = self.get_random_color_option(bold_color)
            
            return {
                "classic": {
                    "name": classic_option.name,
                    "shade": classic_option.shade,
                    "hex": classic_option.hex,
                    "polish_type": classic_option.polish_type
                },
                "bold": {
                    "name": bold_option.name,
                    "shade": bold_option.shade,
                    "hex": bold_option.hex,
                    "polish_type": bold_option.polish_type
                }
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to classic algorithm
            return self._outfit_to_nails_classic(outfit_description, outfit_type)
    
    def nails_to_outfit(self, nail_color: str, nail_shade: str, polish_type: str) -> Dict[str, Any]:
        """Generate outfit suggestions based on nail polish."""
        if self.use_openai:
            return self._nails_to_outfit_openai(nail_color, nail_shade, polish_type)
        else:
            return self._nails_to_outfit_classic(nail_color, nail_shade, polish_type)
    
    def _nails_to_outfit_classic(self, nail_color: str, nail_shade: str, polish_type: str) -> Dict[str, Any]:
        """Generate outfit suggestions using classic algorithm."""
        # Get outfit options that complement the nail color
        casual_options, dressy_options = self._get_outfits_for_nails(nail_color, nail_shade)
        
        # Select random outfits ensuring variation
        attempts = 0
        while attempts < 10:  # Prevent infinite loop
            casual_outfit = random.choice(casual_options)
            dressy_outfit = random.choice(dressy_options)
            
            suggestion_key = f"{casual_outfit['top']}_{casual_outfit['bottom']}_{dressy_outfit['top']}_{dressy_outfit['bottom']}"
            if suggestion_key not in self.previous_outfit_suggestions:
                self.previous_outfit_suggestions.append(suggestion_key)
                # Keep only last 20 suggestions to prevent memory issues
                if len(self.previous_outfit_suggestions) > 20:
                    self.previous_outfit_suggestions.pop(0)
                break
            attempts += 1
        
        return {
            "casual": casual_outfit,
            "dressy": dressy_outfit
        }
    
    def _nails_to_outfit_openai(self, nail_color: str, nail_shade: str, polish_type: str) -> Dict[str, Any]:
        """Generate outfit suggestions using OpenAI."""
        try:
            prompt = f"""
            You are a fashion and nail expert AI. Based on the nail polish provided, suggest outfit combinations.
            
            Nail Polish: {nail_color} - {nail_shade} ({polish_type})
            
            Please suggest:
            1. A CASUAL outfit (everyday wearable style)
            2. A DRESSY outfit (elegant/evening style)
            
            For each outfit, specify: Top, Bottom, Shoes, Accessories
            
            Consider color coordination, style matching, and fashion principles.
            Make the suggestions specific and stylish.
            
            Respond ONLY with a JSON object in this exact format:
            {{
                "casual": {{
                    "top": "Top Name",
                    "bottom": "Bottom Name", 
                    "shoes": "Shoes Name",
                    "accessories": "Accessories Description"
                }},
                "dressy": {{
                    "top": "Top Name",
                    "bottom": "Bottom Name",
                    "shoes": "Shoes Name", 
                    "accessories": "Accessories Description"
                }}
            }}
            """
            
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=OPENAI_TEMPERATURE
            )
            
            ai_response = response.choices[0].message.content
            ai_data = json.loads(ai_response)
            
            return ai_data
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to classic algorithm
            return self._nails_to_outfit_classic(nail_color, nail_shade, polish_type)
    
    def _get_colors_for_outfit(self, outfit_description: str, outfit_type: str) -> Tuple[List[str], List[str]]:
        """Determine appropriate nail colors based on outfit."""
        outfit_lower = outfit_description.lower()
        type_lower = outfit_type.lower()
        
        # Classic colors (neutral/safe)
        classic_colors = ["Nude", "Sheer Pink", "Rose"]
        
        # Bold colors (vibrant/contrasting)
        bold_colors = ["Cherry Red", "Hot Pink", "Electric Blue"]
        
        # Adjust colors based on outfit characteristics
        if any(word in outfit_lower for word in ["black", "dark", "elegant"]):
            classic_colors.extend(["Silver", "Burgundy"])
            bold_colors.extend(["Cherry Red", "Gold"])
        
        if any(word in outfit_lower for word in ["white", "light", "cream"]):
            classic_colors.extend(["Nude", "Sheer Pink"])
            bold_colors.extend(["Coral", "Lavender"])
        
        if any(word in outfit_lower for word in ["blue", "denim"]):
            classic_colors.extend(["Nude", "Silver"])
            bold_colors.extend(["Coral", "Cherry Red"])
        
        if any(word in outfit_lower for word in ["red", "pink"]):
            classic_colors.extend(["Nude", "Rose"])
            bold_colors.extend(["Burgundy", "Gold"])
        
        if any(word in outfit_lower for word in ["green", "olive"]):
            classic_colors.extend(["Nude", "Gold"])
            bold_colors.extend(["Burgundy", "Plum"])
        
        # Adjust based on outfit type
        if type_lower in ["dresses", "skirts", "heels"]:
            bold_colors.extend(["Hot Pink", "Cherry Red"])
        
        if type_lower in ["jeans", "sneakers", "t-shirts"]:
            classic_colors.extend(["Nude", "Sheer Pink"])
        
        if type_lower in ["suits", "jackets", "coats"]:
            classic_colors.extend(["Nude", "Rose", "Silver"])
            bold_colors.extend(["Burgundy", "Plum"])
        
        return list(set(classic_colors)), list(set(bold_colors))
    
    def _get_outfits_for_nails(self, nail_color: str, nail_shade: str) -> Tuple[List[Dict], List[Dict]]:
        """Determine appropriate outfits based on nail color."""
        color_lower = nail_color.lower()
        
        casual_options = []
        dressy_options = []
        
        # Base outfit options
        casual_tops = ["Cotton T-Shirt", "Casual Blouse", "Denim Shirt", "Knit Sweater", "Tank Top"]
        casual_bottoms = ["Jeans", "Casual Pants", "Denim Shorts", "Leggings", "Casual Skirt"]
        casual_shoes = ["Sneakers", "Flats", "Casual Sandals", "Loafers", "Canvas Shoes"]
        
        dressy_tops = ["Silk Blouse", "Dress Shirt", "Elegant Sweater", "Blazer", "Cocktail Top"]
        dressy_bottoms = ["Dress Pants", "Pencil Skirt", "Elegant Dress", "Formal Shorts", "Wide-leg Pants"]
        dressy_shoes = ["Heels", "Dress Shoes", "Elegant Sandals", "Pumps", "Ankle Boots"]
        
        # Adjust based on nail color
        if "red" in color_lower or "cherry" in color_lower:
            casual_accessories = ["Silver jewelry, black handbag", "Gold accessories, neutral tote", "Statement earrings, crossbody bag"]
            dressy_accessories = ["Diamond earrings, black clutch", "Gold jewelry, evening bag", "Pearl necklace, elegant purse"]
        elif "pink" in color_lower:
            casual_accessories = ["Rose gold jewelry, pink accent bag", "Silver accessories, neutral tote", "Delicate jewelry, crossbody bag"]
            dressy_accessories = ["Pearl jewelry, blush clutch", "Rose gold accessories, evening bag", "Diamond studs, elegant purse"]
        elif "blue" in color_lower:
            casual_accessories = ["Silver jewelry, denim accessories", "White accessories, canvas bag", "Nautical jewelry, tote bag"]
            dressy_accessories = ["Silver jewelry, navy clutch", "White gold accessories, evening bag", "Sapphire jewelry, elegant purse"]
        elif "nude" in color_lower or "beige" in color_lower:
            casual_accessories = ["Gold jewelry, tan handbag", "Neutral accessories, leather bag", "Minimalist jewelry, tote bag"]
            dressy_accessories = ["Gold jewelry, nude clutch", "Champagne accessories, evening bag", "Elegant jewelry, neutral purse"]
        else:
            casual_accessories = ["Mixed metal jewelry, versatile bag", "Neutral accessories, everyday tote", "Simple jewelry, crossbody bag"]
            dressy_accessories = ["Statement jewelry, elegant clutch", "Classic accessories, evening bag", "Sophisticated jewelry, formal purse"]
        
        # Generate multiple outfit combinations
        for _ in range(5):  # Generate 5 options each
            casual_options.append({
                "top": random.choice(casual_tops),
                "bottom": random.choice(casual_bottoms),
                "shoes": random.choice(casual_shoes),
                "accessories": random.choice(casual_accessories)
            })
            
            dressy_options.append({
                "top": random.choice(dressy_tops),
                "bottom": random.choice(dressy_bottoms),
                "shoes": random.choice(dressy_shoes),
                "accessories": random.choice(dressy_accessories)
            })
        
        return casual_options, dressy_options

# Initialize the AI
fashion_ai = FashionNailAI()

@app.route('/')
def index():
    """Serve the web interface."""
    return render_template('index.html')

@app.route('/fashion-advice', methods=['POST'])
def get_fashion_advice():
    """Main API endpoint for fashion advice."""
    try:
        data = request.get_json()
        
        if not data or 'mode' not in data:
            return jsonify({"error": "Missing 'mode' parameter"}), 400
        
        mode = data['mode']
        
        if mode == "outfit_to_nails":
            if 'outfit_description' not in data or 'outfit_type' not in data:
                return jsonify({"error": "Missing outfit_description or outfit_type"}), 400
            
            result = fashion_ai.outfit_to_nails(
                data['outfit_description'], 
                data['outfit_type']
            )
            return jsonify(result)
        
        elif mode == "nails_to_outfit":
            if 'nail_color' not in data or 'nail_shade' not in data or 'polish_type' not in data:
                return jsonify({"error": "Missing nail_color, nail_shade, or polish_type"}), 400
            
            result = fashion_ai.nails_to_outfit(
                data['nail_color'],
                data['nail_shade'],
                data['polish_type']
            )
            return jsonify(result)
        
        else:
            return jsonify({"error": "Invalid mode. Use 'outfit_to_nails' or 'nails_to_outfit'"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy", 
        "message": "Fashion & Nail AI is running",
        "openai_enabled": fashion_ai.use_openai,
        "ai_model": OPENAI_MODEL if fashion_ai.use_openai else "Classic Algorithm"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)