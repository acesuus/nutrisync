import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CalorieNinjasService:
    """
    Service to interact with CalorieNinjas API
    Documentation: https://calorieninjas.com/api
    """
    
    BASE_URL = "https://api.calorieninjas.com/v1/nutrition"
    
    def __init__(self):
        self.api_key = settings.CALORIENINJAS_API_KEY
        self.headers = {'X-Api-Key': self.api_key}
    
    def parse_food_query(self, query):
        """
        Parse natural language food query using CalorieNinjas API
        
        Args:
            query (str): Natural language query like "Last night we ordered a 14oz prime rib and mashed potatoes"
        
        Returns:
            dict: Parsed nutrition information or error
        """
        try:
            params = {'query': query}
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'items': data.get('items', []),
                    'raw_response': data
                }
            else:
                logger.error(f"CalorieNinjas API error: {response.status_code}")
                return {
                    'success': False,
                    'error': f"API returned status code {response.status_code}",
                    'message': response.text
                }
                
        except requests.exceptions.Timeout:
            logger.error("CalorieNinjas API timeout")
            return {
                'success': False,
                'error': 'API request timeout',
                'message': 'The request took too long. Please try again.'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CalorieNinjas API request failed: {str(e)}")
            return {
                'success': False,
                'error': 'API request failed',
                'message': str(e)
            }
    
    def extract_food_items(self, api_response):
        """
        Extract and format food items from API response
        
        Args:
            api_response (dict): Response from parse_food_query
        
        Returns:
            list: List of formatted food items
        """
        if not api_response.get('success'):
            return []
        
        items = api_response.get('items', [])
        formatted_items = []
        
        for item in items:
            formatted_items.append({
                'name': item.get('name', 'Unknown'),
                'calories': item.get('calories', 0),
                'serving_size_g': item.get('serving_size_g', 0),
                'protein_g': item.get('protein_g', 0),
                'carbohydrates_total_g': item.get('carbohydrates_total_g', 0),
                'fat_total_g': item.get('fat_total_g', 0),
                'sugar_g': item.get('sugar_g', 0),
                'fiber_g': item.get('fiber_g', 0),
                'sodium_mg': item.get('sodium_mg', 0),
            })
        
        return formatted_items
    
    def format_for_food_log(self, query, api_response):
        """
        Format API response into FoodLog compatible format
        
        Args:
            query (str): Original user query
            api_response (dict): Response from parse_food_query
        
        Returns:
            dict: Data ready for FoodLog model
        """
        items = self.extract_food_items(api_response)
        
        if not items:
            return {
                'food_name': query[:200],  # Use query as fallback
                'description': 'Could not fetch nutrition data',
                'calories': 0
            }
        
        # Combine all food items into one log entry
        total_calories = sum(item['calories'] for item in items)
        food_names = [item['name'].title() for item in items]
        
        # Create detailed description
        description_parts = []
        for item in items:
            desc = (
                f"{item['name'].title()}: "
                f"{item['calories']} cal, "
                f"{item['protein_g']}g protein, "
                f"{item['carbohydrates_total_g']}g carbs, "
                f"{item['fat_total_g']}g fat"
            )
            description_parts.append(desc)
        
        return {
            'food_name': ' + '.join(food_names),
            'description': '\n'.join(description_parts),
            'calories': round(total_calories, 1),
            'items': items  # Include for potential future use
        }