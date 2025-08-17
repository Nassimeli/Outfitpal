#!/usr/bin/env python3
"""
Test script for Fashion & Nail AI
Demonstrates both outfit-to-nails and nails-to-outfit modes
"""

import requests
import json
import time
from typing import Dict, Any

class FashionAITester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> bool:
        """Test if the API is running."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health Check: {data['message']}")
                return True
            else:
                print(f"❌ Health Check Failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to the API. Make sure the server is running.")
            return False
    
    def test_outfit_to_nails(self, outfit_description: str, outfit_type: str) -> Dict[str, Any]:
        """Test outfit to nails recommendation."""
        payload = {
            "mode": "outfit_to_nails",
            "outfit_description": outfit_description,
            "outfit_type": outfit_type
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/fashion-advice",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return {}
    
    def test_nails_to_outfit(self, nail_color: str, nail_shade: str, polish_type: str) -> Dict[str, Any]:
        """Test nails to outfit recommendation."""
        payload = {
            "mode": "nails_to_outfit",
            "nail_color": nail_color,
            "nail_shade": nail_shade,
            "polish_type": polish_type
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/fashion-advice",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return {}
    
    def print_nail_suggestions(self, outfit_desc: str, outfit_type: str, suggestions: Dict[str, Any]):
        """Pretty print nail suggestions."""
        print(f"\n👗 OUTFIT: {outfit_desc} ({outfit_type})")
        print("=" * 60)
        
        if suggestions:
            classic = suggestions.get('classic', {})
            bold = suggestions.get('bold', {})
            
            print(f"💅 CLASSIC OPTION:")
            print(f"   Color: {classic.get('name', 'N/A')} - {classic.get('shade', 'N/A')}")
            print(f"   Hex: {classic.get('hex', 'N/A')}")
            print(f"   Type: {classic.get('polish_type', 'N/A')}")
            
            print(f"\n💅 BOLD OPTION:")
            print(f"   Color: {bold.get('name', 'N/A')} - {bold.get('shade', 'N/A')}")
            print(f"   Hex: {bold.get('hex', 'N/A')}")
            print(f"   Type: {bold.get('polish_type', 'N/A')}")
        else:
            print("❌ No suggestions received")
    
    def print_outfit_suggestions(self, nail_color: str, nail_shade: str, polish_type: str, suggestions: Dict[str, Any]):
        """Pretty print outfit suggestions."""
        print(f"\n💅 NAILS: {nail_color} - {nail_shade} ({polish_type})")
        print("=" * 60)
        
        if suggestions:
            casual = suggestions.get('casual', {})
            dressy = suggestions.get('dressy', {})
            
            print(f"👕 CASUAL OUTFIT:")
            print(f"   Top: {casual.get('top', 'N/A')}")
            print(f"   Bottom: {casual.get('bottom', 'N/A')}")
            print(f"   Shoes: {casual.get('shoes', 'N/A')}")
            print(f"   Accessories: {casual.get('accessories', 'N/A')}")
            
            print(f"\n✨ DRESSY OUTFIT:")
            print(f"   Top: {dressy.get('top', 'N/A')}")
            print(f"   Bottom: {dressy.get('bottom', 'N/A')}")
            print(f"   Shoes: {dressy.get('shoes', 'N/A')}")
            print(f"   Accessories: {dressy.get('accessories', 'N/A')}")
        else:
            print("❌ No suggestions received")
    
    def run_comprehensive_test(self):
        """Run a comprehensive test of all functionality."""
        print("🧪 FASHION & NAIL AI - COMPREHENSIVE TEST")
        print("=" * 60)
        
        # Health check
        if not self.test_health():
            return
        
        print("\n" + "="*60)
        print("🎯 TESTING OUTFIT → NAILS RECOMMENDATIONS")
        print("="*60)
        
        # Test outfit to nails scenarios
        outfit_scenarios = [
            ("Black elegant evening dress with silver jewelry", "Dresses"),
            ("Blue denim jeans with white cotton t-shirt", "Jeans"),
            ("Navy blue business suit with white shirt", "Suits"),
            ("Red cocktail dress for date night", "Dresses"),
            ("Casual khaki shorts with striped shirt", "Shorts"),
            ("Cozy gray sweater with black leggings", "Sweaters")
        ]
        
        for outfit_desc, outfit_type in outfit_scenarios:
            suggestions = self.test_outfit_to_nails(outfit_desc, outfit_type)
            self.print_nail_suggestions(outfit_desc, outfit_type, suggestions)
            time.sleep(0.5)  # Small delay for readability
        
        print("\n" + "="*60)
        print("🎯 TESTING NAILS → OUTFIT RECOMMENDATIONS")
        print("="*60)
        
        # Test nails to outfit scenarios
        nail_scenarios = [
            ("Cherry Red", "Classic Cherry", "Gel"),
            ("Hot Pink", "Fuchsia Pink", "Matte"),
            ("Nude", "Champagne Nude", "Shellac"),
            ("Electric Blue", "Cobalt Blue", "Acrylic"),
            ("Burgundy", "Deep Burgundy", "Dip Powder"),
            ("Lavender", "Soft Lavender", "Regular Nail Polish")
        ]
        
        for nail_color, nail_shade, polish_type in nail_scenarios:
            suggestions = self.test_nails_to_outfit(nail_color, nail_shade, polish_type)
            self.print_outfit_suggestions(nail_color, nail_shade, polish_type, suggestions)
            time.sleep(0.5)  # Small delay for readability
        
        print("\n" + "="*60)
        print("🎯 TESTING VARIATION ALGORITHM")
        print("="*60)
        
        # Test that repeated requests give different results
        print("\n🔄 Testing variation with repeated outfit:")
        outfit_desc = "Little black dress"
        outfit_type = "Dresses"
        
        print(f"Making 3 requests for: {outfit_desc}")
        for i in range(3):
            print(f"\n--- Request {i+1} ---")
            suggestions = self.test_outfit_to_nails(outfit_desc, outfit_type)
            if suggestions:
                classic = suggestions.get('classic', {})
                bold = suggestions.get('bold', {})
                print(f"Classic: {classic.get('name')} - {classic.get('shade')} ({classic.get('polish_type')})")
                print(f"Bold: {bold.get('name')} - {bold.get('shade')} ({bold.get('polish_type')})")
            time.sleep(0.5)
        
        print("\n🔄 Testing variation with repeated nails:")
        nail_color, nail_shade, polish_type = "Hot Pink", "Magenta Pink", "Gel"
        
        print(f"Making 3 requests for: {nail_color} - {nail_shade}")
        for i in range(3):
            print(f"\n--- Request {i+1} ---")
            suggestions = self.test_nails_to_outfit(nail_color, nail_shade, polish_type)
            if suggestions:
                casual = suggestions.get('casual', {})
                dressy = suggestions.get('dressy', {})
                print(f"Casual: {casual.get('top')} + {casual.get('bottom')}")
                print(f"Dressy: {dressy.get('top')} + {dressy.get('bottom')}")
            time.sleep(0.5)
        
        print("\n" + "="*60)
        print("✅ COMPREHENSIVE TEST COMPLETED!")
        print("="*60)

def main():
    """Main function to run tests."""
    print("Starting Fashion & Nail AI Tests...")
    print("Make sure the server is running: python fashion_nail_ai.py\n")
    
    tester = FashionAITester()
    tester.run_comprehensive_test()
    
    print("\n💡 TIP: Try different outfits and nail colors to see the AI in action!")
    print("💡 TIP: Each request should give slightly different results due to the variation algorithm.")

if __name__ == "__main__":
    main()