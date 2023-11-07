from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import uuid #gera um nome único para salvar as imagens