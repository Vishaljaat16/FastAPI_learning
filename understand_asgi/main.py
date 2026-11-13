
import asyncio
import logging
import time

from fastapi import FastAPI, Request
from starlette.types import ASGIApp, Scope, Receive, Send

# --------------------------------------------------
# STEP 1: Configure logging
# --------------------------------------------------

logging.basicConfig( 
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

logger = logging.getLogger("ASGI")


# --------------------------------------------------
# STEP 2: Custom ASGI Middleware
# --------------------------------------------------

class ASGILifecycleMiddleware:

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ):

        # Only trace HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()

        # STAGE 1: SCOPE
        # Uvicorn provides request information here.

        logger.info(
            f"[SCOPE] Method={scope['method']} "
            f"Path={scope['path']} "
            f"HTTP={scope['http_version']}"
        )

        # STAGE 2: RECEIVE
        # Observe incoming ASGI events.

        async def receive_wrapper():

            message = await receive()

            logger.info(
                f"[RECEIVE] Event={message['type']}"
            )

            if message["type"] == "http.disconnect":
                logger.info("[DISCONNECT] Client disconnected")

            return message

        # STAGE 3: SEND
        # Observe outgoing ASGI response events.

        async def send_wrapper(message):

            logger.info(
                f"[SEND] Event={message['type']}"
            )

            if message["type"] == "http.response.start":
                logger.info(
                    f"[RESPONSE] Status={message['status']}"
                )

            await send(message)

        logger.info("[LIFECYCLE] Request processing started")

        # Forward request to FastAPI application.
        await self.app(
            scope,
            receive_wrapper,
            send_wrapper
        )

        duration = time.perf_counter() - start_time

        logger.info(
            f"[LIFECYCLE] Request completed "
            f"in {duration:.4f} seconds"
        )


# --------------------------------------------------
# STEP 3: Create FastAPI application
# --------------------------------------------------

app = FastAPI()

# Register custom ASGI middleware
app.add_middleware(ASGILifecycleMiddleware)


# --------------------------------------------------
# STEP 4: Event loop demonstration
# --------------------------------------------------

async def background_task(task_name: str):

    logger.info(f"[TASK] {task_name} started")

    # Simulates asynchronous I/O operation.
    await asyncio.sleep(2)

    logger.info(f"[TASK] {task_name} completed")

    return f"{task_name} finished"


# --------------------------------------------------
# STEP 5: Practical API endpoint
# --------------------------------------------------

@app.get("/hello")
async def hello():

    logger.info("[ENDPOINT] Hello endpoint executed")

    return {
        "message": "Hello from FastAPI",
        "lifecycle": "ASGI"
    }


# --------------------------------------------------
# STEP 6: Event loop practical endpoint
# --------------------------------------------------

@app.get("/tasks")
async def execute_tasks():

    logger.info("[ENDPOINT] Starting async tasks")

    # Both tasks can make progress concurrently.
    result1, result2 = await asyncio.gather(
        background_task("Task-1"),
        background_task("Task-2")
    )

    return {
        "task_1": result1,
        "task_2": result2
    }


# --------------------------------------------------
# STEP 7: Request information endpoint
# --------------------------------------------------

@app.get("/request-info")
async def request_info(request: Request):

    return {
        "method": request.method,
        "url": str(request.url),
        "client": str(request.client),
        "headers": dict(request.headers)
    }


# --------------------------------------------------
# STEP 8: Root endpoint
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "message": "ASGI Lifecycle Demo",
        "available_routes": [
            "/hello",
            "/tasks",
            "/request-info"
        ]
    }
