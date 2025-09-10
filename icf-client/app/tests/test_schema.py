from app.ferm_schema import FermProject

def test_schema_min_ok():
    p = FermProject(
        external_id="HND-001",
        title="Demo",
        country_code="HN",
        geometry={"type":"Point","coordinates":[-88.0,15.5]}
    )
    assert p.external_id == "HND-001"
