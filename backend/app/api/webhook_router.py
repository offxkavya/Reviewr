import httpx
from fastapi import APIRouter, Request, BackgroundTasks
from app.services.openai_service import review_code

router = APIRouter()

async def process_pull_request(repo_full_name: str, pr_number: int, owner: str, repo: str):
    # In a real app, you'd use a GitHub PAT or Installation Token
    # For now, we simulate fetching the diff
    diff_url = f"https://patch-diff.githubusercontent.com/raw/{repo_full_name}/pull/{pr_number}.diff"
    async with httpx.AsyncClient() as client:
        resp = await client.get(diff_url)
        if resp.status_code == 200:
            diff_content = resp.text
            # Trigger the AI review
            try:
                review_results = review_code(diff_content, "diff")
                print(f"Processed PR #{pr_number} for {repo_full_name}")
                print(review_results)
            except Exception as e:
                print(f"Failed to review PR #{pr_number}: {e}")
        else:
            print(f"Failed to fetch diff for PR #{pr_number}")

@router.post("")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    action = payload.get("action")
    
    # We only care about opened or synchronized PRs
    if "pull_request" in payload and action in ["opened", "synchronize"]:
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]
        owner = payload["repository"]["owner"]["login"]
        repo = payload["repository"]["name"]
        
        background_tasks.add_task(process_pull_request, repo_full_name, pr_number, owner, repo)
        
    return {"status": "received"}
