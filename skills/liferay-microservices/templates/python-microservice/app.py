import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Liferay Demo Agent Microservice REST Provider")

class ObjectActionPayload(BaseModel):
    companyId: int
    eventType: str
    objectDefinitionKey: str
    objectEntryId: int
    values: Dict[str, Any]

class WorkflowActionPayload(BaseModel):
    companyId: int
    entryClassName: str
    entryClassPK: int
    userId: int
    workflowContext: Dict[str, Any]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/object-action")
async def handle_object_action(payload: ObjectActionPayload):
    print(f"Received Object Action [Event: {payload.eventType}] for ID {payload.objectEntryId}")
    try:
        # IMPLEMENT BUSINESS LOGIC HERE
        # Example: if payload.eventType == "onAfterAdd": ...
        
        return {
            "status": "success",
            "message": f"Processed object action {payload.eventType} successfully."
        }
    except Exception as e:
        print(f"Error handling object action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow-action")
async def handle_workflow_action(payload: WorkflowActionPayload):
    print(f"Received Workflow Action for entry {payload.entryClassPK} (Class: {payload.entryClassName})")
    try:
        transition = payload.workflowContext.get("transitionName", "unknown")
        print(f"Workflow transitioning via: {transition}")
        
        # IMPLEMENT TRANSITION LOGIC HERE
        
        return {
            "status": "success",
            "message": f"Processed workflow transition '{transition}' successfully."
        }
    except Exception as e:
        print(f"Error handling workflow action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
