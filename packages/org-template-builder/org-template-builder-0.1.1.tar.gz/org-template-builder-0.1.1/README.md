# Org-template-builder

```shell
pip install org-template-builder
```

```shell
python -m orgtemp myprojectname --author myname
```

The `orgtemp` process will raise an exception if the directory is not empty. It won&rsquo;t exit if it contains dotfiles, like `.git` or `.projectile`. This means that the best way to use it is the following.

```shell
mkdir myprojectname && cd myprojectname && python -m orgtemp myprojectname
```

This behaviour is to protect (in case of user mistake) overwriting existing configurations from other org-template-builder projects, individual checking/versioning/uninstalling has not been implemented.

The template will attempt to initialize a git repo with the `subprocess` module and add submodules to it but it won&rsquo;t make any commits. It will attempt to create and checkout a branch named `main`, to avoid using the default `master` name.


# Template Builder Arguments


## Project Name

Whenever `org-template-builder` installs all the parts, it will use whatever `projectname` was given to it to modify the default of a few files:

1.  Create a `.org` file in `src` and give it the `projectname`.
2.  Set the title and first header of that file to `projectname`.
3.  Set the `PROJECT_NAME` variable in the `Makefile`.

However, when copying the `projectname.md` file from `docs` to the root directory, `Makefile` will rename it to `README.md`.

If no project name is given, it will be set to &ldquo;readme&rdquo;.


## Author Name

The author name argument is optional, defaults to `""` and it is only added to the header of the `projectname.org` file.


# Introduction

This is an org-mode template for literate programming. The HTML theme is a fork of <https://github.com/fniessen/org-html-themes>.

The Makefile options are:

1.  `make update` will go over all submodules and pull any changes.
2.  `make` should call `tangle.el` and `publish.el` without `force`, which renders all the HTML and Markdown and copies all the static files from `resources` to `public`.
3.  `make clean` should remove all directories in `public` before running a `force` version of `publish`.
4.  `make commit` should run `publish` (non-forced) and then add and commit with automated timestamp.

```shell
make update
```

```shell
make
```

```shell
make clean
```


# Folder Structure

This is the structure from the root directory.

```shell
tree .. -I 'venv|orgtemp' -d
```

    ..
    ├── config
    ├── dist
    ├── docs
    ├── public
    │   ├── build
    │   └── resources
    ├── resources
    │   ├── images
    │   └── theme
    │       ├── css
    │       ├── js
    │       └── lib
    │           └── js
    ├── src
    └── tests
    
    15 directories

1.  Public: HTML directory for web.
    -   Resources: Copies of all files from root/resources specified on publish.el.
    -   Build: This is the equivalent of the `src` directory but for the HTML renders.
2.  Resources: All static files, plus the `theme` submodule from `org-theme` repository.
3.  Docs: The equivalent of `src` but for Markdown renders.
4.  Src: Where all org and tangled code files live.
5.  Tests: Reserved for writing tests with our without org files.

All files in `resources` that match the types specified in `publish.el` will be copied to `/public/resources`.

Having the `src` and `build` folders at the same tree level helps when accessing the equivalent `resources` folder from either directory.

![img](../resources/images/emacs.png "Emacs logo")


# Dependencies

The two base dependencies are in `config` and `resources/theme`. They do not share the same parent directory so the user must be careful when assuming their paths. The reason is simply to separate directories that are copied to `public`. So in case that there is any sensitive information in `config` we are sure it is not by default copied to `public`.

The file types to copy to public from resources are specified in the `publish.el` files anyway. And the `.gitignore` includes some paths in `resources` like `resources/keys` that at least won&rsquo;t be commited. In case of storing keys in json, it is not included in the static files as of `0.1.1`.

As of `0.1.1`, the static files are `"ico\\|png\\|jpg\\|jpeg\\|gif\\|svg\\|html\\|css\\|js\\|txt"`.

In conclusion we can say that dependencies go in two places, for the public dependencies, we use `resources` and for the rest we use the root directory by default.

