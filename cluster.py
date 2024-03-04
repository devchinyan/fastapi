import uvicorn
from multiprocessing import cpu_count
from sys import argv 
from re import search
from src.config.config import config

def run_uvicorn(worker_count:int = None):
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=int(config.PORT),
        workers=worker_count if worker_count else cpu_count(),
    )

if __name__ == "__main__":
    if len(argv)==2:
        number_of_cluster = argv[1]
        if number_of_cluster.lower() == "max":
            run_uvicorn()
        elif search(r"^\d+$",number_of_cluster) :
            run_uvicorn(int(number_of_cluster))
        else:
            run_uvicorn(1)
    else:
        run_uvicorn(1)