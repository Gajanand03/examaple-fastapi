from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db
from app.routers import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user), 
                    Limit : int = 10, skip:int=0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")
                    ).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True
                    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return post

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post:schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INsSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                 (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # conn.commit()
    post = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    print(current_user.email)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")
                    ).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True
                    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found!")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",
    # (post.title,post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    post = updated_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()