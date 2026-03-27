import os

files_to_edit = [
    'backend/main.py',
    'backend/ai_brain.py',
    'frontend/index.html',
    'README.md',
    'docs/DEPLOYMENT_GUIDE.md'
]

for file_path in files_to_edit:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We only want to replace the exact capitalized word 'Aria', leaving 'aria' alone.
        new_content = content.replace('Aria', 'Airah')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated {file_path}")
