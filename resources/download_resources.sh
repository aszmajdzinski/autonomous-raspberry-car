#!/bin/bash
curl -o saved_car_data.zip -L 'https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBbkhXUXplYlJidVVrTlZ1Z1UyZERYcTlVd0pUT1E_ZT14Vmo1QzQ/root/content'
unzip -q saved_car_data.zip
rm saved_car_data.zip