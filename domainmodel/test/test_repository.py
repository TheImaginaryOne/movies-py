from domainmodel.repository import MemoryRepository
from domainmodel.movie import Movie

def test_view_movies():
    m0 = Movie("The", 2020)
    m1 = Movie("Tragedy", 2020)
    m2 = Movie("of", 2020)
    m3 = Movie("Darth", 2020)
    m4 = Movie("Plagueis", 2020)
    m5 = Movie("the", 2020)
    m6 = Movie("Wise", 2020)
    movies_mock = [m0, m1, m2, m3, m4, m5, m6]
    rr = MemoryRepository(movies_mock)

    assert rr.view_movies(0, 3) == ([m0, m1, m2], True)
    assert rr.view_movies(5, 80) == ([m5, m6], False)
