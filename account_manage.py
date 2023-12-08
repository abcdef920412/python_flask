from flask import Blueprint, render_template, redirect, request, session
from bson import ObjectId
from db_conn import db

account_manage_bp = Blueprint('account_manage', __name__)
