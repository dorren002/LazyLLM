# flake8: noqa E501
from . import utils
import functools
import lazyllm


add_chinese_doc = functools.partial(utils.add_chinese_doc, module=lazyllm.tools)
add_english_doc = functools.partial(utils.add_english_doc, module=lazyllm.tools)
add_example = functools.partial(utils.add_example, module=lazyllm.tools)

add_english_doc('Document', r"""
Initializes a Document module with optional user interface creation.

This constructor initializes a Document module that can work with or without a user interface (UI). If the UI is enabled, it also sets up a server module to manage document operations and a web module for UI interactions. The module relies on an implementation (`DocGroupImpl`) that handles the core functionality such as generating signatures and querying documents based on signatures.

Arguments:
    dataset_path (str): The path to the dataset directory. This directory should contain the documents to be managed by the Document module.
    embed: An embedding object or function that is used for generating document embeddings. The exact type and requirements depend on the implementation of `DocGroupImpl`.
    create_ui (bool, optional): A flag indicating whether to create a user interface for the Document module. Defaults to True.
    launcher (optional): An object or function responsible for launching the server module. If not provided, a default launcher from `lazyllm.launchers` with asynchronous behavior (`sync=False`) is used.
""")

add_chinese_doc('Document', r"""
初始化一个具有可选用户界面的文档模块。

此构造函数初始化一个可以有或没有用户界面的文档模块。如果启用了用户界面，它还会提供一个ui界面来管理文档操作接口，并提供一个用于用户界面交互的网页。

Arguments:
    dataset_path (str): 数据集目录的路径。此目录应包含要由文档模块管理的文档。
    embed: 用于生成文档embedding的对象。
    create_ui (bool, optional): 指示是否为文档模块创建用户界面的标志。默认为 True。
    launcher (optional): 负责启动服务器模块的对象或函数。如果未提供，则使用 `lazyllm.launchers` 中的默认异步启动器 (`sync=False`)。
""")

add_example('Document', r"""
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='you doc path', embed=m, create_ui=False)
""")

add_english_doc('Rerank', r"""
Initializes a Rerank module for postprocessing and reranking of nodes (documents).
This constructor initializes a Rerank module that configures a reranking process based on a specified reranking type. It allows for the dynamic selection and instantiation of reranking kernels (algorithms) based on the type and provided keyword arguments.

Arguments:
    types: The type of reranker to be used for the postprocessing and reranking process. Defaults to 'Reranker'.
    **kwargs: Additional keyword arguments that are passed to the reranker upon its instantiation.

Detailed explanation of reranker types
  - Reranker：This registered reranking function instantiates a SentenceTransformerRerank reranker with a specified model and top_n parameter. It is designed to rerank nodes based on sentence transformer embeddings.
  - SimilarityFilter：This registered reranking function instantiates a SimilarityPostprocessor with a specified similarity threshold. It filters out nodes that do not meet the similarity criteria.
  - KeywordFilter：This registered reranking function instantiates a KeywordNodePostprocessor with specified required and excluded keywords. It filters nodes based on the presence or absence of these keywords.
""")

add_chinese_doc('Rerank', r"""
用于创建节点（文档）后处理和重排序的模块。

Arguments:
    types: 用于后处理和重排序过程的排序器类型。默认为 'Reranker'。
    **kwargs: 传递给重新排序器实例化的其他关键字参数。

详细解释types类型
  - Reranker：实例化一个具有指定模型和 top_n 参数的 SentenceTransformerRerank 重排序器。
  - SimilarityFilter：实例化一个具有指定相似度阈值的 SimilarityPostprocessor。它过滤掉不满足相似度标准的节点。
  - KeywordFilter：实例化一个具有指定必需和排除关键字的 KeywordNodePostprocessor。它根据这些关键字的存在或缺失来过滤节点。
""")

add_example('Rerank', r"""
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='you doc path', embed=m, create_ui=False)
    >>> rm = Retriever(documents, similarity='chinese_bm25', parser='SentenceDivider', similarity_top_k=6)
    >>> rerank = Rerank(types='SimilarityFilter', threshold=2.0)
    >>> m = lazyllm.ActionModule(rm, rerank)
    >>> m.start()
    >>> print(m("query"))  
""")

