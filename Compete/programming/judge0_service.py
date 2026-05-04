import requests
import base64
from decouple import config

class Judge0Service:
    """Service to interact with self-hosted Judge0 API using Base64 encoding"""
    
    LANGUAGE_MAP = {
        'Python': 71,
        'JavaScript': 63,
        'Java': 62,
        'C++': 54,
        'C': 50,
        'Linux CLI': 46,
    }

    def __init__(self):
        # Default to localhost if environment variable is not set
        self.api_url = config('JUDGE0_API_URL', default='http://judge0_server:2358')

    def _encode(self, data):
        """Helper to convert string to base64 encoded string"""
        if data is None:
            return ""
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def _decode(self, data):
        """Helper to convert base64 encoded string back to plain text"""
        if not data:
            return ""
        try:
            return base64.b64decode(data).decode('utf-8')
        except Exception:
            return data # Return as is if decoding fails

    def get_headers(self):
        """Generate request headers"""
        return {'Content-Type': 'application/json'}

    def get_language_id(self, language):
        """Get Judge0 language ID from language name"""
        return self.LANGUAGE_MAP.get(language, 71)

    def execute_code(self, code, language='Python', stdin=''):
        """Execute code using Base64 encoding and return decoded results"""
        language_id = self.get_language_id(language)
        
        # All source code and stdin MUST be base64 encoded when base64_encoded=true
        payload = {
            'language_id': language_id,
            'source_code': self._encode(code),
            'stdin': self._encode(stdin),
        }

        try:
            response = requests.post(
                f"{self.api_url}/submissions",
                params={
                    "base64_encoded": "true",
                    "wait": "true"
                },
                json=payload,
                headers=self.get_headers(),
                timeout=15
            )
            response.raise_for_status()
            result = response.json()

            # Decode the outputs from Judge0 as they arrive base64 encoded
            return {
                'success': True,
                'stdout': self._decode(result.get('stdout')),
                'stderr': self._decode(result.get('stderr')),
                'compile_output': self._decode(result.get('compile_output')),
                'message': self._decode(result.get('message')),
                'status': result.get('status', {}).get('description', 'Unknown'),
                'time': result.get('time'),
                'memory': result.get('memory'),
                'exit_code': result.get('exit_code')
            }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Code execution timed out (15 second limit)'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Failed to connect to Judge0: {str(e)}'
            }
