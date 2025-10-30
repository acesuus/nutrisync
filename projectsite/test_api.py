from tracker.services import CalorieNinjasService

# Initialize service
service = CalorieNinjasService()

# Test query
query = "Last night we ordered a 14oz prime rib and mashed potatoes"
response = service.parse_food_query(query)

print("API Response:")
print(response)

if response.get('success'):
    formatted = service.format_for_food_log(query, response)
    print("\nFormatted for FoodLog:")
    print(formatted)