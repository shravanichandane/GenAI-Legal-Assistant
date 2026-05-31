# Makes backend.routes a package
from .health import router as health
from .upload import router as upload
from .analyze import router as analyze
from .search import router as search
