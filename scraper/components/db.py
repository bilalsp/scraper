import logging
import boto3

logger = logging.getLogger(__name__)


def get_table(table_name, dyn_resource=None):
    """Get DynamoDB table.
    Args:
        dyn_resource: Either a Boto3 or DAX resource.
    Returns:
        table: The newly created table if doesn't exist
    """
    params = {
        'TableName': table_name,
        'KeySchema': [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'id', 
                'AttributeType': 'S'
            }
        ],
        'ProvisionedThroughput': 
            {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
    }

    try:
        if dyn_resource is None:
            dyn_resource = boto3.resource('dynamodb')
        table = dyn_resource.create_table(**params)
        table.wait_until_exists()
        logger.info(f'Created dynamoDB table - {table_name}')
    except Exception as e:
        logger.exception(e)
        table = dyn_resource.Table(table_name)
        
    return table
    
    
    
def save(table, jobs):
    """ """
    for job in jobs:
        try:
            if job:
                response = table.put_item(Item = job)
        except Exception as e:
            logger.exception(e)
    
    logger.info('Stored all fetched jobs into dynamoDB')