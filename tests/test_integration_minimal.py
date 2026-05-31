from context_router.context.context_pack import ContextPack
from context_router.examples.integration_minimal import run


def test_minimal_integration_example_returns_context_pack():
    pack = run()
    assert isinstance(pack, ContextPack)
    assert pack.memories
    assert pack.metadata["router"] == "hybrid"
