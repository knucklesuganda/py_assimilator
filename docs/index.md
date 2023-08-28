# Assimilator - the best Python patterns for the best projects

<p align="center">
  <a href="https://knucklesuganda.github.io/py_assimilator/"><img src="https://knucklesuganda.github.io/py_assimilator/images/logo.png" alt="PyAssimilator"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/license/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="License">
</a>

<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/stars/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="Stars">
</a>
<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/last-commit/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="Last commit">
</a>
</p>


## Install now
* `pip install py-assimilator`


## Code comparison
<link href="styles/code_examples.css" rel="stylesheet">

<div class="overlay">
  <div class="overlay__inner"></div>
</div>

<div class="code_preview_container">
<div class="code_example_buttons">
    <button class="code_switch_button">Database Example</button>
    <button class="code_switch_button">CRUD Example</button>
    <button class="code_switch_button">Independent Code Example</button>
    <a href="https://github.com/knucklesuganda/py_assimilator/tree/master/examples">
        <button class="code_switch_button" style="background: none">Full examples</button>
    </a>
</div>

<div class="code_examples">

    <div class="code_example" style="display: none">
        <div>
            Common database problems:

            <ul>
                <li>Dependencies - lots of external dependencies!</li>
                <li>Bad query management - long queries, bad queries, no ACID transactions!</li>
                <li>Only one database choice - spend 10 hours of your life to go from MySQL to MongoDB!</li> 
                <li>Hard to understand - code is either bad or hard to get!</li>
                <li>Complicated refactoring - spend 20 more hours on trying to make your code better!</li>
            </ul>

            ```Python
            def create_user(username: str, email: str):
                new_user = User(username=username, email=email, balance=0)
                session = db_session()      # DEPENDENCY!
                session.add(new_user)
                session.commit()    # NO ACID TRANSACTIONS!
                return new_user
            ```
        </div>
    
        <div>
            PyAssimilator solutions:

            <ul> 
                <li>Independent code - no dependencies at all!</li>
                <li>Automatic query management - queries are automatically optimized, easy ACID transactions!</li>
                <li>Multiple databases - change your storage without changing your code!</li>
                <li>Fast - spend 10 minutes instead of 10 hours!</li>
                <li>Easy to understand - you don't even need to know the underlying library!</li>
                <li>Extensible - complex queries for your industry are not a problem!</li>
            </ul>

            ```Python
            def create_user(username: str, email: str, uow: UnitOfWork):
                with uow:   # ACID TRANSACTIONS IN ANY DATABASE
                    new_user = uow.repository.save(
                        username=username,  # NO MODEL DEPENDENCIES
                        email=email,
                        balance=0,
                    )
                    uow.commit()    # AUTO ROLLBACK
            
                return new_user
            ```
        </div>
    </div>

    <div class="code_example"> 
        <div>
            Common CRUD problems:

            <ul>
                <li>Boilerplate - you repeat yourself!</li> 
                <li>Dependencies - lots of external dependencies!</li>
                <li>Coding mistakes - bugs and errors!</li>
                <li>Readability - no easy way to read your code!</li>
                <li>Boring - repeat this boring process over and over again!</li>
            </ul>


            ```Python
            def create_user():
                name = request.json['name']
                email = request.json['email']
                new_user = User(name=name, email=email)  # DEPENDENCY!
                db.session.add(new_user)
                db.session.commit()     # DEPENDENCY!
                return new_user

            def get_all_users():
                users = User.query.all() # DEPENDENCY!
                output = []
                for user in users:  # BOILERPLATE!
                    user_data = {}
                    user_data['name'] = user.name
                    user_data['email'] = user.email
                    output.append(user_data)
                return users
    
            def get_user(user_id):
                user = User.query.get_or_404(user_id)   # DEPENDENCY!
                user_data = {}
                user_data['name'] = user.name   # BOILERPLATE!
                user_data['email'] = user.email # BOILERPLATE!
                return user_data

            def update_user(user_id):
                user = User.query.get_or_404(user_id)   # DEPENDENCY!
                user.name = request.json['name']    # BOILERPLATE!
                user.email = request.json['email']  # BOILERPLATE!
                db.session.commit()     # NO ACID! DEPENDENCY!
                return user

            def delete_user(user_id):
                user = User.query.get_or_404(user_id)   # DEPENDENCY!
                db.session.delete(user) # NO ACID!
                db.session.commit() # DEPENDENCY!
                return True
            ```
        </div>

        <div>
            PyAssimilator CRUD solutions:

            <ul>
                <li>One pattern - get all the functions from CRUDService class</li> 
                <li>Independent code - no dependencies at all!</li>
                <li>Coding mistakes - common bugs and errors are fixes!</li>
                <li>Multiple databases - change your storage without changing your code!</li>
                <li>Fast - spend 10 minutes instead of 10 hours!</li>
                <li>Extensible - make CRUDService pattern suit your needs!</li>
            </ul>

            ```Python
            service = create_crud_service()

            def create_user(user_data: dict):
                return service.create(user_data)

            def list_users():
                return service.list()

            def get_user(id: int):
                return service.get(id=id)

            def update_user(id: int, new_data: dict):
                return service.update(id=id, is_admin=True, update_data=new_data)

            def delete_user():
                return service.delete(username="Tom")

            # Full FastAPI CRUD example on Github
            # https://github.com/knucklesuganda/py_assimilator/tree/master/examples/fastapi_crud_example
            ```
        </div>
    </div>

    <div class="code_example">
        <div>
            Why do we hate dependencies:

            <ul>
                <li>We depend on other people and their bugs!</li>
                <li>It's hard to update our code!</li>
                <li>We cannot use new technologies!</li> 
                <li>Complicated refactoring!</li>
            </ul>

            You can try to rewrite this code from sqlaclhemy to MongoDB and see why dependencies are bad yourself.

            ```Python
            from sqlalchemy import Table, Column,...
            from models import User, Friend, Like,...
            from database_init import init, session_create...
            from database_filters import my_filter...

            def bad_code():
                init()
                session = session_create()

                my_user = session(User).filter(
                    Friend.id == 1,
                    Like.post.id == 5,
                ).first()
                return my_user.username
            ```
        </div>
    
        <div>
            PyAssimilator independent code:

            <ul>
                <li>We use patterns to hide dependencies from other modules!</li>
                <li>It's easy to update our code since we have no dependencies!</li>
                <li>We can easily use new technologies!</li> 
                <li>Refactoring is easy!</li>
                <li>Patterns are extensible to your specific needs!</li>
            </ul>

            We use Repository pattern. We don't need to change our code to go from sqlalchemy to mongodb or any
            other supported database.

            ```Python
            from assimilator.core.database import Repository, filter_

            def independent_code(repository: Repository):
                return repository.get(
                    filter_(friend__id=1, like__post=5)
                )
            ```
        </div>
    </div>
