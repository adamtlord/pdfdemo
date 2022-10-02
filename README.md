# PDF Form Generation Demo
[https://adamtlord.github.io/pdfdemo/](https://adamtlord.github.io/pdfdemo/)
## Frontend
- Vite for dev server and building
- Tailwind CSS, with some help from Tailwind UI
- Alpine.js
- Deployed via Github Pages
## Backend
- pipenv
- AWS Python Lambda
- pdfkit, Jinja2, and wkhtmltopdf for rendering and pdf generation
- AWS Chalice serverless framework for super quick REST API
## Disclaimers and Confessions
- I'm a sucker for extra credit, so I spent too much time on styling, and I was determined to deploy it from the start.
- I knew a serverless function was how I wanted to do the pdf part, but this was my first time using Chalice.
- Because the repo is monolithic, I had to do some wild git stuff to get the frontend deployed.
- I didn't bother with a local version of the backend -- it would have required running things in a container, and it felt simpler to just deploy and tweak the lambda.

**If I had more time, I would:**
- add some error handling and validation
- get the whole thing running locally
- add some tests (but really, who are we kidding)
- make the pdf look better
