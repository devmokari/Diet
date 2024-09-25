import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

# Select your DynamoDB table
table = dynamodb.Table('Meals')

# Example: Add a meal entry to the DynamoDB table
def add_meal(meal_id, meals):
    try:
        table.put_item(
            Item={
                'meal_id': meal_id,
                'meals': meals  # meals is the field storing all meal-related data
            }
        )
        print(f"Meal with ID {meal_id} added successfully.")
    except ClientError as e:
        print(f"Error adding meal: {e}")

# Example: Get meal details from DynamoDB
def get_meal(meal_id):
    try:
        response = table.get_item(Key={'meal_id': meal_id})
        return response.get('Item', None).get(meal_id, None)
    except ClientError as e:
        print(f"Error retrieving meal: {e}")
        return None

# Example: Update a meal in DynamoDB
def update_meal(meal_id, updated_meals):
    try:
        table.update_item(
            Key={'meal_id': meal_id},
            UpdateExpression="set meals=:m",  # updating the 'meals' field
            ExpressionAttributeValues={':m': updated_meals},
            ReturnValues="UPDATED_NEW"
        )
        print("Meal updated successfully.")
    except ClientError as e:
        print(f"Error updating meal: {e}")

# Example Usage:

# # Add a meal entry
# new_meal_data = {
#     "بروتين": "2.0",
#     "غلات": "2.5",
#     "خضروات": "1.0"
# }
# add_meal('diet_1', new_meal_data)

# # Get a meal
# meal = get_meal('diet_1')
# if meal:
#     print(f"Retrieved meal: {meal}")
# else:
#     print("Meal not found.")

# # Update a meal
# updated_meal_data = {
#     "بروتين": "3.0",
#     "غلات": "3.5",
#     "خضروات": "1.5"
# }
# update_meal('diet_1', updated_meal_data)
