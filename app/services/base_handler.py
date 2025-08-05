from model.domain.url_model import UrlModel
import secrets
from datetime import datetime, timedelta
from db.url_uow import UrlShortenerUnitofWork
from model.serializers import URLCreate,  ShortURLResponse
from loguru import logger

def create_unique_short_code() -> str:
    """Generates a unique 7-character short code."""
    # A short code of 7 characters gives over 3.5 trillion unique combinations
    # using a base62 character set (a-z, A-Z, 0-9).
    length = 7
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    

    with UrlShortenerUnitofWork() as uow:
        while True:
            short_code = ''.join(secrets.choice(charset) for _ in range(length))
            logger.debug(f"creating shor_code for {short_code}")
            # Check if the generated short code already exists in the database
            if not uow.url_shotner_repository.get_by_short_code(short_code=short_code):
                return short_code

def create_short_url(url: URLCreate) -> ShortURLResponse:
    """Creates a new entry in the database for the shortened URL."""
    logger.debug(f"Getting url from {url}")
    short_code = create_unique_short_code()
    logger.debug(f"creating urlshort from {short_code}")
    # Set expiration time to 30 days from now
    expires_at = datetime.utcnow() + timedelta(days=30)
    logger.debug(f"expires at expires_at from {expires_at}")
    
    with UrlShortenerUnitofWork() as uow:

        db_url = UrlModel(
            short_code=short_code,
            original_url=str(url.original_url),
            expires_at=expires_at,
            visits=0
        )
        logger.debug(f"Creating data in Db {db_url}")
        repsonse = ShortURLResponse(**db_url.dump())
        uow.url_shotner_repository.add(db_url)
        uow.commit()
        logger.debug(f"Creating response serialized {repsonse}")
        return repsonse

# def get_original_url_by_short_code(db: Session, short_code: str) -> models.URL | None:
#     """Retrieves the URL entry based on the short code."""
#     return db.query(models.URL).filter_by(short_code=short_code).first()

# def record_visit(db: Session, url: models.URL):
#     """Increments the visit count for a given URL."""
#     url.visits += 1
#     db.commit()
#     db.refresh(url)