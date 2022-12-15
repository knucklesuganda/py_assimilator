# Database patterns

## Repository
Repository is the pattern that makes a virtual collection out of the database.
When we use a database we often have some kind of library, language or protocol.
If we want to make the database abstract, we use the repository pattern. It has basic
functions that help us change and query our data from any source. The beauty of the pattern
is that you can use it with SQL, text files, cache, S3, external API's or any kind of data storage.


###### `__init__(session, initial_query)`
- session - each repository has a session that works as the primary data source. It can be your database connection, a text file or a data structure.
- initial_query - the initial query that you use in the data storage. We will show how it works later. It can be an SQL query, a key in the dictionary or anything else.

###### `_get_initial_query()`
returns the initial query used in the `_apply_specifications()`

###### `_apply_specifications`
Applies Specifications to the query. **Must not be used directly.** apply
specifications gets a list of specifications and applies them to the query returned
in _get_initial_query(). The idea is the following: each specification gets a query and
adds some filters to it. At the end we get a fully working query modified with the
specifications provided by the user.
- specifications - an iterable of specifications that can be used to specify some conditions in the query
> Specification is a pattern that adds filters or anything
else that specifies what kind of data we want.

###### `get`


###### `filter`


###### `save`


###### `delete`


###### `update`


###### `is_modified`


###### `refresh`

