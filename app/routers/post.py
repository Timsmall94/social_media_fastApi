from .. database import get_db
from typing import List, Optional
from .. import model, schemas, oauth
from fastapi import Depends, FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session 
from sqlalchemy import func

router = APIRouter(
    prefix="/post",
    tags=['Post']
)


@router.get("/",response_model=List[schemas.PostOUt])
def get_all_Post (db: Session =Depends(get_db), current_user : int=Depends(oauth.get_current_user), search:Optional[str]="", limit:int=10, skip:int = 0):
    #cursor.execute("""SELECT * FROM post """)
    #posts=cursor.fetchall()
    #posts =db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts= db.query(model.Post, func.count(model.Vote.post_id).label("Likes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(
            model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.get('/{id}', response_model=schemas.PostOUt)
def Get_post_by_id (id :str, db: Session =Depends(get_db), current_user: int= Depends(oauth.get_current_user)):
    #cursor.execute("""SELECT * from post where id = %s """, (str(id)))
    #post = cursor.fetchone() this is for sql    10797422832
    #post = find_post(id)
    #post=db.query(model.Post).filter(model.Post.id ==id).first()
    post = db.query(model.Post, func.count(model.Vote.post_id).label("Likes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(
            model.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} not found")
    
    return post
 
@router.get('/latest', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def Get_Latest (db: Session =Depends(get_db), current_user: int= Depends(oauth.get_current_user)):
    
    post =db.query(model.Post).all()
    postLatest = post[len (post)-1]
    return postLatest

@router.post ('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post ( post:schemas.PostBase, db: Session =Depends(get_db), current_user : int=Depends(oauth.get_current_user)):
    
    print(current_user.id)
    new_post=model.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def Update_post(id:str, updated_post:schemas.PostBase, db: Session =Depends(get_db), current_user: int=Depends(oauth.get_current_user)):
    #cursor.execute("""UPDATE post SET 
      #                  title= %s, content=%s, published=%s 
      #                  WHERE id =%s Returning *""",
     #                   (post.title, post.content, post.published, (str(id))))

   # updated_post = cursor.fetchone()#index = find_index_post(id)
    #conn.commit()
    post_query =db.query(model.Post).filter(model.Post.id == id)
    post =post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} do not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"you are not autorize to edit this post")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #new_post_dict = post.dict()
    #new_post_dict['id'] = id
    #my_posts[index]= new_post_dict
    return post_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete(id:str, db: Session =Depends(get_db), current_user : int=Depends(oauth.get_current_user)):
   # cursor.execute(""" DELETE FROM post WHERE id= %s returning * """,(str(id)))
   # delete_post = cursor.fetchone()
   # conn.commit()
    #deleting post
    #find the index in the arrary that has required ID
    # my_post.pop(index)
    #index = find_index_post(id)

    post_query=db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first() 
    if post== None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
         detail= f"post with id: {id} do not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"you are not autorize to delete this post")

    post_query.delete(synchronize_session=False)
    db.commit # to make changes
    #my_posts.pop(delete_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

