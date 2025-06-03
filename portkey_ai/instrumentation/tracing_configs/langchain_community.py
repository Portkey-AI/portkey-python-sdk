from portkey_ai.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    ClassConfig,
    MethodConfig,
)

langchain_community_tracing_config = TracingConfig(
    name="langchain_community",
    min_version="0.2.0",
    modules=[
        ModuleConfig(
            name="langchain_community.vectorstores",
            classes=[
                ClassConfig(
                    pattern=".*",
                    methods=[
                        MethodConfig(name="add_texts", args="?!", result="?!"),
                        MethodConfig(name="delete", args="?!", result="?!"),
                        MethodConfig(name="get_by_ids", args="?!", result="?!"),
                        MethodConfig(name="add_documents", args="?!", result="?!"),
                        MethodConfig(name="search", args="?!", result="?!"),
                        MethodConfig(name="similarity_search", args="?!", result="?!"),
                        MethodConfig(
                            name="similarity_search_with_score", args="?!", result="?!"
                        ),
                        MethodConfig(
                            name="similarity_search_with_relevance_scores",
                            args="?!",
                            result="?!",
                        ),
                        MethodConfig(
                            name="similarity_search_by_text", args="?!", result="?!"
                        ),
                        MethodConfig(
                            name="similarity_search_by_vector", args="?!", result="?!"
                        ),
                        MethodConfig(
                            name="max_marginal_relevance_search", args="?!", result="?!"
                        ),
                        MethodConfig(
                            name="max_marginal_relevance_search_by_vector",
                            args="?!",
                            result="?!",
                        ),
                        MethodConfig(name="from_documents", args="?!", result="?!"),
                        MethodConfig(name="from_texts", args="?!", result="?!"),
                        MethodConfig(name="as_retriever", args="?!", result="?!"),
                        MethodConfig(name="add_texts", args="?!", result="?!"),
                    ],
                ),
            ],
        ),
        ModuleConfig(
            name="langchain_community.document_loaders.base",
            classes=[
                ClassConfig(
                    pattern="BaseLoader",
                    methods=[
                        MethodConfig(name="load", args="?!", result="?!"),
                        MethodConfig(name="aload", args="?!", result="?!"),
                        MethodConfig(name="load_and_split", args="?!", result="?!"),
                        MethodConfig(
                            name="lazy_load_and_split", args="?!", result="?!"
                        ),
                    ],
                ),
                ClassConfig(
                    pattern="BaseBlobParser",
                    methods=[
                        MethodConfig(name="parse", args="?!", result="?!"),
                        MethodConfig(name="lazy_parse", args="?!", result="?!"),
                    ],
                ),
            ],
        ),
    ],
)
