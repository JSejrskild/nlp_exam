'''
Model used for this summarisation is Googles Pegasus
'''

from transformers import pipeline
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Pick model
model_name = "google/pegasus-xsum"

# Load pretrained tokenizer
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

example_text = ""

print('Original Document Size:',len(example_text))
# Define PEGASUS model
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
# Create tokens
tokens = pegasus_tokenizer(example_text, truncation=True, padding="longest", return_tensors="pt")

# Generate the summary
encoded_summary = pegasus_model.generate(**tokens)

# Decode the summarized text
decoded_summary = pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)

# Print the summary
print('Decoded Summary :',decoded_summary)
