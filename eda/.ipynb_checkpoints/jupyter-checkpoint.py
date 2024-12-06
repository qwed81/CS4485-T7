from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

# Define the backend server URL
backend_url = "http://localhost:8888"

@app.route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(req: Request):
    # Construct the full URL for the backend request
    url = backend_url + req.url.path
    print(url)

    # Create an HTTPX client to forward the request
    async with httpx.AsyncClient() as client:
        body = await req.body()

        # Forward the request to the backend server
        backend_response = await client.request(
            method=req.method,
            url=url,
            headers=req.headers,
            content=body
        )

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=dict(backend_response.headers)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
