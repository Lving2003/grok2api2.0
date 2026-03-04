from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from app.core.auth import is_public_enabled

router = APIRouter()
STATIC_DIR = Path(__file__).resolve().parents[2] / "static"


def _resolve_static_path(*parts: str) -> Path | None:
    candidates: list[Path] = []

    base = Path(__file__).resolve()
    candidates.append(STATIC_DIR.joinpath(*parts))

    cwd = Path.cwd()
    candidates.append(cwd.joinpath("app", "static", *parts))
    candidates.append(cwd.joinpath("static", *parts))

    for parent in base.parents[:8]:
        candidates.append(parent.joinpath("static", *parts))
        candidates.append(parent.joinpath("app", "static", *parts))

    for candidate in candidates:
        try:
            if candidate.exists():
                return candidate
        except OSError:
            continue
    return None


def _serve_public_page(filename: str) -> FileResponse:
    path = _resolve_static_path("public", "pages", filename)
    if path is None:
        path = _resolve_static_path("_pub", "pages", filename)
    if path is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(path)


@router.get("/", include_in_schema=False)
async def root():
    if is_public_enabled():
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/admin/login")


@router.get("/login", include_in_schema=False)
async def public_login():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("login.html")


@router.get("/imagine", include_in_schema=False)
async def public_imagine():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("imagine.html")


@router.get("/voice", include_in_schema=False)
async def public_voice():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("voice.html")


@router.get("/video", include_in_schema=False)
async def public_video():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("video.html")


@router.get("/chat", include_in_schema=False)
async def public_chat():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("chat.html")


@router.get("/nsfw", include_in_schema=False)
async def public_nsfw():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("nsfw.html")


@router.get("/imagine-workbench", include_in_schema=False)
async def public_imagine_workbench():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    return _serve_public_page("imagine_workbench.html")


@router.get("/manifest.webmanifest", include_in_schema=False)
async def public_manifest():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    path = _resolve_static_path("public", "manifest.webmanifest")
    if path is None:
        path = _resolve_static_path("_pub", "manifest.webmanifest")
    if path is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(path, media_type="application/manifest+json")


@router.get("/sw.js", include_in_schema=False)
async def public_service_worker():
    if not is_public_enabled():
        raise HTTPException(status_code=404, detail="Not Found")
    path = _resolve_static_path("public", "sw.js")
    if path is None:
        path = _resolve_static_path("_pub", "sw.js")
    if path is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(path, media_type="application/javascript")
