"""
This module provides endpoints for accessing and managing research samples stored in MongoDB.

Functions:
- get_samples: Retrieves a list of samples from MongoDB, optionally filtered by sample_type and/or status.
- get_sample: Fetches a single sample by its unique sample_id.
- create_sample: Inserts a new sample document into MongoDB based on the provided data.
- update_sample: Updates an existing sample document identified by sample_id with the specified fields.
- delete_sample: Deletes a sample document from MongoDB by its sample_id.
"""

from typing import List
from database import mongo_db
from schemas import Sample, SampleCreate, SampleUpdate

collection = mongo_db['samples']

async def get_samples(sample_type: str = None, status: str = None) -> List[Sample]:
    query = {}
    if sample_type:
        query['sample_type'] = sample_type
    if status:
        query['status'] = status
    cursor = collection.find(query)
    return [Sample(**doc) async for doc in cursor]

async def get_sample(sample_id: str) -> Sample:
    doc = await collection.find_one({'sample_id': sample_id})
    return Sample(**doc) if doc else None

async def create_sample(sample: SampleCreate) -> Sample:
    await collection.insert_one(sample.model_dump())
    return sample

async def update_sample(sample_id: str, data: SampleUpdate) -> Sample:
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    await collection.update_one({'sample_id': sample_id}, {'$set': update_data})
    return await get_sample(sample_id)

async def delete_sample(sample_id: str) -> bool:
    result = await collection.delete_one({'sample_id': sample_id})
    return result.deleted_count == 1