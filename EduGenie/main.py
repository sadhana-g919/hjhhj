from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from qna import answer_question
from explation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="AI-powered Learning Assistant",
    version="1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")


# =========================
# DEMO MODE
# =========================

DEMO_MODE = True


class TextRequest(BaseModel):
    text: str


class QuestionRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    text: str
    count: int = 3


class LearningRequest(BaseModel):
    topic: str
    level: str = "beginner"


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/qa")
def qa(request: QuestionRequest):

    if DEMO_MODE:
        return {
            "answer": (
                "Photosynthesis is the process by which green plants "
                "prepare their own food using sunlight, carbon dioxide, "
                "and water. Oxygen is released as a by-product."
            )
        }

    try:
        return {"answer": answer_question(request.question)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/explain")
def explain(request: TextRequest):

    if DEMO_MODE:
        return {
            "explanation": (
                "Photosynthesis is the process through which green plants "
                "make their own food.\n\n"
                "Important Points:\n"
                "1. Plants use sunlight as an energy source.\n"
                "2. Carbon dioxide is taken from the air.\n"
                "3. Water is absorbed through the roots.\n"
                "4. Chlorophyll helps the plant capture sunlight.\n"
                "5. Oxygen is released during the process.\n\n"
                "Example:\n"
                "A green leaf uses sunlight, water and carbon dioxide "
                "to produce food for the plant."
            )
        }

    try:
        return {"explanation": explain_topic(request.text)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/quiz")
def quiz(request: QuizRequest):

    if DEMO_MODE:
        return {
            "quiz": (
                "1. What is the main source of energy for photosynthesis?\n"
                "A) Water\n"
                "B) Sunlight\n"
                "C) Oxygen\n"
                "D) Soil\n"
                "Answer: B) Sunlight\n\n"

                "2. Which gas is used by plants during photosynthesis?\n"
                "A) Oxygen\n"
                "B) Nitrogen\n"
                "C) Carbon dioxide\n"
                "D) Hydrogen\n"
                "Answer: C) Carbon dioxide\n\n"

                "3. Which pigment helps plants absorb sunlight?\n"
                "A) Chlorophyll\n"
                "B) Haemoglobin\n"
                "C) Melanin\n"
                "D) Keratin\n"
                "Answer: A) Chlorophyll"
            )
        }

    try:
        return {"quiz": generate_quiz(request.text, request.count)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/summarize")
def summarize(request: TextRequest):

    if DEMO_MODE:
        return {
            "original_text": request.text,
            "summary": (
                "Photosynthesis is the process in which green plants "
                "use sunlight, water and carbon dioxide to make food. "
                "Oxygen is released during this process."
            )
        }

    try:
        return {
            "original_text": request.text,
            "summary": summarize_text(request.text)
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/learn/recommendations")
def learning_recommendations(request: LearningRequest):

    if DEMO_MODE:
        return {
            "learning_path": (
                "Learning Path for " + request.topic + "\n\n"
                "Step 1: Learn the basic definition.\n"
                "Step 2: Understand the important concepts.\n"
                "Step 3: Study a simple example.\n"
                "Step 4: Practice with quiz questions.\n"
                "Step 5: Revise the topic and test your understanding."
            )
        }

    try:
        return {
            "learning_path": get_learning_recommendations(
                request.topic,
                request.level
            )
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/api")
def api_status():
    return {
        "message": "EduGenie API is running!",
        "features": [
            "Question & Answer",
            "Explain Topic",
            "Generate Quiz",
            "Summarize Notes",
            "Learning Path"
        ]
    }