
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, model, utils, oauth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session =Depends(database.get_db)):

#OAuth2PasswordRequestForm
#{
  #"username":"whatever you input"
 # "password": "what ever the user input"
#}
#OAuth2PasswordRequestFormdoesnt care what the username ot password is, it only save the what yu swnd as username into iter

# now we can access all the attempted login credentials witht the user_credentials // we going to make request to our database specificlly our "user" table to retrieve the userbase.emai;
   
    Newuser = db.query(model.User).filter(model.User.email == user_credentials.username).first()
      
    if not Newuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid creditial email")


    if not utils.verify(user_credentials.password, Newuser.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                            detail=f"Invalid creditial password"
                            )
    access_token = oauth.create_access_token(data={"user_id":Newuser.id})
    # {"user_id":Newuser.id} this get the id of the user and turn it to a stringß

    return {"access_token" :access_token, "token_type":"bearer"}
    # the access token we return in the above return statement is the token generated when a user login using the login path
