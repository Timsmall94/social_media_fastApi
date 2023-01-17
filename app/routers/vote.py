from .. import model, schemas, oauth, database
from fastapi import Depends,HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session 

router =APIRouter(
    prefix= "/vote",
    tags= ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote:schemas.Vote, db: Session =Depends(database.get_db), current_user : int=Depends(oauth.get_current_user)):
   # print(type(current_user.id))
    #print(type(vote.post_id))
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {vote.post_id} does not exist")
    
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id ==vote.post_id , model.Vote.user_id ==current_user.id )
    found_vote=vote_query.first()
    if (vote.dir == 1):
       
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f'user{current_user.id} has already voted on the post {vote.post_id}')
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succefully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"succefully deleted Vote"}
        
"""
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth.get_current_user)):
    print('Testing____')
    post = db.query(model.Post).filter_by(id= vote.post_id).one()
    print(post)
   if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully Added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted vote"}"""