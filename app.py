import os
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal, User, Disease
from schema import UserIn, UserOut, DiseaseIn, DiseaseOut
import uvicorn
# import tensorflow as tf
# from PIL import Image

app = FastAPI()

# Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Route to get all users
@app.get("/users")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Route to create a new user
@app.post("/users")
def create_user(user: UserIn, image: UploadFile = File(None), db: Session = Depends(get_db)):
    db_user = User(**user.dict())

    if image:
        file_path = os.path.join("images", image.filename)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        db_user.image_url = file_path

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserOut.from_orm(db_user)

# Route to get a single user by id
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.from_orm(user)

# Route to update a user by id
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserIn, image: UploadFile = File(None), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)

    if image:
        file_path = os.path.join("images", image.filename)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        update_data['image_url'] = file_path

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()

    return UserOut.from_orm(db_user)

# Route to serve the user's image
@app.get("/images/{image}")
async def get_image(image: str):
    return FileResponse(f"images/{image}")

# Route to get all diseases
@app.get("/diseases")
def get_diseases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    diseases = db.query(Disease).offset(skip).limit(limit).all()
    return diseases

# Route to get a single disease by id
@app.get("/diseases/{disease_id}")
def read_disease(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    return disease


# @app.get('/classify')
# def classify_disease(image: UploadFile = File(None), db: Session = Depends(get_db)):

#     model_path = "models/skinvision.h5"
#     model = tf.keras.models.load_model(model_path, compile=False)
    
#     img = Image.open(image.file).convert("RGB")
#     img = img.resize((125, 100)) 
#     img_array = tf.keras.preprocessing.image.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)  
#     img_array /= 255.0  

#     prediction = model.predict(img_array)[0]

#     return db.query(Disease).filter(Disease.shortcut == prediction).first()

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host='0.0.0.0')