</div>
</div>

<script src="scripts/code_examples.js"></script>


## What is that all about?

1. We want to write the best code.
2. We need the best patterns and techniques for this.
3. We use PyAssimilator and save lots of time.
4. We use PyAssimilator and write the best code.
4. We use PyAssimilator and use the best patterns.
6. We use PyAssimilator and have no dependencies in our code.
7. We use PyAssimilator and can switch one database to another in a matter of seconds.
7. We learn PyAssimilator once and use it forever!
7. **And most importantly, we make Python projects better!**

## So, do I really need it?

If you want to spend less time writing your code, but write better code - then you must use PyAssimilator.
It can be hard to start if you have no experience with good code, so you can watch creator's [video tutorials](https://knucklesuganda.github.io/py_assimilator/video_tutorials/).


## Our vision

Make Python the best programming language for enterprise development and use all of its dynamic capabilities to write
things that other languages can't even comprehend!

- Pattern substitution(switch databases easily) ✔️
- Event-based apps(in development) 🛠️
- 45% of all Python projects use PyAssimilator 🛠️
- Independent code(in development) 🛠️
- Adaptive patterns(in development) 🛠️
- Automatic code improvements(in development) 🛠️
- Decentralized code management(in development) 🛠️

If you want to help with any of those things - be free to contribute to the project. Remember, you never do anything for
free - and that will not be the case either.

