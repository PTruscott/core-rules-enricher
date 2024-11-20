# Core Rules Enricher

This is a project to add basic enrichment to a given Mod Security Core Ruleset Firewall Rules ID.   This will recieve a rule_id via REST and return related NIST 800-53 and ASVS entries.

This project is written in Python 3.13 and FastAPI with the use of TinyDB, a lightweight NoSQL database and the requests package.

### Installation & Running
After cloning the repo, navigate to the root directory and install the required packages in requirements.txt

```pip install -r /path/to/requirements.txt```

After this, you should be able to run 
```fastapi dev main.py```
directly in the terminal.    This will give you the following successful message:

![image](https://github.com/user-attachments/assets/c65cc985-3686-406d-aa7b-6a1a7c5dcbfc)

Navigating to `http://127.0.0.1:8000` should give you a hello world message

![image](https://github.com/user-attachments/assets/23fc8468-c66c-4233-9d89-6fc389ff9a55)

Then navigating to the suggested link will show you the linked NIST 800-53s and ASVS entries as well as additional info about the rule.

Here, 921210 is a good example of a rule with lots of info.

http://127.0.0.1:8000/rule_info/921210

### Responses

Responses are in the format:

```
message: String - Information about the success or failure or the returned response
ASVS: Optional list[dict] - These are the URLs of the ASVS entries.  They come with a confidence value of how close the match is.
NIST: Optional list[dict] - These are the URLs of the NIST entries.  They come with a confidence value of how close the match is.
rule_info: Optional dict - Detailed information about the mapping of data between the rule ID and the final values.  Useful for additional info and debugging
```

### Data flow
Here is a dataflow diagram of the system 

![Core Rule Dataflow](https://github.com/user-attachments/assets/0485c3df-b55b-4421-925d-04aedbbdcb2b)

Here is the existing dataflow through the system, as well as next steps to implement for more consistent mapping as the current mapping can be sparse.
