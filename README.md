# How to Use This PDF Parsing Tool

API key available upon request or follow steps:
https://docs.cloud.llamaindex.ai/llamacloud/getting_started/api_key \
Input api key in .env file:
```
LLAMA_CLOUD_API=llx-{{key}}
```
Installation
```
pip install -r requirements.txt
```

Run code input into console: 
```
# with provided pdf
python tool.py 3360.pdf

# with another pdf
python tool.py /path/to/pdf
```

This script will parse every pdf document accurately.

I converted the PDF into Markdown, and my code processes it to extract sections, subsections, and content.

I also have an open-source solution that doesn't require API calls, but it does need an LLM installed locally due to the document's complexity. Unfortunately, I don't have the storage or GPU support to run it on my machine.

Here is a example of the output when putting in 3360.pdf:

![image](images/Screenshot1.png)
![image](images/Screenshot2.png)
