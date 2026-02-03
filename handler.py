# this will keep it running
# print("hihi")
import os
import time
import runpod


def handler(job):
    """
    Basic handler that:
    - Reads MODE env var: "success" or "fail"
    - Waits for a single configurable TIMEOUT (seconds)
    - Either returns a JSON payload (success) or raises an exception (fail)
    """

    mode = os.getenv("MODE", "success").lower()
    timeout = float(os.getenv("TIMEOUT", "1"))  # single timeout env var

    # Simulate work taking some time
    time.sleep(timeout)

    if mode == "success":
        # Normal application-level success payload
        return {
            "ok": True,
            "mode": "success",
            "timeout_seconds": timeout,
            "message": "Simulated successful job.",
            "input": job.get("input", {}),
        }

    elif mode == "fail":
        # Unhandled exception → Runpod will mark the job as FAILED
        raise RuntimeError(
            f"Simulated unhandled error after {timeout} seconds in fail mode."
        )

    # Treat unexpected mode as an application-level error (still a completed job)
    return {
        "ok": False,
        "mode": mode,
        "timeout_seconds": timeout,
        "error": {
            "code": "INVALID_MODE",
            "message": "MODE env var must be 'success' or 'fail'.",
        },
    }


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
