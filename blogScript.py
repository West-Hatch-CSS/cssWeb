"""
This script is used to edit blog.html and instert new blog entries.

In order to add new blog entries do the following:
1. Fork the cssWeb repository
2. Run this script and it will edit blog.html for you
3. Commit the changes to your forked repository
4. Create a pull request to the original repository
5. Wait for the pull request to be merged
6. Your blog entry will be live on the website

Credit - Samuel Douek - Director of the CSS
"""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QPlainTextEdit
from bs4 import BeautifulSoup
from html import escape
import sys

class BlogPostGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Blog Post Adder")

        layout = QVBoxLayout()

        self.header_input = QLineEdit()
        self.header_input.setPlaceholderText("Enter Header (e.g. May 4th, 2025 By Samuel Douek)")
        layout.addWidget(QLabel("Header:"))
        layout.addWidget(self.header_input)

        self.quote_input = QLineEdit()
        self.quote_input.setPlaceholderText("Enter Quote (optional)")
        layout.addWidget(QLabel("Quote:"))
        layout.addWidget(self.quote_input)

        self.body_input = QPlainTextEdit()
        self.body_input.setPlaceholderText("Enter Body Text")
        layout.addWidget(QLabel("Body Text:"))
        layout.addWidget(self.body_input)

        self.submit_button = QPushButton("Add Blog Post")
        self.submit_button.clicked.connect(self.add_blog_post)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_blog_post(self):
        header = escape(self.header_input.text().strip())
        quote = escape(self.quote_input.text().strip())
        body = self.body_input.toPlainText().strip()

        # Convert all actual newlines to <br> only once
        body_lines = body.splitlines()
        body_html = '<br>'.join(escape(line) for line in body_lines)

        article_html = f'''
<article class="blog-entry">
    <h3>{header}</h3>
    <h3>{quote}</h3>
    <p>{body_html}</p>
</article>
'''

        try:
            with open("blog.html", "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            blog_div = soup.find("div", id="blog-posts")
            if blog_div:
                new_post = BeautifulSoup(article_html, "html.parser")
                # Insert at the top of the div's contents
                blog_div.insert(0, new_post)

                with open("blog.html", "w", encoding="utf-8") as file:
                    file.write(str(soup))

                print("Post successfully added.")
            else:
                print("No div with id='blog-posts' found in blog.html.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BlogPostGUI()
    window.show()
    sys.exit(app.exec_())
