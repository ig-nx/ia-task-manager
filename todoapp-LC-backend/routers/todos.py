from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import crud
from database import SessionLocal
# LANGCHAIN 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

router = APIRouter(
    prefix="/todos"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo)
    return todo

@router.get("", response_model=List[schemas.ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return res
     
    


# LANGCHAIN
# Esto es un ejemplo de cómo usar LangChain para crear cadenas de resumen y generación de poemas utilizando el modelo GPT-4o-mini. Se define una cadena de resumen que toma un texto de entrada y devuelve un resumen, y una cadena de generación de poemas que toma el nombre de un todo y genera un poema corto basado en ese nombre.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Summarize chain using LCEL - Resume un texto dado utilizando el modelo GPT-4o-mini. El prompt se define para solicitar un resumen del texto proporcionado, y la cadena se construye combinando el prompt con el modelo y un parser de salida que convierte la respuesta en una cadena de texto simple. La función `summarize_text` se expone como un endpoint de la API que recibe un texto y devuelve su resumen.
summarize_prompt = ChatPromptTemplate.from_template(
    "Resume el siguiente texto en espanol: {text}"
)
summarize_chain = summarize_prompt | llm | StrOutputParser()

@router.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.invoke({"text": text})
    return {'summary': summary}

# Write poem chain using LCEL - Escribe un poema corto con el siguiente texto: {text}. El prompt se define para solicitar la creación de un poema basado en el texto proporcionado, y la cadena se construye combinando el prompt con el modelo y un parser de salida que convierte la respuesta en una cadena de texto simple. La función `write_poem_by_id` se expone como un endpoint de la API que recibe el ID de un todo y devuelve un poema generado.
write_poem_prompt = ChatPromptTemplate.from_template(
    "Escribe un poema corto en espanol con el siguiente texto: {text}"
)
write_poem_chain = write_poem_prompt | llm | StrOutputParser()


@router.post("/write-poem/{id}")
async def write_poem_by_id(id: int, db: Session = Depends(get_db)):
    try:
        # Obtenemos el todo por su ID
        todo = crud.read_todo(db, id)
        if todo is None:
            raise HTTPException(status_code=404, detail="todo no encontrado")
        
        # Generamos el poema utilizando el nombre del todo como texto de entrada para la cadena de generación de poemas
        poem = write_poem_chain.invoke({"text": todo.name})
        return {"poem": poem}
    except HTTPException:
        raise
    except Exception as e:
        # Manejamos cualquier otra excepción que pueda ocurrir durante el proceso y devolvemos un error 500 con el mensaje de la excepción
        raise HTTPException(
            status_code=500, 
            detail=f"Error al generar el poema: {str(e)}"
        )

# LCEL (Language Chain Execution Language) es un lenguaje de programación diseñado para facilitar la creación y ejecución de cadenas de procesamiento de lenguaje natural utilizando modelos de lenguaje como GPT-4o-mini. Permite a los desarrolladores definir flujos de trabajo complejos combinando diferentes componentes, como prompts, modelos y parsers, de manera modular y reutilizable. En este ejemplo, se utilizan LCEL para crear cadenas que resumen textos y generan poemas basados en el nombre de un todo, demostrando cómo se pueden integrar fácilmente estas funcionalidades en una API utilizando FastAPI.

