import textwrap
import logging

logger = logging.getLogger(__name__)

class ArticleBuilder:
    SECTION_SEP_TOKEN = "<SECTION>"
    CONTENT_SEP_TOKEN = "<CONTENT>"
    
    def __init__(self):
        self.article = ""
        self.indent_level = 0
        self.indent_prefix = " " * 4
        self.paragraph_hint = ""
        self.bullet = ""
        self.textwrapper = textwrap.TextWrapper(width = 80)

    def getArticleInPlainText(self):
        temp = self.article.replace(ArticleBuilder.SECTION_SEP_TOKEN, "")
        temp = temp.replace(ArticleBuilder.CONTENT_SEP_TOKEN, "")
        return temp

    def getArticleInSections(self):
        sections = self.article.split(ArticleBuilder.SECTION_SEP_TOKEN)
        structuredArticle = [list(section.split(ArticleBuilder.CONTENT_SEP_TOKEN)) for section in sections]

        logger.info(f"Sectioned article into {len(structuredArticle)} parts")
        return structuredArticle

    def clear(self):
        self.article = ""
        self.resetIndents()
        logger.info("Reset ArticleBuilder")
        return self

    def resetIndents(self):
        self.indent_level = 0
        self.indent_with = ""

    def title(self, title: str):
        self.content(title.upper())
        # self.content("=" * len(title))
        self.br()
        logger.debug(f"Added title & newline: {title}")
        return self

    def subtitle(self, subtitle: str):
        subtitle = subtitle.title()
        self.content(subtitle)
        logger.debug(f"Added subtitle: {subtitle}")
        return self

    def startSection(self, bullet = "", paragraph_hint = ""):
        ''' Responsible for changing the indentation state '''
        # textwrap.fill(longString, width = 80, prefix = )

        self.indent_level += 1
        self.bullet = bullet
        self.paragraph_hint = paragraph_hint
        self.article += ArticleBuilder.SECTION_SEP_TOKEN
        logger.debug(f"Started new section. Current indent level: {self.indent_level}")
        return self

    def endSection(self):
        ''' Responsible for changing the indentation state '''
        self.indent_level -= 1
        self.bullet = ""
        self.paragraph_hint = ""
        # self.article += ArticleBuilder.SECTION_SEP_TOKEN
        logger.debug(f"Ended new section. Current indent level: {self.indent_level}")
        return self

    def content(self, longString):
        with self:
            self.article += ArticleBuilder.CONTENT_SEP_TOKEN
            content = self.textwrapper.fill(longString)
            self.article += content
            logger.debug(f"Added statement: {content} & newline")
            # self.article += ArticleBuilder.CONTENT_SEP_TOKEN
            self.article += "\n"
        return self

    def __enter__(self):
        emptyIndent = self.indent_prefix * self.indent_level
        bulletedIndent = self.insertBullet(self.bullet, emptyIndent)
        if self.indent_level:
            unBulletedIndent = emptyIndent + (" " * (len(self.bullet) + 1))
        else:
            unBulletedIndent = emptyIndent
        self.textwrapper.initial_indent = bulletedIndent + self.paragraph_hint
        self.textwrapper.subsequent_indent = unBulletedIndent
        

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.textwrapper.initial_indent = ""
        self.textwrapper.subsequent_indent = ""

    def insertBullet(self, bullet, string):
        if self.indent_level:
            return string + bullet + " "
        else:
            return string

    def br(self, num_line_breaks = 1):
        with self:
            self.article += num_line_breaks * "\n"
            logger.debug(f"Added {num_line_breaks} newline tokens")
        return self

    def __str__(self):
        return self.article
