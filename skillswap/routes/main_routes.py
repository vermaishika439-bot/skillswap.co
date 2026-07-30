"""
main_routes.py
---------------
Public-facing pages: the landing page and the browse-skills page.
These don't require login (though browse could be gated in a
real product — kept open here for portfolio-demo purposes).
"""

from flask import Blueprint, render_template, request
from models.db import get_db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    db = get_db()

    # Pull a handful of users to show as "Featured Teachers" on the landing page
    featured_teachers = db.execute(
        """SELECT u.id, u.name, u.location, u.profile_image, u.bio,
                  GROUP_CONCAT(DISTINCT so.skill_name) as skills
           FROM users u
           LEFT JOIN skills_offered so ON so.user_id = u.id
           GROUP BY u.id
           ORDER BY u.created_at DESC
           LIMIT 6"""
    ).fetchall()

    # Simple site-wide stats for the "Community Statistics" section
    total_users = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    total_skills = db.execute("SELECT COUNT(*) as c FROM skills_offered").fetchone()["c"]
    total_swaps = db.execute(
        "SELECT COUNT(*) as c FROM swap_requests WHERE status = 'accepted'"
    ).fetchone()["c"]

    return render_template(
        "landing.html",
        featured_teachers=featured_teachers,
        total_users=total_users,
        total_skills=total_skills,
        total_swaps=total_swaps,
    )


@main_bp.route("/browse")
def browse_skills():
    db = get_db()

    # --- Read filter/search params from the query string ---
    search_query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 9

    # Build query dynamically based on filters
    base_query = """
        SELECT u.id, u.name, u.location, u.profile_image,
               GROUP_CONCAT(DISTINCT so.skill_name) as skills_offered,
               GROUP_CONCAT(DISTINCT sw.skill_name) as skills_wanted
        FROM users u
        LEFT JOIN skills_offered so ON so.user_id = u.id
        LEFT JOIN skills_wanted sw ON sw.user_id = u.id
    """
    conditions = []
    params = []

    if search_query:
        conditions.append("so.skill_name LIKE ?")
        params.append(f"%{search_query}%")
    if category:
        conditions.append("so.category = ?")
        params.append(category)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " GROUP BY u.id ORDER BY u.created_at DESC"

    all_results = db.execute(base_query, params).fetchall()

    # --- Basic pagination (slice results in Python, fine for demo scale) ---
    total_results = len(all_results)
    total_pages = max(1, (total_results + per_page - 1) // per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = all_results[start:end]

    categories = [
        "Programming", "Design", "Marketing", "Music",
        "Language", "Business", "Writing", "Photography"
    ]

    return render_template(
        "browse_skills.html",
        users=paginated_results,
        categories=categories,
        search_query=search_query,
        selected_category=category,
        page=page,
        total_pages=total_pages,
    )
