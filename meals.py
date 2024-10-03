import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import json

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

# Select your DynamoDB table
meals_table = dynamodb.Table('Meals')
users_table = dynamodb.Table('User')
# Example: Add a meal entry to the DynamoDB table
def add_meal(meal_id, meals):
    try:
        meals_table.put_item(
            Item={
                'meal_id': meal_id,
                'meals': meals  # meals is the field storing all meal-related data
            }
        )
        print(f"Meal with ID {meal_id} added successfully.")
    except ClientError as e:
        print(f"Error adding meal: {e}")

# Example: Get meal details from DynamoDB
def load(meal_id):
    try:
        response = meals_table.get_item(Key={'meal_id': meal_id})
        meals  = response.get('Item', None).get(meal_id, None)
        return json.loads(meals)
    except ClientError as e:
        print(f"Error retrieving meal: {e}")
        return None
    
def get_user_date(user_id):
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        return response.get('Item', None)
    except ClientError as e:
        print(f"Error retrieving user: {e}")
        return None


def update_or_insert_report(user_id, date, new_report_data):
    try:
        # Retrieve user data from DynamoDB
        response = users_table.get_item(Key={'user_id': user_id})
        data = response.get('Item', None)

        # If the user doesn't exist, initialize a new record
        if data is None:
            data = {'user_id': user_id, 'report': {}}
        else:
            # Extract the current report data
            report = data.get('report', {})
        
        # Update the specific date's report with new data
        data['report'][date] = json.dumps(new_report_data, ensure_ascii=False, indent=4)  # Convert dict to JSON string

        # Save the updated report back to the database
        users_table.put_item(Item=data)
        print("Report updated successfully.")
        
    except ClientError as e:
        print(f"Error updating report for {user_id}: {e}")
        return None

# Example: Update a meal in DynamoDB
def update_meal(meal_id, updated_meals):
    try:
        meals_table.update_item(
            Key={'meal_id': meal_id},
            UpdateExpression="set meals=:m",  # updating the 'meals' field
            ExpressionAttributeValues={':m': updated_meals},
            ReturnValues="UPDATED_NEW"
        )
        print("Meal updated successfully.")
    except ClientError as e:
        print(f"Error updating meal: {e}")

