# Filament
A project aimed at calculating energy loss and costs of leaving lights on too long.

## Website installation and usage

 1. Clone this repository <br>
	    ```git clone https://github.com/kinghos/filament```
 2. Navigate to the "Filament" subdirectory <br>
        ```cd Filament```
 3. Run the server, making it accessible from any device <br>
        ```python manage.py runserver 0.0.0.0:8000```
 4. Access the server by navigating to 127.0.0.1:8000/filament on the host device, or the hosting device's IPv4 address followed by :8000/filament to access the website.
		
Note: This will only allow you to view the website, you will need to run the sensor interpretation code on a Raspberry Pi hosting the website to update the database.
