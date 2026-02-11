import json
import uuid

input_file = r'c:\Users\leitmotiv\Downloads\wp_post_ideas.json'
output_file = r'c:\Users\leitmotiv\Downloads\wp_post_ideas.json_cleaned.json'

def clean_n8n_workflow(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    keys_to_remove = ['active', 'id', 'tags', 'pinData', 'versionId', 'settings', 'meta']
    for key in keys_to_remove:
        if key in workflow:
            del workflow[key]


    if 'nodes' in workflow:
        for node in workflow['nodes']:
            node['id'] = str(uuid.uuid4())

            if 'credentials' in node:
                del node['credentials']

            if 'webhookId' in node:
                del node['webhookId']


            if 'disabled' in node and node['disabled'] is False:
                del node['disabled']

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)

    print(f"Cleaned workflow saved to {output_path}")

if __name__ == "__main__":
    clean_n8n_workflow(input_file, output_file)