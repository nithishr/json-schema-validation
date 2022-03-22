# JSON Schema Validation using Pydantic

An example showcasing how to validate JSON documents stored in [Couchbase](http://couchbase.com/) against a schema defined using [Pydantic](https://pydantic-docs.helpmanual.io/).

### Requirements

- Python 3.7+
- Install the dependencies
  $ `pip install -r requirements.txt`

### Generating Fake Data

Run the `generate_fake_data.py` script by specifying the amount of documents to be generated in the variable `FAKE_DOCS_COUNT`.

The script would output the generated data into `fake_data.json`.

### Importing the Data

The data can be imported from the Couchbase UI by specifying the output file with the key set as the `username` field. For reference the [documentation](https://docs.couchbase.com/server/current/manage/import-documents/import-documents.html) can be checked.

### Validating the Documents in Couchbase

Set the environment variables to connect to Couchbase by copying the `.env.example` file and renaming it to `.env` and specifying the values.

```
    CONNECT_STRING= The connection string like "couchbases://<capella-host>?ssl=no_verify" or "couchbase://localhost:8091"
    BUCKET= Bucket where documents are stored
    SCOPE= Scope for the collection where documents are stored
    COLLECTION= Collection containing the documents
    DB_USER= Database user with the permissions for the bucket
    DB_PWD= Database user's password
```

Run the script

$ `python validate_documents.py`

The output shows the schema for the documents. This is followed by the documents that do not conform to the schema.

Schema

```
{
	"title": "UserProfile",
	"description": "Schema for User Profiles",
	"type": "object",
	"properties": {
		"username": {
			"title": "Username",
			"type": "string"
		},
		"name": {
			"title": "Name",
			"type": "string"
		},
		"phone": {
			"$ref": "#/definitions/Phone"
		},
		"mail": {
			"title": "Mail",
			"type": "string"
		},
		"company": {
			"title": "Company",
			"type": "string"
		},
		"residence": {
			"title": "Residence",
			"type": "string"
		},
		"website": {
			"title": "Website",
			"type": "array",
			"items": {
				"type": "string",
				"minLength": 1,
				"maxLength": 2083,
				"format": "uri"
			}
		},
		"job": {
			"title": "Job",
			"type": "string"
		},
		"address": {
			"title": "Address",
			"type": "string"
		}
	},
	"required": [
		"username",
		"name",
		"phone",
		"mail",
		"website"
	],
	"definitions": {
		"Phone": {
			"title": "Phone",
			"description": "Schema for Phone numbers",
			"type": "object",
			"properties": {
				"home": {
					"title": "Home",
					"type": "string"
				},
				"mobile": {
					"title": "Mobile",
					"type": "string"
				}
			},
			"required": [
				"home",
				"mobile"
			]
		}
	}
}

```

Document Validation

```
Error found in document: aarias
 [
  {
    "loc": [
      "phone",
      "home"
    ],
    "msg": "value is an extension, got \"(932)532-4001x319\"",
    "type": "value_error.extension",
    "ctx": {
      "wrong_value": "(932)532-4001x319"
    }
  },
  {
    "loc": [
      "phone",
      "mobile"
    ],
    "msg": "field required",
    "type": "value_error.missing"
  }
]

```
