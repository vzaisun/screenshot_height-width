from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = FastAPI()

# Allow requests from the specified origin
origins = [
    "https://screenshot-theta-ten.vercel.app",
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class URLInput(BaseModel):
    url: str

@app.post('/dimensions')
async def dimensions(data: URLInput):
    url = data.url

    if not url:
        return JSONResponse({'error': 'URL is required'}, status_code=400)

    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        driver.get(url)

        width = driver.execute_script("return document.body.scrollWidth")
        height = driver.execute_script("return document.body.scrollHeight")
        
        driver.quit()

        return JSONResponse({'width': width, 'height': height})

    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)
