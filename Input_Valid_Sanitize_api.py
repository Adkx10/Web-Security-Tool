from flask import Flask, request, jsonify
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Helpers
def is_valid_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except:
        return False
    
def sanitize_message(value: str) -> str:
    sanitized = re.sub(r'<.*?>', '', value)
    return sanitized.strip()

# Validation endpoint
@app.route("/validate", methods=["POST"])
def validate_input():
    data = request.json
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    age = str(data.get("age", "")).strip()
    message = str(data.get("message", "")).strip()
    
    results = {}

    # Simple email regex
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not email:
        results["email"] = {"is_valid": False, "result": "Email is required"}
    else:
        is_valid = re.match(email_regex, email) is not None
        results["email"] = {"is_valid": is_valid, "result": "valid email" if is_valid else "Invalid email format"}

    # Simple name validation: only letters and spaces, at least 2 chars
    name_regex = r"^[A-Za-z\s]{2,}$"
    if not name:
        results["name"] = {"is_valid": False, "result": "Name is required"}
    else:
        is_valid = re.match(name_regex, name) is not None
        results["name"] = {"is_valid": is_valid, "result": "valid name" if is_valid else "Invalid name (letters/spaces only, min 2 chars)"}
    
    # Simple age validation: optional and only takes age between 18 - 120
    if age == "":
        results["age"] = {"is_valid": True, "result": "Optional (not provided)"}
    else:
        try:
            age_val = int(age)
            if 18 < age_val <= 120:
                results["age"] = {"is_valid": True, "result": age_val}
            else:
                results["age"] = {"is_valid": False, "result": "Invalid Age (must be between 18 and 120)"}
        except ValueError:
            results["age"] = {"is_valid": False, "result": "Invalid input, must be a number"}
     
    # Simple message validation
    clean_msg = sanitize_message(message)
    if not clean_msg:
        results["message"] = {"is_valid": False, "result": "Optional (not provided)"}
    elif is_valid_url(clean_msg):
        results["message"] = {"is_valid": True, "result": f"Valid URL: {clean_msg}"}
    else:
        results["message"] = {"is_valid": True, "result": f"Plain text: {clean_msg}"}
            
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000, debug=True)