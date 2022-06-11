## Resources
Database design: [link](https://drawsql.app/sevbo/diagrams/unibook-uz)
# How To Use
1. Clone the repository
 - ```bash
   git clone https://github.com/sevbo2003/unibook.uz-backend.git
    ```
2. Install dependencies
 - ```python
   pip install -r requirements.txt
    ```
3. Environment setup
    - open `.env.dev` file and enter your credentials end rename file to `.env`
4. Run server after this commands
    - ```python
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver
        ```

# How to create an app
1. Create a new app
    - ```python
      python manage.py startapp <app_name>
2. Move your app to the `apps` folder
3. Rename app name inside `apps.py` file from `name = '<app_name>'` to `name = 'apps.<app_name>'`
4. Add app name to `INSTALLED_APPS` list in `settings.py` with `'apps.<app_name>'`
5. Do what ever you want with your app

# How to contribute
1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push your changes to the repository
5. Open a pull request