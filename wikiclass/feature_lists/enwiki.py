"""
English Wikipedia
+++++++++++++++++
"""

from revscoring.features import wikitext
from revscoring.features.modifiers import max, sub
from revscoring.languages import english

from . import wikipedia

# Templates
infobox_templates = wikitext.revision.template_names_matching(
    r"infobox", name="enwiki.revision.infobox_templates")
CN_TEMPLATES = [
    r"Citation[_ ]needed",
    r"Cn",
    r"Fact"
]
cn_templates = wikitext.revision.template_names_matching(
    "|".join(CN_TEMPLATES), name="enwiki.revision.cn_templates")
who_templates = wikitext.revision.template_names_matching(
    "Who", name="enwiki.revision.who_templates")
main_article_templates = wikitext.revision.template_names_matching(
    "Main", name="enwiki.main_article_templates")
cite_templates = wikitext.revision.template_names_matching(
    r"cite", name="enwiki.revision.cite_templates")
proportion_of_templated_references = \
    cite_templates / max(wikitext.revision.ref_tags, 1)
non_templated_references = max(wikitext.revision.ref_tags - cite_templates, 0)
non_cite_templates = sub(
    wikitext.revision.templates, cite_templates,
    name="enwiki.revision.non_cite_templates"
)

# Links
category_links = wikitext.revision.wikilink_titles_matching(
    r"Category\:", name="enwiki.revision.category_links")
image_links = wikitext.revision.wikilink_titles_matching(
    r"File|Image\:", name="enwiki.revision.image_links")

local_wiki = [
    image_links,
    image_links / max(wikitext.revision.content_chars, 1),
    category_links,
    category_links / max(wikitext.revision.content_chars, 1),
    cite_templates,
    cite_templates / max(wikitext.revision.content_chars, 1),
    proportion_of_templated_references,
    non_templated_references,
    non_templated_references / max(wikitext.revision.content_chars, 1),
    non_cite_templates,
    non_cite_templates / max(wikitext.revision.content_chars, 1),
    infobox_templates,
    cn_templates + 1,
    cn_templates / max(wikitext.revision.content_chars, 1),
    who_templates + 1,
    who_templates / max(wikitext.revision.content_chars, 1),
    main_article_templates,
    main_article_templates / max(wikitext.revision.content_chars, 1),
    english.stemmed.revision.stem_chars / \
        max(wikitext.revision.content_chars, 1),
]

wp10 = wikipedia.article + local_wiki
"""
Based largely on work by Morten Warncke-Wang et al.[1] and with a few
improvements and extensions that Morten identified after publication.

1. Warncke-Wang, M., Cosley, D., & Riedl, J. (2013, August). Tell me more: An
   actionable quality model for wikipedia. In Proceedings of the 9th
   International Symposium on Open Collaboration (p. 8). ACM.
   http://opensym.org/wsos2013/proceedings/p0202-warncke.pdf
"""
