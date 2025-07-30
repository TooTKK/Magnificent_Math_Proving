import os
import asyncio
import httpx

async def text_to_latex(prompt, api_key):
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    payload = {
        "model": "doubao-seed-1-6-250615",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "thinking": {"type": "disabled"}
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "max_tokens": "512"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]
            return content
    except Exception as e:
        print("Text generation request failed: ", e)
        return None


if __name__ == "__main__":
    prompt = f"Convert the following content into LaTeX format. Only output valid LaTeX:" + input("Enter the math content you want to convert to LaTeX: ")
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("API Key not found. Please set the ARK_API_KEY environment variable.")
    else:
        result = asyncio.run(text_to_latex(prompt, api_key))
        if result:
            print("\nLaTeX Output: \n", result)
