
from fastapi import FastAPI
from app import model, schemas, utils
from .database import engine, get_db
from .routers import post, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)

app =FastAPI() 
origins = [" *"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

#my_posts = [
 #   {"tittle": "this is the first title", "content": "omoju is a good boy", "id":1 },
  #  {"tittle": "this is the second title", "content": "KT is a good cartel", "id":2 }
#]





#def find_post(id):
 #   for p in my_posts:
  #      if p['id']==id:
   #         return p

#def find_index_post(id):
 #   for i, p in enumerate (my_posts):
  #      if p['id'] == id:
   #         return i


#@app.get("/sql")
#def test_db(db: Session =Depends(get_db)):
    
 #   posts =db.query(model.Post).all()
  #  return {"status": posts}

