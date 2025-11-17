from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.v1.deps.auth import get_current_user_id
from src.core.errors import api_envelope, ApplicationError, ErrorCode
from src.db.mongo import get_collection
from src.models.course import CourseCreate, CourseOut

router = APIRouter()


def _serialize_course(doc: Dict[str, Any]) -> CourseOut:
    return CourseOut(
        id=str(doc["_id"]),
        title=doc["title"],
        description=doc["description"],
        category=doc["category"],
        published=doc.get("published", False),
        created_by=doc.get("created_by"),
        created_at=doc["created_at"],
    )


@router.get(
    "/api/v1/courses",
    summary="List courses",
    description="List courses with optional filters for category and publication status.",
)
# PUBLIC_INTERFACE
async def list_courses(
    category: Optional[str] = Query(default=None, description="Filter by category"),
    published: Optional[bool] = Query(default=None, description="Filter by published flag"),
):
    """List courses with optional query filters.

    Args:
        category: Optional category filter.
        published: Optional published flag.

    Returns:
        dict: response envelope with list of courses.
    """
    coll = get_collection("courses")
    query: Dict[str, Any] = {}
    if category:
        query["category"] = category
    if published is not None:
        query["published"] = published

    cursor = coll.find(query).sort("created_at", -1)
    results: List[CourseOut] = []
    async for doc in cursor:
        results.append(_serialize_course(doc))
    return api_envelope([c.model_dump() for c in results])


@router.post(
    "/api/v1/courses",
    summary="Create course",
    description="Create a new course (placeholder auth allows all).",
    status_code=201,
)
# PUBLIC_INTERFACE
async def create_course(
    payload: CourseCreate,
    user_id: Optional[str] = Depends(get_current_user_id),
):
    """Create a course document in MongoDB. Placeholder allows all requests.

    Args:
        payload: CourseCreate payload.
        user_id: placeholder user id; None for now.

    Returns:
        dict: response envelope with created course.

    Notes:
        TODO: Enforce instructor/admin role for creation once auth is implemented.
    """
    coll = get_collection("courses")
    doc = {
        "title": payload.title,
        "description": payload.description,
        "category": payload.category,
        "published": payload.published,
        "created_by": user_id,  # may be None in placeholder
        "created_at": datetime.utcnow(),
    }
    try:
        result = await coll.insert_one(doc)
    except Exception:
        raise ApplicationError("Failed to create course", ErrorCode.DATABASE_ERROR, 500)
    inserted = await coll.find_one({"_id": result.inserted_id})
    course = _serialize_course(inserted)
    return api_envelope(course.model_dump(), message="created")


@router.get(
    "/api/v1/courses/{course_id}",
    summary="Get course",
    description="Retrieve course details by id.",
)
# PUBLIC_INTERFACE
async def get_course(course_id: str):
    """Get course by id.

    Args:
        course_id: The course identifier.

    Raises:
        HTTPException: 404 if not found.

    Returns:
        dict: response envelope with course details.
    """
    coll = get_collection("courses")
    try:
        oid = ObjectId(course_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Course not found")

    doc = await coll.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Course not found")
    course = _serialize_course(doc)
    return api_envelope(course.model_dump())
