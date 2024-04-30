import base64

# Your UserData content
user_data = '''#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &'''

# Encode the UserData content into Base64
encoded_user_data = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')

# Print the encoded UserData for verification
print(encoded_user_data)

# Now you can update your YAML file with the encoded UserData
