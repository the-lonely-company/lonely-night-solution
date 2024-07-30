from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import os
import markdown


document_router = APIRouter(
    prefix='/document',
    tags=['Document']
)


@document_router.get("/terms-and-conditions", response_class=HTMLResponse)
async def get_terms_and_conditions():
    file_path = "documents/night_solution_terms_and_conditions.md"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Terms and Conditions file not found")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    html_content = markdown.markdown(content)
    
    return HTMLResponse(content=html_content)
