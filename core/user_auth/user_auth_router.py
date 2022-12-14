from core.user_auth import schemas, models
from core.utils.database_utils import get_db, verify_password,get_password_hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.user_auth.oauth import create_access_token,get_current_user,create_refresh_token
from core.utils import token_utils, database_utils, mailer_utils
from fastapi import APIRouter, status, HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from core.config import settings 




frontend_url = settings.frontend_url


auth = APIRouter(prefix = "/auth", tags=["Authentication & Authorization"])









@auth.post("/register/", status_code=status.HTTP_201_CREATED, response_model=schemas.RegistrationResponse)
async def registration(new_user:schemas.UserCreate,db:Session = Depends(get_db)):


    user_check = db.query(models.User).filter(models.User.email == new_user.email).first()

    if user_check is not None:
        raise HTTPException(detail="User already exist, Please Login to continue.", status_code=status.HTTP_409_CONFLICT)




    new_user.password = database_utils.get_password_hash(new_user.password)
    #because I did not create mailer.
    new_user.is_verified = True 



    create_user = models.User(**new_user.dict())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)

    # verify email
    # new_user_token = token_utils.create_token(create_user.email)
    # generate mail link 
    # send the link with template to the user.

    return {
        "message": "User Registered sucessfully",
        "data": create_user, 
        "status": status.HTTP_201_CREATED
    }
    


@auth.post("/login/", status_code= status.HTTP_200_OK, response_model=schemas.LoginResponse)
def login(user_login:OAuth2PasswordRequestForm= Depends(),db:Session = Depends(get_db)):

    user_check = db.query(models.User).filter(models.User.email == user_login.username).first()

    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # check if account has been verified.
    password_check = database_utils.verify_password(user_login.password, user_check.password)

    if password_check is False:
        raise HTTPException(detail="Incorrect User email/password", status_code=status.HTTP_409_CONFLICT)
    
    data = {}
    
    access_token =create_access_token(jsonable_encoder(user_check))
    data["refresh_token"] = create_refresh_token(jsonable_encoder(user_check))
    data["data"] = user_check


    return {
        "access_token": access_token,
        "token_type":"Bearer",
        "message": "User Logged in Sucessfully.",
        "data": data,
        "status": status.HTTP_200_OK
    }



@auth.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.ResponseUser)
def get_user(current_user:dict = Depends(get_current_user)):



    return current_user


@auth.post("/invite/",status_code = status.HTTP_201_CREATED, response_model= schemas.ContractualMessageRespsonse)
async def create_invite(invite:schemas.ContractualInvitesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    invite_check = db.query(models.ContractualInvites).filter(models.ContractualInvites.email_invited ==invite.email_invited).first()

    if invite_check:
        raise HTTPException(detail="Invite has been sent to this user.", status_code=status.HTTP_409_CONFLICT)
    
    invite = invite.dict()
    invite["inviter_id"] = current_user.id

    new_invite = models.ContractualInvites(**invite)
    db.add(new_invite)
    db.commit()
    db.refresh(new_invite)

    # await
    token = token_utils.create_token(new_invite.email_invited) 
    body_data = {
        "inviter": new_invite.user.firstname,
        "url": f"{frontend_url}/contract-user/invite/{token}/"
    }
    # await mailer_utils.send_mail(mail_subject="Hallo, Invite from PayBills",
    # recipient=[new_invite.email_invited],data=body_data, template="user/new_invites.html")
    print(body_data)

    return {
        "message": "Invite has been sent to the invited party",
        "data": new_invite,
        "status":status.HTTP_201_CREATED
    }



@auth.patch("/invite/{token}",status_code = status.HTTP_202_ACCEPTED)
async def create_invite(token:str,invite:schemas.UpdateContractualInvites, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    mail_invited = token_utils.invite_verify_token(token)

    invite_check = db.query(models.ContractualInvites).filter(models.ContractualInvites.email_invited == mail_invited)

    if not invite_check.first():
        raise HTTPException(detail="No Invite is attched", status_code=status.HTTP_404_NOT_FOUND)
    redirect = False
    invite_check_ = invite_check.first()
    invite = invite.dict(exclude_unset= True)
    if invite["confirmation"] is True:
        for key, values in invite.items():
            setattr(invite_check_,key, values)
        redirect = True

    elif invite["confirmation"] is False:
        invite_check.delete()
    
    # status to the person who invited.
    db.commit()

    

    return {
        "message": "Invite has been acted upon",
        "redirect": redirect,
        "status":status.HTTP_202_ACCEPTED
    }



