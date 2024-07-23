# Project Name
Özyeğin University Lab & Artificial Department Introducer
## Description
This project is a result of the summer highschool internship program at Özyeğin University. The project aims to introduce the Interactive Inteligent Systems Labarotory and the nwely found faculty of artifical intelligence in Özyeğin University to the new students. The project is a controller for the QT robot which allows it to listen to students and answer their questions or concerns regarding tot he Faculty and the Labarotory of Interactive Inteligent Systems. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
* [Authors](#Authors)

## Installation
First, clone the project to a directory,

The run the following command to install the dependencies for the project.
```cd src```
``` pip3 install -r requirements.txt ```

Edit the `.env` file to feautre your groqcloud api key

## Usage
The project must be on the controller computer of the QT robot and it uses the ROS system to communicate with the robot. 
The conversations of the robot are defaulted to Turkish but can be changed to English by changing the language in the `WhispherMain.py`, `app.py` and `prompt.txt` files.

Run the following command to start the project the speak up. 
``` python3 run.py ```

## Authors
- [Atilla Altunbayrak](https://github.com/atialtunbayrak)
- [Talha Efe Üstün](https://github.com/talhaefeustun)
- [Efe Kayra]()