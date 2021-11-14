import textwrap

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

    def getArticleLines(self):
        return self.article.split("\n")   

    def getArticleSections(self):
        articleSections = self.article.split(ArticleBuilder.SECTION_SEP_TOKEN)
        articleStruct = list(map(lambda section : section.split(ArticleBuilder.CONTENT_SEP_TOKEN), articleSections))

        return articleStruct

    def clear(self):
        self.article = ""
        self.resetIndents()
        return self

    def resetIndents(self):
        self.indent_level = 0
        self.indent_with = ""

    def title(self, title):
        self.content(title.upper())
        # self.content("=" * len(title))
        self.br()
        return self

    def subtitle(self, subtitle):
        self.content(subtitle.title())
        # self.content("-" * len(subtitle))
        return self

    def startSection(self, bullet = "", paragraph_hint = ""):
        ''' Responsible for changing the indentation state '''
        # textwrap.fill(longString, width = 80, prefix = )
        self.indent_level += 1
        self.bullet = bullet
        self.paragraph_hint = paragraph_hint
        self.article += ArticleBuilder.SECTION_SEP_TOKEN
        return self

    def endSection(self):
        ''' Responsible for changing the indentation state '''
        self.indent_level -= 1
        self.bullet = ""
        self.paragraph_hint = ""
        self.article += ArticleBuilder.SECTION_SEP_TOKEN
        return self

    def content(self, longString):
        with self:
            self.article += ArticleBuilder.CONTENT_SEP_TOKEN
            self.article += self.textwrapper.fill(longString)
            self.article += ArticleBuilder.CONTENT_SEP_TOKEN
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
        return self

    def __str__(self):
        return self.article

if __name__ == "__main__":
    builder = ArticleBuilder()
    
    # print(ArticleBuilder.render_title("string loose ends meet me at the"))
    (builder.title("Sylvia Chan and Oniichan")
                .startSection()
                .subtitle("Example Subtitle")
                .content("lorem ipsum" * 50)
                .endSection()
    )

    for section in builder.getArticleSections():
        for content in section:
            print(content, end="")

'''
builder = ArticleBuilder()

bulder.title("Sylvia Chan kena")
        .startSection()
        .content(authors)
        .content(longString)
        .content(video links)
        .endSection()

bulder.title("Word: Engineer")
        .subtitle("VERB:")
        .startSection(bullet = "-")
        .content(longString)
        .content(longString)
        .content(longString)
        .endSection()

        .subtitle("NOUN:")
        .startSection(bullet = "-")
        .content(longString)
        .content(longString)
        .content(longString)
        .endSection()


Wrap must account for bullets

- width
- initial indent
- subsequent indent
- 
'''