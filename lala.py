import requests
import prompt
import tool

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.base import MIMEBase
from email import encoders
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import prompt
from agent import agent
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import markdown
from dotenv import load_dotenv

# Import your tool functions
import tool

from test import mail


user_email = session.get("email") 
print( user_email)