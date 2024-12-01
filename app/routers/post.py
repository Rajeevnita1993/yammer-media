from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# my_posts = [{"title": "First title",
#         "content": "Content from First post",
#         "published": True,
#         "rating": 1,
#         "id": 1},
#         {"title": "Second title",
#         "content": "Content from Second post",
#         "published": True,
#         "rating": 2,
#         "id": 2}]

# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post

# def find_index_post(id):
#     for i, post in enumerate(my_posts):
#         if post['id'] == id:
#             return i

#@router.get("/", response_model = List[schemas.Post])
@router.get("/", response_model = List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    #print(f"limit is {limit}")
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # If you want to get posts specific to owner_id
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)

    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(f"current_user is {current_user.id}")
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#@router.get("/{id}", response_model = schemas.Post)
@router.get("/{id}", response_model = schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id),))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    # Validate whether extracted post is specific to particular owner id
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts where id = %s returning * """, (str(id),))
    # deleted_posts = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s returning * """, 
    #         (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


