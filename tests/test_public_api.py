def test_public_api_imports_remain_available():
    from context_router import (
        BaseRouter,
        ContextItem,
        ContextPack,
        HybridRouter,
        MemoryStore,
        RecencyRouter,
        ScoredContextItem,
        SemanticRouter,
        SQLiteMemoryStore,
        RouterConfig,
        TaskRouter,
    )

    assert ContextItem
    assert ScoredContextItem
    assert ContextPack
    assert MemoryStore
    assert BaseRouter
    assert RecencyRouter
    assert SemanticRouter
    assert TaskRouter
    assert HybridRouter
    assert RouterConfig
    assert SQLiteMemoryStore
