from typing import Optional, List
from pydantic import BaseModel, ValidationError, PydanticValueError, validator, HttpUrl
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.cluster import PasswordAuthenticator
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load Database Settings
load_dotenv()
CONN_STR = os.getenv("CONNECT_STRING")
BUCKET = os.getenv("BUCKET")
SCOPE = os.getenv("SCOPE")
COLLECTION = os.getenv("COLLECTION")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DOCUMENT_LIMIT = 50


class ExtensionError(PydanticValueError):
    """The phone number should not contain extensions"""

    code = "extension"
    msg_template = 'value is an extension, got "{wrong_value}"'


class Phone(BaseModel):
    """Schema for Phone numbers"""

    home: str
    mobile: str

    @validator("mobile", "home")
    def does_not_contain_extension(cls, v):
        """Check if the phone numbers contain extensions"""
        if "x" in v:
            raise ExtensionError(wrong_value=v)
        return v


class UserProfile(BaseModel):
    """Schema for User Profiles"""

    username: str
    name: str
    phone: Phone
    mail: str
    company: Optional[str]
    residence: Optional[str]
    website: List[HttpUrl]
    job: Optional[str]
    address: Optional[str]


if __name__ == "__main__":

    print("Schema for Model\n", UserProfile.schema_json(indent=2))
    password_authenticator = PasswordAuthenticator(DB_USER, DB_PWD)

    # Connect to Couchbase Cluster
    cluster = Cluster(
        CONN_STR,
        ClusterOptions(password_authenticator),
    )
    validation_error_count = 0
    query = f"select profile.* from `{BUCKET}`.{SCOPE}.{COLLECTION} profile LIMIT {DOCUMENT_LIMIT}"
    try:
        # Fetch the documents and test them
        results = cluster.query(query)
        for row in tqdm(results):
            try:
                # Check the validity of the documents
                UserProfile.parse_obj(row)
                validation_error_count += 1
            except ValidationError as e:
                print(f"Error found in document: {row['username']}\n", e.json())
    except Exception as e:
        print(e)

    print(f"Validation Error Count: {validation_error_count}")
