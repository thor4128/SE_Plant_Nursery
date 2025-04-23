# Plant Nursery

This project represents a structured configuration for an indoor plant nursery using XML. It contains curated plant collections with their names, sizes, care instructions, and associated images. The goal is to provide an organized way to manage and visually present houseplants with design tips.

## Table of Contents
1. [Introduction](#1-introduction)
2. [Tools Necessary](#2-tools-necessary)
3. [Project Structure](#3-project-structure)
4. [How to Use](#4-how-to-use)
5. [Sample XML Snippet](#5-sample-xml-snippet)
6. [Future Improvements](#6-future-improvements)
7. [Conclusion](#7-conclusion)

---

## 1. Introduction

This is a prototype version of an application that recommends plant sets based on user-specified space and environmental conditions. It aims to combine practicality with design, offering tailored suggestions for plant arrangements.

## 2. Tools Necessary

- .Net SDK 9.0
- Python 3.11 - 3.13 (ensure PyQT5 is supported)
- pip (make sure its up to date)

- PyQt5: 'pip install PyQT5'


## 3. Project Structure

This program uses a Python PyQt5 GUI for the frontend and a C# backend that handles data processing from XML files (serving as our database). The backend uses JsonSerializer to return the data to Python, where it's parsed and displayed in the GUI.

## 4. How to Use

click buttons make go.

(Seriously though: open the GUI, input your environment and garden bed size, and let the app recommend plants based on your inputs.)

## 5. Sample XML Snippet

'''xml
<Environment type="indoor">
    <collection number="0">
        <name>Snake Plant, Spider Plant, Peace Lily, ZZ Plant, Baby Rubber Plant</name>
        <length>0.9, 0.6, 0.6, 0.6, 0.45</length>
        <care>
            <light>indirect low</light>
            <water>low, medium</water>
            <designTip>For a bold and lively look, use Snake Plant, Spider Plant, Peace Lily, ZZ Plant, and Baby Rubber Plant to create a vibrant, untamed aesthetic.</designTip>
        </care>
        <image>"plant_images/Snake Plant.png", "plant_images/Spider Plant.png", "plant_images/Peace Lily.png", "plant_images/ZZ Plant.png", "plant_images/baby_rubber.png"</image>
    </collection>
</Environment>
'''

## 6. Future Improvements

This project was an experiment in integrating two programming languages (C# and Python) to create a functional plant recommendation system. Future improvements may include:

- Consolidating to one language for better maintainability

- Porting to mobile using a more suitable framework (e.g., .NET MAUI or a web-based solution)

- Integrating camera functionality to allow users to take a photo instead of manually inputting dimensions

## 7. Conclusion

It works. It looks good. We’re proud of it.
