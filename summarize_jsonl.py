import json
from collections import Counter
from datetime import datetime

file_path = r"C:\Users\freshair\.claude\projects\E--The-Human-Algorithm-T2-agent\05a8f4a8-7d99-4d19-b9f7-b4c2bc7c176a.jsonl"

def summarize_jsonl(path):
    user_requests = []
    assistant_actions = []
    files_modified = set()
    snapshots = 0
    start_time = None
    end_time = None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    
                    # Timestamp tracking
                    ts_str = data.get('timestamp')
                    if ts_str:
                        # Simplified timestamp parsing if needed, or just keep string
                        if not start_time: start_time = ts_str
                        end_time = ts_str

                    # Message tracking
                    if 'message' in data:
                        msg = data['message']
                        role = msg.get('role')
                        content = msg.get('content', [])
                        
                        text_content = ""
                        if isinstance(content, list):
                            for part in content:
                                if part.get('type') == 'text':
                                    text_content += part.get('text', '')
                                elif part.get('type') == 'tool_use':
                                    assistant_actions.append(f"Tool Use: {part.get('name')}")
                        elif isinstance(content, str):
                            text_content = content

                        if role == 'user':
                            # Simplify user request log
                            if text_content:
                                user_requests.append(text_content[:200].replace('\n', ' '))
                        elif role == 'assistant':
                            # Just iterate actions above
                            pass

                    if 'toolUseResult' in data:
                        res = data['toolUseResult']
                        if isinstance(res, dict):
                            if res.get('type') == 'create' or res.get('type') == 'write':
                                files_modified.add(res.get('filePath', 'unknown'))
                        elif isinstance(res, str):
                             # Sometimes it might just be the output string
                             pass                    
                    if data.get('type') == 'file-history-snapshot':
                        snapshots += 1

                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print("File not found.")
        return

    with open("e:\\eva\\full_user_requests.md", "w", encoding="utf-8") as out_req:
        out_req.write(f"# All User Requests ({len(user_requests)} Total)\n\n")
        for i, req in enumerate(user_requests, 1):
            out_req.write(f"{i}. {req}\n")
            
    print(f"Full list of {len(user_requests)} requests written to e:\\eva\\full_user_requests.md")

    with open("e:\\eva\\jsonl_summary.md", "w", encoding="utf-8") as out:
        out.write(f"# Summary of {path}\n")
        out.write(f"- **Time Range:** {start_time} to {end_time}\n")
        out.write(f"- **Total Interactive Turns:** {len(user_requests)}\n")
        out.write(f"- **Snapshots Taken:** {snapshots}\n\n")
        
        out.write("## Files Created/Modified\n")
        for file in sorted(files_modified):
            out.write(f"- {file}\n")

        out.write("\n## Key User Requests (First 5)\n")
        for i, req in enumerate(user_requests[:5], 1):
            out.write(f"{i}. {req}\n")
            
        out.write("\n## Assistant Tool Actions\n")
        action_counts = Counter(assistant_actions)
        for action, count in action_counts.items():
            out.write(f"- {action}: {count}\n")
    
    print("Summary written to e:\\eva\\jsonl_summary.md")

if __name__ == "__main__":
    summarize_jsonl(file_path)
