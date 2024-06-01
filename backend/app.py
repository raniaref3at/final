from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from backend.ner_model import extract_entities

app = FastAPI()

# Mount static files directory for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Example API endpoint to process text
class TextInput(BaseModel):
    text: str

@app.post("/process_text")
async def process_text(text_input: TextInput):
    entities = extract_entities(text_input.text)
    processed_entities = process_entities(entities, text_input.text)
    return JSONResponse(content={"entities": processed_entities})

def process_entities(entities: list, input_text: str) -> list:
    processed_entities = []
    print (entity)
    for entity in entities:
        # Extract the recognized word from the input text based on start and end indices
        if entity["start"] is not None and entity["end"] is not None:
            word = input_text[entity["start"]:entity["end"]]
        else:
            word = "not found"
        print("Entity:", entity)
        print("Start:", entity["start"])
        print("End:", entity["end"])
        print("Extracted Word:", word)
        # Add the entity to the list with the desired fields
        processed_entity = {
            "entity_group": entity["entity"],
            "score": float(entity["score"]),
            "Disease": word,  # Assign the extracted word to the "Disease" field
            "start": entity["start"],  # Add start position
            "end": entity["end"]  # Add end position
        }
        processed_entities.append(processed_entity)
    return processed_entities






# Serve index.html as the main page
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    with open("frontend/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