## Sources
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [PyPI](https://pypi.org/project/py-assimilator/)
* [Documentation](https://knucklesuganda.github.io/py_assimilator/)
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [Author's YouTube RU](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw)
* [Author's YouTube ENG](https://www.youtube.com/channel/UCeC9LNDwRP9OfjyOFHaSikA)
* [Discord channel](https://discord.gg/gTVaGu7DHN)
* [Donations](https://www.donationalerts.com/r/pyassimilator)


------------------------------------------------------------

# Donate and create your own framework!

[Donate using this link](https://www.donationalerts.com/r/pyassimilator) and help PyAssimilator prosper! You can also request a feature that you want to see in our framework and we will have it in our priority list!

------------------------------------------------------------

## Contributors

<a href="https://github.com/knucklesuganda/py_assimilator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=knucklesuganda/py_assimilator" />
</a>

## Stars history

[![Star History Chart](https://api.star-history.com/svg?repos=knucklesuganda/py_assimilator&type=Date)](https://star-history.com/#knucklesuganda/py_assimilator&Date)

## ⭐Stargazers⭐

<div id="stargazers" style="display: flex;
    align-items: baseline; flex-wrap: wrap; align-content: center;
    flex-direction: row; padding: 0.2em;"></div>

<script>
    fetch("https://pyassimilator.azurewebsites.net/api/create_stars").then(async (response) => {
        const stargazers = await response.json();
        let stargazersHTML = '';

        const chunkSize = 10;
        for (let i = 0; i < stargazers.length; i += chunkSize) {
            let chunkHTML = "<div style='display: flex; width: 100%; justify-content: space-evenly'>";

            for(const stargazer of stargazers.slice(i, i + chunkSize)){
                chunkHTML += `<a href='${stargazer.url}' class='stargazer'>
                    <img src='${stargazer.avatar}'  style='width: 4em'>
                    <span style='display: none'>${stargazer.login}</span>
                </a>`;
            }

            stargazersHTML += chunkHTML + "</div>";
        }

        document.getElementById("stargazers").innerHTML = stargazersHTML;
    });
</script>

<style>
.stargazer:hover{

    transition: 100ms;
    border: 2px solid white;
    
    overflow: hidden;
    display: flex;
    
    align-items: flex-start;
    align-content: flex-start;
    justify-content: space-evenly;
    flex-direction: column;
    text-align: center;

}

.stargazer:hover > img{

    transition: 100ms;
    width: 12em!important;

}

.stargazer:hover > span{
    transition: 100ms;
    display: inherit!important;
    color: white;
    font-size: 1.4em;
}
</style>

## Types of patterns
These are different use cases for the patterns implemented:

- Database - patterns for database/data layer interactions.
- Events(in development) - projects with events or event-driven architecture.
- Unidentified - patterns that are useful for different purposes.

## Available providers
Providers are different patterns for external modules like SQLAlchemy or FastAPI.

- Alchemy(Database, Events) - patterns for [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) for both database and events.
- Kafka(Events) - patterns in [Kafka](https://kafka.apache.org/) related to events.
- Internal(Database, Events) - internal is the type of provider that saves everything in memory(dict, list and all the tools within your app).
- Redis(Database, Events) - redis_ allows us to work with [Redis](https://redis.io/) memory database.
- MongoDB(Database) - mongo allows us to work with [MongoDB](https://www.mongodb.com/) database.