add_english_doc('Retriever', r"""
Create a Retriever module for document query and retrieval.
This constructor initializes a Retriever module that configures a document retrieval process based on a specified similarity measure. It generates a signature using the document's generate_signature method, which is then used for querying documents.

Arguments:
    doc: The Document module instance that contains the documents and functionalities for generating signatures and querying documents.
    parser: The parser to be used for processing documents during querying.The candidate sets are ["Hierarchy", "CoarseChunk", "MediumChunk", "FineChunk", "SentenceDivider", "TokenDivider", "HtmlExtractor", "JsonExtractor", "MarkDownExtractor"]
    similarity : The name of the similarity function to be used for document retrieval. Defaults to 'defatult'. The candidate sets are ["defatult", "chinese_bm25", "bm25"].
    index: The type of index to be used for document retrieval. Defaults to 'vector'.

Detailed explanation of Parser types
  - Hierarchy: This node parser will chunk nodes into hierarchical nodes. This means a single input will be chunked into several hierarchies of chunk sizes, with each node containing a reference to it's parent node.
  - CoarseChunk: Get children of root nodes in given nodes that have given depth 0.
  - MediumChunk: Get children of root nodes in given nodes that have given depth 1.
  - FineChunk: Get children of root nodes in given nodes that have given depth 2.
  - SentenceDivider：This node parser attempts to split text while respecting the boundaries of sentences.
  - TokenDivider：This node parser attempts to split to a consistent chunk size according to raw token counts.
  - HtmlExtractor：This node parser uses beautifulsoup to parse raw HTML.By default, it will parse a select subset of HTML tags, but you can override this.The default tags are: ["p", "h1"]
  - JsonExtractor：Splits a document into Nodes using custom JSON splitting logic.
  - MarkDownExtractor：Splits a document into Nodes using custom Markdown splitting logic.
                
Detailed explanation of similarity types
  - defatult：Search documents using embedding method.
  - chinese_bm25：Search documents using chinese_bm25 method.The primary differences between chinese_bm25 and the standard bm25 stem from the specific adjustments and optimizations made for handling Chinese text. 
  - bm25：Search documents using bm25 method.
""")

add_chinese_doc('Retriever', r"""
创建一个用于文档查询和检索的检索模块。

此构造函数初始化一个检索模块，该模块根据指定的相似度度量配置文档检索过程。它使用文档的 generate_signature 方法生成签名，然后用于查询文档。

Arguments:
    doc: 文档模块实例。
    parser: 用于设置处理文档的解析器。候选集包括 ["Hierarchy", "CoarseChunk", "MediumChunk", "FineChunk", "SentenceDivider", "TokenDivider", "HtmlExtractor", "JsonExtractor", "MarkDownExtractor"]
    similarity : 用于设置文档检索的相似度函数。默认为 'defatult'。候选集包括 ["defatult", "chinese_bm25", "bm25"]。
    index: 用于文档检索的索引类型。默认为 'vector'。

详细解释parser类型
  - Hierarchy: 此节点解析器将原始文本按照分层算法拆分成节点。这意味着一个输入将被分块成几个层次的块，每个节点包含对其父节点的引用。
  - CoarseChunk: 获取给定结点中的深度为 0 的子节点。
  - MediumChunk: 获取给定结点中的深度为 1 的子节点。
  - FineChunk: 获取给定结点中的深度为 2 的子节点。
  - SentenceDivider：此节点解析器尝试在尊重句子边界的同时拆分文本。
  - TokenDivider：此节点解析器尝试将原始文本拆分为一致的块大小。
  - HtmlExtractor：此节点解析器使用 beautifulsoup 解析原始 HTML。默认情况下，它将解析选定的 HTML 标签，但您可以覆盖此设置。默认标签为: ["p", "h1"]
  - JsonExtractor：使用自定义 JSON 拆分逻辑将文档拆分为节点。
  - MarkDownExtractor：使用自定义 Markdown 拆分逻辑将文档拆分为节点。

详细解释similarity类型
  - defatult：使用 embedding 算法搜索文档。
  - chinese_bm25：使用 chinese_bm25 算法搜索文档。chinese_bm25 与标准 bm25 的主要区别在于对中文的特定优化。
  - bm25：使用 bm25 算法搜索文档。
""")

add_example('Retriever', r"""
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='you doc path', embed=m, create_ui=False)
    >>> rm = Retriever(documents, similarity='chinese_bm25', parser='SentenceDivider', similarity_top_k=6)
    >>> rm.start()
    >>> print(rm("query"))
""")