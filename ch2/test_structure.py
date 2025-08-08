from cards import Card


def test_to_dict():
    # (GIVEN) DADO um objeto Card com conteúdo
    c1 = Card("something", "brian", "todo", 123)

    # (WHEN) QUANDO chamamos to_dict() no objeto
    c2 = c1.to_dict()

    # (THEN) ENTÃO o resultado será um dicionário com conteúdo
    c2_expected = {
        "summary": "something",
        "owner": "brian",
        "state": "todo",
        "id": 123,
    }
    assert c2 == c2_expected
