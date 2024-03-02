from .seed_model import SeedMatrix
from typing import List
from .data.account_seed import accountSeed
from .data.profile_seed import profileSeed

seedMatrices:List[SeedMatrix] = [
    accountSeed,
    profileSeed
]