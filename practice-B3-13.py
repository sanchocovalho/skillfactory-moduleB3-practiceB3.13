class Tag:
    def __init__(self, tag, is_single=False, klass=None, childlevel=0, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.childlevel = childlevel
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        tabs = ""
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        for tab in range(self.childlevel+1):
            tabs += "\t"

        if len(self.children) > 0:
            opening = tabs + "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = tabs + "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                    return tabs + "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                if(attrs is None):
                    return tabs + "<{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                    )
                else:
                    return tabs + "<{tag}>{text}</{tag}>\n".format(
                    tag=self.tag, text=self.text
                    )


class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "</%s>\n" % self.tag
        return html


def main(output=None):
    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p", childlevel=1) as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag(
                    "img", is_single=True,  childlevel=1, src="/icon.png", data_image="responsive"
                ) as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main("index.html")