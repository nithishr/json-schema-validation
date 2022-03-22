# Generate Fake User Profile Data
import random
import json
from faker import Faker
from tqdm import tqdm

fake = Faker()

FAKE_DOCS_COUNT = 100000
MAIL_ERRORS = 0.1
PHONE_ERRORS = 0.2

error_email = 0
error_phone = 0
docs = []

for i in tqdm(range(FAKE_DOCS_COUNT)):
    profile = fake.profile(
        fields=[
            "residence",
            "job",
            "company",
            "name",
            "username",
            "address",
            "website",
            "mail",
        ]
    )
    profile["phone"] = {"home": fake.phone_number(), "mobile": fake.phone_number()}

    # Simulate broken documents
    choice = random.random()
    if choice <= MAIL_ERRORS:
        del profile["mail"]
        error_email += 1

    if choice <= PHONE_ERRORS:
        del profile["phone"]["mobile"]
        error_phone += 1

    docs.append(profile)

# Write the data to an output file for importing into couchbase
with open("fake_data.json", "w") as fout:
    json.dump(docs, fout)

print(f"Total Docs: {len(docs)}")
print(f"Document Errors\n Emails: {error_email} \n Phones:{error_phone}")
