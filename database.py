
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from datetime import timedelta
from couchbase.options import ClusterOptions, ClusterTimeoutOptions
from couchbase.management.buckets import CreateBucketSettings
from starlette.concurrency import run_in_threadpool
from schemas import ItemCreate, ItemUpdate, Item
import uuid

# 💡 Replace with your real Capella connection string
COUCHBASE_CONNECTION_STRING = "couchbases://cb.r3qa0unhxpltrg-w.cloud.couchbase.com"

USERNAME = "inventory"        # Database access user you created
PASSWORD = "Priya@2210"
BUCKET_NAME = "travel-sample"

cluster = None
bucket = None
collection = None

async def init_db():
    global cluster, bucket, collection
    cluster = Cluster(
        COUCHBASE_CONNECTION_STRING,
        ClusterOptions(
            PasswordAuthenticator(USERNAME, PASSWORD),
            timeout_options=ClusterTimeoutOptions(kv_timeout=timedelta(seconds=10))
        )
    )
    bucket = cluster.bucket(BUCKET_NAME)
    collection = bucket.default_collection()


# Wrap blocking calls with run_in_threadpool for async compatibility

async def insert_item(item: ItemCreate) -> Item:
    item_id = str(uuid.uuid4())
    doc = item.dict()
    doc["id"] = item_id
    await run_in_threadpool(collection.upsert, item_id, doc)  # run sync call in thread
    return Item(**doc)

async def fetch_item(item_id: str) -> Item:
    print(f"Trying to fetch item_id: {item_id}")  # Log the ID
    try:
        result = await run_in_threadpool(collection.get, item_id)
        print(f" Document found: {result.content_as[dict]}")  #  Log result
        return Item(**result.content_as[dict])
    except Exception as e:
        print(f"Error while fetching item: {e}")
        raise e


async def fetch_all_items():
    result = await run_in_threadpool(cluster.query, "SELECT META().id, * FROM `inventory`")
    items = []
    for row in result:
        doc = row['inventory']
        doc["id"] = row["id"]
        items.append(Item(**doc))
    return items

async def update_item(item_id: str, item: ItemUpdate) -> Item:
    current = await run_in_threadpool(collection.get, item_id)
    current_doc = current.content_as[dict]
    updated = {**current_doc, **item.dict(exclude_unset=True)}
    await run_in_threadpool(collection.replace, item_id, updated)
    return Item(id=item_id, **updated)

async def delete_item(item_id: str):
    await run_in_threadpool(collection.remove, item_id)
    return {"message": "Item deleted"}
