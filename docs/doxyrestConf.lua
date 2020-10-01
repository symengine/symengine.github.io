-- Specify input and output paths:

OUTPUT_FILE = "docs/Sphinx/source/gen_doxyrest/index.rst"
INPUT_FILE = "docs/Doxygen/gen_docs/xml/index.xml"
FRAME_FILE = "docs/doxyrest/frame/cfamily/index.rst.in"
FRAME_DIR_LIST = { "docs/doxyrest/frame/cfamily", "docs/doxyrest/frame/common" }

-- Usually, Doxygen-based documentation has a main page (created with
-- the \mainpage directive). If that's the case, force-include
-- the contents of 'page_index.rst' into 'index.rst':

INTRO_FILE = "page_index.rst"

-- If your documentation uses \verbatim directives for code snippets
-- you can convert those to reStructuredText C++ code-blocks:

VERBATIM_TO_CODE_BLOCK = "cpp"

-- Asterisks, pipes and trailing underscores have special meaning in
-- reStructuredText. If they appear in Doxy-comments anywhere except
-- for code-blocks, they must be escaped:

ESCAPE_ASTERISKS = true
ESCAPE_PIPES = true
ESCAPE_TRAILING_UNDERSCORES = true