My personal use of literate projects with org-mode is for studying and ETL-like processes where there may be data that I need to load from `resources`, then output the results in the same `resources` directory. In case of graphs and plots, `.png` files will be the results, but HTML and JS may also come into play.


# Default theme and modules

By default, the `resources/theme` path of the theme is referenced in `config/org-theme.config` and it will link to a relative path in the project directory.

However, there is a second file named `config/org-theme-alt.config` that will link to an external and absolute path that we can use instead of the default one.

We must set the name of the file in the header of our `.org` files and run `C-c C-c` in order to update the configuration.

```org
#+SETUPFILE: ../config/org-theme-alt.config
```

Then we can edit the contents of the file to fit our needs. Its default values link to the `org-template` repository but we can set them to wherever else.

Once we don&rsquo;t need the theme in `resources/theme` we can remove it from the repository.

```shell
git rm resources/theme
git commit "removed default theme"
```

That way we don&rsquo;t copy the contents to the `public` folder, as we are no longer using it. This can also be useful when dealing with a nested project where we may have trees of org projects and we want them to use the same common theme.


## Running from a parent project

We can apply the same idea to the headers of the org file and redirect to an absolute path outside of the `.org` file directory. Then we can run `make` from a parent repository because the default behaviour of `publish.el` is to act recursively, so all `.org` files in whatever directory we set, `src` by default, will be exported to the parent&rsquo;s directory respective `public` and `docs` directories.

In that case, we should also copy the resources path recursively in order to keep the folder structure of the new tree.


# Code Examples


## Shell Example

Shell source blocks don&rsquo;t tangle as they are normally one liners. This particular line just sets the local Python environment via `pyenv`, I don&rsquo;t need a `venv` for this demo.

We must make sure that `:dir` is set to the parent directory `..`.

```shell
pyenv local 3.7.13 && cat .python-version
```

    3.7.13


## SQL Example

This is an SQL query for the database specified in the `org-header.config` file, which is the pagila sample database. For changing the sql info it&rsquo;s always better to override the `header-args` in the current document while using the original configuration as reference.

```sql
SELECT
	CONCAT(customer.last_name, ', ', customer.first_name) AS customer,
	address.phone,
	film.title
FROM
	rental
	INNER JOIN customer ON rental.customer_id = customer.customer_id
	INNER JOIN address ON customer.address_id = address.address_id
	INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id
	INNER JOIN film ON inventory.film_id = film.film_id
WHERE
	rental.return_date IS NULL
	AND rental_date < CURRENT_DATE
ORDER BY
	title
LIMIT 5;
```

    customer	phone	title
    OLVERA, DWAYNE	62127829280	ACADEMY DINOSAUR
    HUEY, BRANDON	99883471275	ACE GOLDFINGER
    OWENS, CARMEN	272234298332	AFFAIR PREJUDICE
    HANNON, SETH	864392582257	AFRICAN EGG
    COLE, TRACY	371490777743	ALI FOREVER


## Elisp Example

Elisp blocks do not tangle by default either as they are mostly functions to evaluate on-the-go while using emacs.

```elisp
(run-python)
```

```elisp
(emacs-version)
```

    GNU Emacs 28.1 (build 1, x86_64-apple-darwin18.7.0, NS appkit-1671.60 Version 10.14.6 (Build 18G95))
     of 2022-05-11


## Python Example

Python uses a session, as specified in the `../config/org-header.config`, so there must be a `(run-python)` session running.

```python
print("TODO: finish this part.")
```

    TODO: finish this part.


# To Do


## TODO Fix the README file in the project root.

**Problem**: Whenever using the README.md file outside of a repository with the `resources` folder, the image links break.

**Possible solution**: Whenever copying the README.md to root, process it with a Python script so it references the public url address.


# Admonitions

Support for HTML export admonitions. Four colors for a few options.

<div class="note" id="orgbe27cae">
<p>
This is a note.
</p>

</div>

<div class="hint" id="org1af94f8">
<p>
This is a hint.
</p>

</div>

<div class="caution" id="org80efb3e">
<p>
This is a caution.
</p>

</div>

<div class="warning" id="org917e234">
<p>
This is a warning.
</p>

</div>
